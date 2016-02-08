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

    var width = 960,
      height = 500;

    // var margin = {
    //     top: -5,
    //     right: -5,
    //     bottom: -5,
    //     left: -5
    // };

    var zoom = d3.behavior.zoom()
      .scaleExtent([0.1, 10])
      .on("zoom", zoomed);

    // var drag = d3.behavior.drag()
    //   .origin(function(d) {
    //     return d;
    //   })
    //   .on("dragstart", dragstarted)
    //   .on("drag", dragged)
    //   .on("dragend", dragended);

    var svg_tag = d3.select("body").selectAll("svg")
      .style("height", $(document).height() - 100);

    //Set real width and height
    width = parseInt(svg_tag.style("width"));
    height = parseInt(svg_tag.style("height"));

    svg = svg_tag.append("g")
      // .attr("transform")
      .call(zoom);

    var rect = svg.append("rect")
      .attr("width", width)
      .attr("height", height)
      .style("fill", "none")
      .style("pointer-events", "all");

    var container = svg.append("g");

    var nodeById = d3.map();
    var lastNodeId = nodes[0].id;
    var lastEdgeId = edges[0].id;

    nodes.forEach(function(node) {
      nodeById.set(node.id, node);
    });

    // console.log(nodes);
    // console.log(edges);

    // node = node.data(nodes, function(d) { return d.id; });

    edges.forEach(function(link) {
      link.source = nodeById.get(link.parent);
      link.target = nodeById.get(link.child);
      // link.right = true;
    });

    var force = d3.layout.force()
      .charge(-1000)
      .linkDistance(150)
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

    // line displayed when dragging new nodes
    // var drag_line = container.append('svg:path')
    //   .attr('class', 'link dragline hidden')
    //   .attr('d', 'M0,0L0,0');

    var path = container.append('g').selectAll('path');
    var node = container.append('svg:g');

    function zoomed() {
      container.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
    }

    function tick() {
      path.attr('d', function(d) {
        var deltaX = d.target.x - d.source.x,
          deltaY = d.target.y - d.source.y,
          dist = Math.sqrt(deltaX * deltaX + deltaY * deltaY),
          normX = deltaX / dist,
          normY = deltaY / dist,
          targetPadding = 43 + (d.target.number_of_descendants * 8),
          targetX = d.target.x - (targetPadding * normX),
          targetY = d.target.y - (targetPadding * normY);
        return 'M' + d.source.x + ',' + d.source.y + 'L' + targetX + ',' + targetY;
      });

      node.attr('transform', function(d) {
        return 'translate(' + d.x + ',' + d.y + ')';
      });
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
          if (mousedown_link === selected_link) return;
          else selected_link = mousedown_link;
          selected_node = null;

          restart();
        });

      // remove old links
      path.exit().remove();


      // NODES ////////////////////////
      node = node.selectAll("g").data(nodes, function(d) {
        return d.id;
      });

      node.classed('selected', function(d) {
        return d === selected_node;
      });

      node.classed('selected-end', function(d) {
        return d === end_selected_node;
      });

      var group = node.enter().append("g").attr("class", "nodeGroup")
        .on('mousedown', function(d) {
          //disable panning
          d3.event.stopImmediatePropagation();

          // console.log(selected_node);
          if (d3.event.shiftKey) {
            if (selected_node !== null && selected_node !== d && end_selected_node !== d) {
              mousedown_node = d;
              end_selected_node = mousedown_node;
              selected_link = null;
            } else {
              return;
            }
          } else {
            // select node
            mousedown_node = d;
            if (mousedown_node === selected_node) return;
            else selected_node = mousedown_node;
            selected_link = null;
          }

          restart();
        });

      //ADD CIRCLE
      group.append("circle")
        .attr("class", "node");

      group.selectAll("circle").attr("r", function(d) {
        return 40 + (d.number_of_descendants * 8);
      });

      //ADD TEXT
      group.append("text")
        .attr("class", "text")
        .attr("dy", "0em")
        .attr("y", "4")
        .text(function(d) {
          return d.name;
        })
        .call(wrap, 70);

      node.exit().remove();

      force.start();
    }

    document.getElementById("add").addEventListener("click", function() {
      add();
    }, false);

    // document.getElementById("restart").addEventListener("click", function() {
    //   restart();
    // }, false);

    document.getElementById("delete").addEventListener("click", function() {
      del();
    }, false);

    document.getElementById("connect").addEventListener("click", function() {
      connect();
    }, false);


    function mousedown() {
      var stop = d3.event.button;
      if (stop) d3.event.stopImmediatePropagation();

      if (selected_node !== null || selected_link !== null || end_selected_node !== null) {
        selected_node = null;
        selected_link = null;
        end_selected_node = null;
        restart();
      }
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
        url: 'add_edge/',
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
    }

    function addNode(node) {
      $.ajaxSetup({
        beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
        }
      });

      $.ajax({
        url: 'add_node/',
        type: 'POST',
        data: JSON.stringify(node),
        // data: JSON.stringify(jsonNodes),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: false,
        success: function(msg) {
          response = msg;
        }
      });
    }

    function saveGraph(jsonNodes, jsonEdges) {
      $.ajaxSetup({
        beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
        }
      });

      $.ajax({
        url: 'save_graph/',
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

    // function resetWeigth(edges) {
    //   edges.forEach(function(edge) {
    //     edge.number_of_descendants = 0;
    //   });
    // }

    function refreshWeights(nodes) {
      getNodes(function(nodesActual) {
        var nodeById = d3.map();

        nodesActual.forEach(function(node) {
          nodeById.set(node.id, node);
        });

        nodes.forEach(function(node) {
          if (node.number_of_descendants !== nodeById.get(node.id).number_of_descendants) {
            console.log("UDPATE");
          }
          node.number_of_descendants = nodeById.get(node.id).number_of_descendants;
        });
      });
    }

    function connect() {
      // resetWeigth(nodes);
      // restart();
      // console.log(nodes);
      // console.log(edges);

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

      addEdge(link);

      edges.push(link);
      refreshWeights(nodes);
      restart();

    }

    function add() {
      // prevent I-bar on drag
      //d3.event.preventDefault();

      // because :active only works in WebKit?
      svg.classed('active', true);

      // if(d3.event.ctrlKey || mousedown_node || mousedown_link) return;
      var name;

      while (true) {
        name = prompt("Please enter (unique) name of the node");
        if (!checkIfNameExists(name)) {
          break;
        }
      }

      // if (name.length === 0) {
      //   return;
      // }
      // insert new node at point
      // var point = d3.mouse(this),
      // var nodesLength = nodes.length;
      var node = {
        id: ++lastNodeId,
        name: name,
        is_root_node: true,
        is_leaf_node: true,
        number_of_descendants: 0
      };
      // node.x = point[0];
      // node.y = point[1];

      nodes.push(node);

      restart();

      saveGraph(nodes, edges);


    }

    function spliceEdgesForNode(node) {
      var toSplice = edges.filter(function(l) {
        return (l.source === node || l.target === node);
      });
      toSplice.map(function(l) {
        edges.splice(edges.indexOf(l), 1);
      });
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
      restart();
      saveGraph(nodes, edges);


      // console.log(nodes);
      // console.log(edges);
    }

    svg.on('mousedown', mousedown)
    restart();
  });
});
