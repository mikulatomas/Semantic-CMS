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

var apiroot = "/semantic_admin/semantic/";

//CALLS

getNodes(function(nodes) {
  getEdges(function(edges) {

    var width = 960,
      height = 500;

    var zoom = d3.behavior.zoom()
      .scaleExtent([0.1, 10])
      .on("zoom", zoomed);

    var svg_tag = d3.select("body").selectAll("svg")
      .style("height", $(document).height() - 63);

    //Set real width and height
    width = parseInt(svg_tag.style("width"));
    height = parseInt(svg_tag.style("height"));

    $(".article-list-right").height($(document).height() - 90);

    svg = svg_tag.append("g")
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
      nodes.forEach(function (node) {
        if (node.id > lastNodeId) {
          lastNodeId = node.id;
        }
      });
    } else {
      lastNodeId = 0;
    }
    if (edges.length > 0) {
      lastEdgeId = edges[0].id;
      edges.forEach(function (edge) {
        if (edge.id > lastEdgeId) {
          lastEdgeId = edge.id;
        }
      });
    } else {
      lastEdgeId = 0;
    }

    console.log(nodes);

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
        return 100 + 20 * (d.source.number_of_descendants);
      })
      .chargeDistance(2000)
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

      node.selectAll("text").text(function(d) {
          return d.name;
        }).call(wrap, 70);

      redrawWeight();
    }

    function restart() {
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

          // select node
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

          if (selectedArticle) {
            if (d.article) {
              d.article = false;
              var index = article_nodes.indexOf(d.id);
              if (index > -1) {
                article_nodes.splice(index, 1);
              }
            } else {
              d.article = true;

              article_nodes.push(d.id);
            }
            restart();
            saveArticleNodes(selectedArticle, article_nodes);
          }
        })
        .on('mousedown', function(d) {
          //disable panning
          d3.event.stopImmediatePropagation();

          if (d3.event.shiftKey) {
            if (selected_node !== null && selected_node !== d && end_selected_node !== d) {
              mousedown_node = d;
              end_selected_node = mousedown_node;
              selected_link = null;
              hideButton("#delete");
              hideButton("#edit");
              showButton("#connect");
            } else {
              return;
            }
          } else {
            // select node
            mousedown_node = d;
            if (end_selected_node === null) {
              showButton("#delete");
              showButton("#edit");
            }
            if (mousedown_node === selected_node) return;
            else selected_node = mousedown_node;
            selected_link = null;
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
        child: end_selected_node.id
      };

      if (addEdge(link) === 0) {

        edges.push(link);
        refreshWeights(nodes);

        //MAYBE DELETE
        force.stop();
        force.linkDistance(function(d) {
          return 100 + 20 * (d.source.number_of_descendants);
        });
        force.start();

        restart();
      } else {
        lastEdgeId--;
        alert("Invalid connection.");
      }


    }

    function add() {
      // because :active only works in WebKit?
      svg.classed('active', true);

      var name;
      while (true) {
        name = prompt("Please enter (unique) name of the node");
        if (!checkIfNameExists(name)) {
          break;
        }
      }
      console.log(lastNodeId);
      var node = {
        id: ++lastNodeId,
        name: name,
        type: "semantic",
        number_of_descendants: 0
      };

      nodes.push(node);
      console.log(nodes);
      restart();
      saveGraph(nodes, edges);
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

    function edit(node) {
      // because :active only works in WebKit?
      // svg.classed('active', true);

      var name;
      while (true) {
        name = prompt("Please enter (unique) name of the node");
        if (!checkIfNameExists(name)) {
          break;
        }
      }

      node.name = name;

      restart();
      saveGraph(nodes, edges);
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
          return 30 + (25 * (Math.log((d.number_of_descendants + 2))));
        } else {
          return 40;
        }
      });
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

    document.getElementById("reset").addEventListener("click", function() {
      hideButton("#reset");
      $(".article").removeClass("selected");
      selectedArticle = null;
      article_nodes = [];
      restart();
    }, false);

    document.getElementById("add").addEventListener("click", function() {
      add();
    }, false);

    document.getElementById("edit").addEventListener("click", function() {
      edit(selected_node);
    }, false);

    document.getElementById("delete").addEventListener("click", function() {
      del();
      hideButton("#delete");
    }, false);

    document.getElementById("connect").addEventListener("click", function() {
      connect();
    }, false);

    svg.on('mousedown', mousedown);
    restart();
  });
});
