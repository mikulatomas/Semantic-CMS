//FUNCTIONS
function getNodes(callback) {
    d3.json("/api/semantic_node/", function(error, nodesJson) {
        if (error) return console.warn(error);
        callback(nodesJson);
    });
}

function getEdges(callback) {
    d3.json("/api/semantic_edge/", function(error, edgesJson) {
        if (error) return console.warn(error);
        callback(edgesJson);
    });
}

function wrap(text, width) {
    text.each(function() {
        var text = d3.select(this),
            words = text.text().split(/\s+/).reverse();
        if (words.length > 1) {
            var word,
                line = [],
                lineNumber = 0,
                lineHeight = 1, // ems
                y = text.attr("y"),
                dy = parseFloat(text.attr("dy")),
                tspan = text.text(null).append("tspan").attr("x", 0).attr("y", 0).attr("dy", dy + "em");

            while (word = words.pop()) {
                line.push(word);
                // tspan.attr("y", 0);
                tspan.text(line.join(" "));
                if (tspan.node().getComputedTextLength() > width) {
                    line.pop();
                    tspan.text(line.join(" "));
                    line = [word];
                    tspan = text.append("tspan").attr("x", 0).attr("y", 0).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
                }
            }
        }
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

//GLOBAL VARIABLES
var csrftoken = getCookie('csrftoken');

// mouse event vars
var selected_node = null,
    selected_link = null,
    mousedown_link = null,
    mousedown_node = null,
    mouseup_node = null,
    end_selected_node = null;

function resetMouseVars() {
    mousedown_node = null;
    mouseup_node = null;
    mousedown_link = null;
}

//CALLS

getNodes(function(nodes) {
    getEdges(function(edges) {

        var height = 400;
        var initialScale = 0.7;

        var zoom = d3.behavior.zoom()
            .scale(initialScale)
            .scaleExtent([0.5, 1.5])
            .on("zoom", zoomed);

        var svg_tag = d3.select("body").selectAll("svg")
            .style("height", height);

        //Set real width and height
        width = parseInt($(window).width());
        height = parseInt(svg_tag.style("height"));

        svg = svg_tag.append("g")
            .attr("transform", "translate(" +[width / 10,50]+ ")")
            .call(zoom);

        var rect = svg.append("rect")
            .attr("width", width)
            .attr("height", height)
            .style("fill", "none")
            .style("pointer-events", "all");

        var container = svg.append("g");

        var nodeById = d3.map();
        var lastNodeId;
        var lastEdgeId;

        if (nodes.length > 0) {
            lastNodeId = nodes[0].id;
            nodes.forEach(function(node) {
                if (node.id > lastNodeId) {
                    lastNodeId = node.id;
                }
            });
        } else {
            lastNodeId = 0;
        }
        if (edges.length > 0) {
            lastEdgeId = edges[0].id;
            edges.forEach(function(edge) {
                if (edge.id > lastEdgeId) {
                    lastEdgeId = edge.id;
                }
            });
        } else {
            lastEdgeId = 0;
        }

        nodes.forEach(function(node) {
            nodeById.set(node.id, node);
        });

        edges.forEach(function(link) {
            link.source = nodeById.get(link.parent);
            link.target = nodeById.get(link.child);
        });

        var force = d3.layout.force()
            .charge(-2000)
            // .linkDistance(150)
            .linkDistance(function(d) {
                return 110 + 20 * (d.source.number_of_descendants);
            })
            // .chargeDistance(5000)
            // .linkStrength(0.5)
            .gravity(0.1)
            .friction(0.7)
            .nodes(nodes)
            .links(edges)
            .size([width, height])
            .on('tick', tick);

        // Definition of the marker
        svg.append('svg:defs').append('svg:marker')
            .attr('id', 'end-arrow')
            .attr('viewBox', '0 -5 10 10')
            .attr('refX', 6)
            .attr('markerWidth', 4)
            .attr('markerHeight', 4)
            .attr('orient', 'auto')
            .append('svg:path')
            .attr('d', 'M0,-5L10,0L0,5')
            .attr('fill', 'gray');

        var path = container.append('g').selectAll('path');
        var node = container.append('svg:g').selectAll("g");

        function tick() {
            path.attr('d', function(d) {
                var deltaX = d.target.x - d.source.x,
                    deltaY = d.target.y - d.source.y,
                    dist = Math.sqrt(deltaX * deltaX + deltaY * deltaY),
                    normX = deltaX / dist,
                    normY = deltaY / dist,
                    targetPadding = 33 + (25 * (Math.log((d.target.number_of_descendants + 2)))),
                    targetX = d.target.x - (targetPadding * normX),
                    targetY = d.target.y - (targetPadding * normY);
                return 'M' + d.source.x + ',' + d.source.y + 'L' + targetX + ',' + targetY;
            });

            node.attr('transform', function(d) {
                return 'translate(' + d.x + ',' + d.y + ')';
            });

            redrawWeight();
        }

        function restart() {
            path = path.data(edges);

            path.classed('selected', function(d) {
                return d === selected_link;
            });

            path.enter().append('path')
                .attr('class', 'link')
                .style('marker-end', 'url(#end-arrow)');

            // remove old links
            path.exit().remove();


            // NODES ////////////////////////
            node = node.data(nodes, function(d) {
                return d.id;
            });

            node.classed('selected', function(d) {
                return d === selected_node;
            });

            node.classed('selected-end', function(d) {
                return d === end_selected_node;
            });

            redrawWeight();
            refreshArticleNodes();

            var group = node.enter().append("g").attr("class", "nodeGroup")
                .on('mousedown', function(d) {
                    //disable panning
                    d3.event.stopImmediatePropagation();

                    window.location = "/semantic/" + d.slug + "/";
                });

            //ADD CIRCLE
            group.append("circle")
                .attr("r", function(d) {
                    if (d.type === "semantic") {
                        return 20 + (25 * (Math.log((d.number_of_descendants + 2))));
                    } else {
                        return 40;
                    }
                });

            node.classed('article', function(d) {
                return d.article;
            });

            node.classed('node', function(d) {
                return !d.article;
            });

            //ADD TEXT
            group.append("text")
                .attr("class", "text")
                .attr("dy", "0em")
                .attr("y", "4");

            group.selectAll("text").text(function(d) {
                return d.name;
            }).call(wrap, 70);

            node.exit().remove();
            force.start();
        }

        // --------------------
        // HELP FUNCIONS
        // --------------------
        function zoomed() {
            container.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
        }

        function refreshWeights(nodes) {
            getNodes(function(nodesActual) {
                var nodeById = d3.map();

                nodesActual.forEach(function(node) {
                    nodeById.set(node.id, node);
                });
                nodes.forEach(function(node) {
                    node.number_of_descendants = nodeById.get(node.id).number_of_descendants;
                });
            });
        }

        function refreshArticleNodes() {
            nodes.forEach(function(d) {
                d.article = false;
                if (article_nodes !== undefined) {
                    article_nodes.forEach(function(n) {
                        if (d.id === n) {
                            d.article = true;
                            return;
                        }
                    });
                }
            });
        }

        function redrawWeight() {
            node.selectAll("circle").attr("r", function(d) {
                if (d.type === "semantic") {
                    return 30 + (25 * (Math.log((d.number_of_descendants + 2))));
                } else {
                    return 40;
                }
            });
        }

        // --------------------
        // HELP UI FUNCTIONS
        // --------------------

        function showElement(id) {
            $(id).removeClass("hidden");
        }

        function hideElement(id) {
            $(id).addClass("hidden");
        }

        var fixmeTop = $('.sidebar-content').offset().top;       // get initial position of the element




      $(function() {
          $("#show-topics").on("click", function() {

              $('#semantic-map').css({
                  position: 'fixed',
                  width: '100%',
                  height: '100%',
                  zIndex: '10',
              });
            //   $('#semantic-map').css({visibility: 'visible',});
              $('#semantic-map').attr("class", "border");
              width = parseInt($(window).width());
              height = parseInt($(window).height()) - 80;
              rect.attr("width", width)
                  .attr("height", height);
              svg.attr("transform", "translate(" +[0,50]+ ")");
              zoom.scale(1);
              container.attr("transform", "scale(" + 1 + ")");
              force.size([width, height]).resume();
              $('#hide-topics').removeClass("hidden");
          });
      });

      $(function() {
          $("#hide-topics").on("click", function() {

              $('#semantic-map').css({
                  position: 'static',
                  width: '100%',
                  height: '400',
                  zIndex: '1000',
                  visibility: 'visible',
              });
              if ($('#hide-topics').hasClass("switch")) {
                  $('#semantic-map').attr("class", "hidden");
              }

              width = parseInt($(window).width());
              height = parseInt(svg_tag.style("height"));
              rect.attr("width", width)
                  .attr("height", height);
              zoom.scale(initialScale);
              container.attr("transform", "scale(" + initialScale + ")");
              svg.attr("transform", "translate(" +[width / 10,50]+ ")");
              force.size([width, height]).resume();
              $('#hide-topics').addClass("hidden");
          });
      });


        container.attr("transform", "scale(" + initialScale + ")");

        restart();
    });
});
