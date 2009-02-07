var WEBNODES = function(root, settings){
	// Fast Tree Layout 
	settings = $.extend({
		minWidth: 250,
		maxWidth: 600,
		linkColor: 'black',
		linkWidth: 10,
		horSpacing: 20,
		vertSpacing: 50,
		service: '/commands?action=dispatch',
		graph: {}
	}, settings);
	
	var Node = function(element) {
		this.element = element;
		this.childIds = settings.graph[element.id] || [];
		this.children = []; // Displayed children
		
		this.top = element.offsetTop;
		this.left = element.offsetLeft;
		this.width = element.offsetWidth;
		this.height = element.offsetHeight;
		this.right = this.left + this.width;
		this.bottom = this.top + this.height;
		
		// Positions for this node's children
		this.childTop = this.bottom + 50;
		this.childLeft = this.left;
		this.childRight = this.right;
	}

	var root = new Node(root);
	
	function log(row, out) {
		for (var i = 0, node; node = row[i]; i++) {
			out += node.element.id + ", ";
		}
		console.log(out);
	}	
	
	function layout() {
		var row = [root];
		while (row.length) {
			//log(row, "children :");
			removeNodes(row);
			//log(row, "culled :");
			layoutChildren(row);
		}
		drawConnections(root);
	}

	function removeNodes(row) {
		// Removes nodes that don't have any children, and lets adjacent nodes take up their space
		for (var i = 0, node; node = row[i]; i++) {
			if (node.childIds.length) continue;
			
			var leftNode = row[i - 1];
			var rightNode = row[i + 1];
			if (leftNode) {
				leftNode.childTop = Math.max(leftNode.childTop, node.bottom + 50);
				leftNode.childRight = node.right;
			} else if (rightNode) {
				rightNode.childTop = Math.max(rightNode.childTop, node.bottom + 50);
				rightNode.childLeft = node.left;
			}
			
			// Remove node and continue to next node
			row.splice(i--, 1);
		}
	}
		
	function layoutChildren(row) {
		for (var i = 0, node; node = row[i]; i++) {
			var totWidth = node.childRight - node.childLeft;
			var maxChildren = Math.floor(totWidth / settings.minWidth);
			var nChildren = Math.min(maxChildren, node.childIds.length);
			var childWidth = (totWidth - settings.horSpacing * (nChildren -1)) / nChildren;
			
			// Remove parent node
			row.splice(i, 1);
			
			// Add child nodes
			for (var j = 0, child, element; j < nChildren; j++) {
				element = document.getElementById(node.childIds[j]);
				
				element.style.top = node.childTop + "px";
				element.style.left = node.childLeft + childWidth * j + settings.horSpacing * j + "px";
				element.style.width = childWidth + "px";
				element.style.display = "block";
				
				child = new Node(element);
				node.children.push(child);
				row.splice(i++, 0, child);
			}
			i--;
		}
	}
	
	function drawConnection(ctx, node) {
		for (var i = 0, child; child = node.children[i]; i++) {
			var x = node.left + node.width / 2;
			var y = node.bottom - 5;
			var childX = child.left + child.width / 2;
			var childY = child.top + 5;
			var dY = childY - y;
			
			ctx.moveTo(x, y);
			//ctx.lineTo(childX, childY);
			//ctx.quadraticCurveTo(childX, y, childX, childY);
			ctx.bezierCurveTo(x, childY, childX, y + dY / 2, childX, childY);
			drawConnection(ctx, child);
		}
	}
	
	function drawConnections(node) {
		var canvas = document.createElement('canvas');
		
		canvas.width = $("#container").width();
		canvas.height = 3000;
		
		$(canvas).css({
			"top": 0,
			"left": 0
		}).appendTo("#container");
		
		// Initialize Excanvas
		if (window.G_vmlCanvasManager) {
			window.G_vmlCanvasManager.initElement(canvas);
		}
		
		var ctx = canvas.getContext("2d");
		ctx.strokeStyle = settings.linkColor;
		ctx.lineWidth = settings.linkWidth;
		
		ctx.beginPath();
		
		drawConnection(ctx, node);
		
		ctx.stroke();
		ctx.closePath();
	}
	
	layout();
}

var submitReply = function(id) {
	var content = prompt("content", id);
	return false;
}