

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

// function flushAllD3Transitions() {
//     var now = Date.now;
//     Date.now = function() { return Infinity; };
//     d3.timer.flush();
//     Date.now = now;
//  }

//GLOBAL VARIABLES
var csrftoken = getCookie('csrftoken');

// mouse event vars
var selected_node = null,
    selected_link = null;

//CALLS
getNodes(function(nodes) {
  getEdges(function(edges) {

    var width = 960,
      height = 500;

    var svg = d3.select("body").selectAll("svg");

    svg.style("height", $(document).height() - 100);

    //Set real width and height
    width = parseInt(svg.style("width"));
    height = parseInt(svg.style("height"));

    var nodeById = d3.map();
    var lastNodeId = nodes[0].id;

    nodes.forEach(function(node) {
      nodeById.set(node.id, node);
    });

    console.log(nodes);
    console.log(edges);

    // nodeEnter = nodeEnter.data(nodes, function(d) { return d.id; });

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

    var path = svg.append('g').selectAll('path');
    var nodeEnter = svg.append('svg:g').selectAll("g");

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

      nodeEnter.attr('transform', function(d) {
        return 'translate(' + d.x + ',' + d.y + ')';
      });
    }

    function restart() {
      path = path.data(edges);

      path.classed('selected', function(d) { return d === selected_link; });

      path.enter().append('path')
        .attr('class', 'link')
        .style('marker-end', 'url(#end-arrow)')
        .on('mousedown', function(d) {
          // select node
          mousedown_link = d;
          if(mousedown_link === selected_link) selected_link = null;
          else selected_link = mousedown_link;
          selected_node = null;
          restart();

          restart();
        });

      // remove old links
      path.exit().remove();

      nodeEnter = nodeEnter.data(nodes, function(d) { return d.id; });

      nodeEnter.classed('selected', function(d) { return d === selected_node; });

      nodeEnter.enter().append("g").attr("class", "nodeGroup")
                .on('mousedown', function(d) {
                  // select node
                  mousedown_node = d;
                  if(mousedown_node === selected_node) selected_node = null;
                  else selected_node = mousedown_node;
                  selected_link = null;

                  restart();
                });

      var circle = nodeEnter.append("circle");

      circle.attr("class", "node")
        .attr("r", function(d) {
          return 40 + (d.number_of_descendants * 8);
        });

      var nodeText = nodeEnter.append("text");

      nodeText.attr("class", "text")
        .attr("dy", "0em")
        .attr("y", "4")
        .text(function(d) {
          return d.name;
        })
        .call(wrap, 70);

      nodeEnter.exit().remove();

      force.start();
      // flushAllD3Transitions();
    }

    document.getElementById("save").addEventListener("click", function() {
      saveData(nodes, edges);
    }, false);

    document.getElementById("add").addEventListener("click", function() {
      add();
    }, false);

    document.getElementById("restart").addEventListener("click", function() {
      restart();
    }, false);

    document.getElementById("delete").addEventListener("click", function() {
      del();
    }, false);

    function add() {
      // prevent I-bar on drag
      //d3.event.preventDefault();

      // because :active only works in WebKit?
      svg.classed('active', true);

      // if(d3.event.ctrlKey || mousedown_node || mousedown_link) return;

      // insert new node at point
      // var point = d3.mouse(this),
      // var nodesLength = nodes.length;
      var node = {id: ++lastNodeId, name: "added", is_root_node: true, number_of_descendants: 0};
      // node.x = point[0];
      // node.y = point[1];
      nodes.push(node);

      restart();
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
      if(selected_node) {
          nodes.splice(nodes.indexOf(selected_node), 1);
          spliceEdgesForNode(selected_node);
        } else if(selected_link) {
          edges.splice(edges.indexOf(selected_link), 1);
        }
        selected_link = null;
        selected_node = null;
        restart();
        console.log(nodes);
        console.log(edges);
    }

    function saveData(jsonNodes, jsonEdges) {
      $.ajaxSetup({
        beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
        }
      });

      console.log(jsonNodes);

      $.ajax({
        url: 'save/',
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
          alert(msg);
        }
      });
    }

    restart();
  });
});
