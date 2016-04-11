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
                if (tspan.node().getComputedTextLength() > width + 20) {
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

var apiroot = "/admin/semantic/";

//CALLS
$(function() {
getNodes(function(nodes) {
    getEdges(function(edges) {

        var width = 960,
            height = 500;

        var initialScale = 0.8;

        var zoom = d3.behavior.zoom()
            .scaleExtent([0.5, 1.5])
            .scale(initialScale)
            .on("zoom", zoomed);


        var doc_height = $(document).height() - 65;

        var svg_tag = d3.select("body").selectAll("svg")
            .style("height", doc_height);

        //Set real width and height
        width = parseInt(svg_tag.style("width"));
        height = parseInt(svg_tag.style("height"));

        // $(".articles").height($(document).height() - 394);
        $(".articles").css("height", doc_height - 200);
        // $(".articles").css("max-height", doc_height - 70);
        $(".article-list-right").css("height", doc_height);

        svg = svg_tag.append("g")
            .attr("transform", "translate(" +[width / 5,50]+ ")")
            .call(zoom);

        var rect = svg.append("rect")
            .attr("width", width)
            .attr("height", height)
            .style("fill", "none")
            .style("pointer-events", "all");

        var container = svg.append("g");

        refreshArticleNodes();

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
            .charge(-10000)
            // .linkDistance(150)
            .linkDistance(function(d) {
                return 80 + 9 * (d.source.number_of_descendants);
            })
            .chargeDistance(8000)
            // .linkStrength(0.5)
            .gravity(0.2)
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
            .attr('markerWidth', 3)
            .attr('markerHeight', 3)
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
                    targetPadding = 43 + (20 * (Math.log((d.target.number_of_descendants + 2)))),
                    targetX = d.target.x - (targetPadding * normX),
                    targetY = d.target.y - (targetPadding * normY);
                return 'M' + d.source.x + ',' + d.source.y + 'L' + targetX + ',' + targetY;
            });

            node.attr('transform', function(d) {
                return 'translate(' + d.x + ',' + d.y + ')';
            });

            node.selectAll("text").text(function(d) {
                return d.name;
            }).call(wrap, 70);

            redrawWeight();
        }

        function restart() {
            force.stop();
            path = path.data(edges);

            path.classed('selected', function(d) {
                return d === selected_link;
            });

            path.enter().append('path')
                .attr('class', 'link')
                .style('marker-end', 'url(#end-arrow)')
                .on('mousedown', function(d) {
                    //disable panning
                    d3.event.stopImmediatePropagation();

                    // select link
                    mousedown_link = d;
                    if (mousedown_link === selected_link) {
                        hideButton("#delete");
                        return;
                    } else {
                        showButton("#delete");
                        selected_link = mousedown_link;
                    }

                    selected_node = null;

                    restart();
                });

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
                .on('dblclick', function(d) {
                    //disable panning
                    d3.event.stopImmediatePropagation();

                    // Pokud je vybrán článek
                    if (selectedArticle) {
                        // Pokud je již člnek v daném tématu
                        if (d.article) {
                            d.article = false;
                            removeArticleFromSemantic(d);
                            // Pokud není článek v danném tématu
                        } else {
                            d.article = true;
                            addArticleToSemantic(d);
                        }
                        restart();
                        saveArticleNodes(selectedArticle, article_nodes);
                    }
                })
                .on('mousedown', function(d) {
                    //disable panning
                    d3.event.stopImmediatePropagation();

                    // Pokud je klik s klavesou shift
                    if (d3.event.shiftKey) {
                        // Neni vybrat node, Koncovy node neni ten na ktery klikam
                        if (selected_node !== null && end_selected_node !== d && selected_node !== d) {
                            mousedown_node = d;
                            end_selected_node = mousedown_node;
                            selected_link = null;
                            hideButton("#delete");
                            hideButton("#edit");
                            hideButton("#assign");
                            hideButton("#unassign");
                            showButton("#connect");
                        } else {
                            return;
                        }
                        // Pokud je pouze klik
                    } else {
                        mousedown_node = d;
                        // Pokud klikam na ten stejny node, nic nedelej
                        if (mousedown_node === selected_node) {
                            return;
                            // Jinak vyber node
                        } else {
                            // Odeznač vybrane spojeni
                            selected_link = null;

                            if (mousedown_node === end_selected_node) {
                                end_selected_node = null;
                            }

                            selected_node = mousedown_node;

                            // Pokud není vybrát koncovy node (delete nebo edit)
                            if (end_selected_node === null) {
                                showButton("#delete");
                                showButton("#edit");
                                hideButton("#connect");
                            }

                            //Pokud je vybrany članek
                            if (selectedArticle) {
                                // Pokud je članek jiz v kategorii
                                if (d.article) {
                                    showButton("#unassign");
                                    hideButton("#assign");
                                } else {
                                    showButton("#assign");
                                    hideButton("#unassign");
                                }
                            }
                        }
                    }

                    restart();
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
            // force.resume();
            force.start();
        }

        // --------------------
        // EDIT FUNCIONS
        // --------------------
        function connect() {
            if (end_selected_node === null) {
                return;
            }

            if (checkIfConnectionExists(edges, selected_node, end_selected_node)) {
                return;
            }

            var link;
            link = {
                id: ++lastEdgeId,
                source: selected_node,
                target: end_selected_node,
                parent: selected_node.id,
                child: end_selected_node.id,
                parent_name: selected_node.name,
                child_name: end_selected_node.name,
            };

            if (addEdge(link) === 0) {

                edges.push(link);
                refreshWeights(nodes);

                redrawWeight();
                restart();
            } else {
                lastEdgeId--;
                alert("Invalid connection.");
            }


        }

        function add(name) {
            // because :active only works in WebKit?
            svg.classed('active', true);

            if (checkIfNameExists(name)) {
                return 1;
            } else if (name.length > 25){
                return 2;
            } else {
                var node = {
                    id: ++lastNodeId,
                    name: name,
                    type: "semantic",
                    number_of_descendants: 0
                };

                nodes.push(node);

                restart();
                saveGraph(nodes, edges);
                return 0;
            }


        }

        function del() {

            if (selected_node) {
                nodes.splice(nodes.indexOf(selected_node), 1);
                spliceEdgesForNode(selected_node);
            } else if (selected_link) {
                edges.splice(edges.indexOf(selected_link), 1);
            }

            selected_link = null;
            selected_node = null;

            saveGraph(nodes, edges);
            refreshWeights(nodes);
            restart();
        }

        function edit(node, name) {
            // var name;
            // while (true) {
            //     name = prompt("Please enter (unique) name of the node");
            if (checkIfNameExists(name)) {
                return 1;
            } else if (name.length > 25){
                return 2;
            } else {
                node.name = name;

                restart();
                saveGraph(nodes, edges);
                return 0;
            }



        }

        function assign() {
            selected_node.article = true;
            addArticleToSemantic(selected_node);
            restart();
            saveArticleNodes(selectedArticle, article_nodes);
            hideButton("#assign");
            showButton("#unassign");
        }

        function unassign() {
            selected_node.article = false;
            removeArticleFromSemantic(selected_node);
            restart();
            saveArticleNodes(selectedArticle, article_nodes);
            showButton("#assign");
            hideButton("#unassign");
        }

        // --------------------
        // MOUSE FUNCIONS
        // --------------------
        function mousedown() {
            var stop = d3.event.button;
            if (stop) d3.event.stopImmediatePropagation();

            if (selected_node !== null || selected_link !== null || end_selected_node !== null) {
                selected_node = null;
                selected_link = null;
                end_selected_node = null;
                hideButton("#delete");
                hideButton("#edit");
                hideButton("#connect");
                hideButton("#assign");
                hideButton("#unassign");
                restart();
            }
        }

        // --------------------
        // HELP FUNCIONS
        // --------------------
        function zoomed() {
            container.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
        }

        function checkIfNameExists(name) {
            var exists = false;
            nodes.forEach(function(node) {
                if (node.name.toUpperCase() === name.toUpperCase()) {
                    exists = true;
                }
            });
            return exists;
        }

        function checkIfConnectionExists(edges, source_node, target_node) {
            var connections = edges.filter(function(l) {
                return (l.source === source_node && l.target === target_node) || (l.source === target_node && l.target === source_node);
            });

            return (connections.length > 0);
        }

        function refreshArticleNodes() {
            nodes.forEach(function(d) {
                d.article = false;
                article_nodes.forEach(function(n) {
                    if (d.id === n) {
                        d.article = true;
                        return;
                    }
                });
            });
        }

        function displayArticleNodes(button) {
            article_nodes = requestArticleNodes(button.id);
            selectedArticle = button.id;
            refreshArticleNodes();
            restart();
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

        function spliceEdgesForNode(node) {
            var toSplice = edges.filter(function(l) {
                return (l.source === node || l.target === node);
            });
            toSplice.map(function(l) {
                edges.splice(edges.indexOf(l), 1);
            });
        }

        function redrawWeight() {
            node.selectAll("circle").attr("r", function(d) {
                if (d.type === "semantic") {
                    // return 40 + (15 * (Math.sqrt((d.number_of_descendants + 2))));
                    return 40 + (20 * (Math.log((d.number_of_descendants + 2))));
                } else {
                    return 40;
                }
            });
        }

        function removeArticleFromSemantic(node) {
            var index = article_nodes.indexOf(node.id);
            if (index > -1) {
                article_nodes.splice(index, 1);
            }
        }

        function addArticleToSemantic(node) {
            article_nodes.push(node.id);
        }

        // --------------------
        // AJAX FUNCTIONS
        // --------------------
        function requestArticleNodes(article) {
            var response;
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });

            $.ajax({
                url: apiroot + 'request_article_nodes/',
                type: 'POST',
                data: JSON.stringify({
                    id: article
                }),
                // data: JSON.stringify(jsonNodes),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function(msg) {
                    response = msg;
                }
            });

            return response.message;
        }

        function saveArticleNodes(article, article_nodes) {
            var response;
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });

            $.ajax({
                url: apiroot + 'save_article_nodes/',
                type: 'POST',
                data: JSON.stringify({
                    id: article,
                    article_nodes: article_nodes
                }),
                // data: JSON.stringify(jsonNodes),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function(msg) {
                    response = msg;
                }
            });

            return response.message;
        }

        function saveGraph(jsonNodes, jsonEdges) {
            var response;
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });

            $.ajax({
                url: apiroot + 'save_graph/',
                type: 'POST',
                data: JSON.stringify({
                    nodes: jsonNodes,
                    edges: jsonEdges
                }),
                // data: JSON.stringify(jsonNodes),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function(msg) {
                    response = msg;
                }
            });
            return response.message;
        }

        function addEdge(edge) {
            var response;
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });

            $.ajax({
                url: apiroot + 'add_edge/',
                type: 'POST',
                data: JSON.stringify(edge),
                // data: JSON.stringify(jsonNodes),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function(msg) {
                    response = msg;
                }
            });

            return response.message;
        }

        // --------------------
        // HELP UI FUNCTIONS
        // --------------------

        function showButton(id) {
            $(id).removeClass("hidden");
        }

        function hideButton(id) {
            $(id).addClass("hidden");
        }

        // --------------------
        // UI
        // --------------------
        var articleButtonsList = document.getElementsByClassName("article");
        articleButtons = Array.prototype.slice.call(articleButtonsList, 0);

        articleButtons.forEach(function(button) {
            if (selectedArticle == button.id) {
                $("#" + button.id).addClass("selected");
                showButton("#reset");
            }
            button.addEventListener("click", function() {
                $(".article").removeClass("selected");
                $("#" + button.id).addClass("selected");

                displayArticleNodes(button);
                showButton("#reset");
            }, false);
        });

        $("#dialog-confirm").dialog({
            autoOpen: false,
            resizable: false,
            width: 400,
            modal: true,
            buttons: [{
                text: "Delete",
                "class": 'btn btn-red-solid',
                click: function() {
                    del();
                    hideButton("#edit");
                    hideButton("#delete");
                    $(this).dialog("close");
                }
            }, {
                text: "Cancel",
                "class": 'btn btn-gray-outline',
                click: function() {
                    $(this).dialog("close");
                }
            }]
        });

        $("#dialog-help").dialog({
            autoOpen: false,
            resizable: false,
            width: 800,
            modal: true,
            buttons: [{
                text: "OK",
                "class": 'btn btn-gray-outline',
                click: function() {
                    $(this).dialog("close");
                }
            }]
        });

        $("#dialog-add").dialog({
            autoOpen: false,
            resizable: false,
            width: 400,
            modal: true,
            buttons: [{
                text: "Add",
                "class": 'btn btn-green-solid',
                click: function() {
                    var result = add($("#new-node-name").val());

                    if (result === 1) {
                        $(".error").text("You have to enter uqnique non-empty name!");
                        return;
                    } else if (result === 2) {
                        $(".error").text("The name is too long (25 char max).");
                        return;
                    }
                    $("#new-node-name").val("Node name");
                    $(".error").empty();
                    $(this).dialog("close");
                }
            }, {
                text: "Cancel",
                "class": 'btn btn-gray-outline',
                click: function() {
                    $("#new-node-name").val("Node name");
                    $(".error").empty();
                    $(this).dialog("close");
                }
            }]
        });

        $("#dialog-edit").dialog({
            autoOpen: false,
            resizable: false,
            width: 400,
            modal: true,
            buttons: [{
                text: "Rename",
                "class": 'btn btn-green-solid',
                click: function() {
                    var result = edit(selected_node, $("#rename-node-name").val());

                    if (result === 1) {
                        $(".error").text("You have to enter uqnique non-empty name!");
                        return;
                    } else if (result === 2) {
                        $(".error").text("The name is too long (25 char max).");
                        return;
                    }
                    // $("#rename-node-name").val("Node name");
                    $(".error").empty();
                    $(this).dialog("close");
                }
            }, {
                text: "Cancel",
                "class": 'btn btn-gray-outline',
                click: function() {
                    $("#rename-node-name").val("Node name");
                    $(".error").empty();
                    $(this).dialog("close");
                }
            }]
        });

        document.getElementById("reset").addEventListener("click", function() {
            hideButton("#reset");
            hideButton("#assign");
            $(".article").removeClass("selected");
            selectedArticle = null;
            article_nodes = [];
            restart();
        }, false);

        document.getElementById("help").addEventListener("click", function() {
          $("#dialog-help").removeClass("hidden");
            $("#dialog-help").dialog("open");
        }, false);

        document.getElementById("add").addEventListener("click", function() {
          $("#dialog-add").removeClass("hidden");
            $("#dialog-add").dialog("open");
        }, false);

        document.getElementById("edit").addEventListener("click", function() {
          $("#dialog-edit").removeClass("hidden");
            $("#rename-node-name").val(selected_node.name);
            $("#dialog-edit").dialog("open");
        }, false);

        document.getElementById("delete").addEventListener("click", function() {
          $("#dialog-confirm").removeClass("hidden");
            $("#dialog-confirm").dialog("open");

        }, false);

        document.getElementById("connect").addEventListener("click", function() {
            connect();
        }, false);

        document.getElementById("assign").addEventListener("click", function() {
            assign();
        }, false);

        document.getElementById("unassign").addEventListener("click", function() {
            unassign();
        }, false);

        svg.on('mousedown', mousedown);
        container.attr("transform", "scale(" + initialScale + ")");
        // zoom.translate([100,0]);
        // container.attr("transform", "translate(" +[100,0]+ ")");
        // force.start();
        restart();
    });
});
});
