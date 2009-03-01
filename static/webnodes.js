var WebNodes = function(root, graph, options){
    // Fast Tree Layout    
    options = $.extend({
        minWidth: 250,
        maxWidth: 400,
        linkColor: '#00557F',
        linkWidth: 5,
        horSpace: 10, // Space on both sides of the node
        vertSpace: 60
    }, options);
    
    function setNode(node) {
        node.childIds = graph[node.id] || [];
        node.visibleChildren = [];
        return node;
    }

    function layout() {
        var row = [setNode(root)];
        var height = 0;
        while (row.length) {
            row = expandNodes(row);
            //console.log('removed', row);
            row = layoutChildren(row);
            //console.log('children', row);
            
            // find the max height of the document
            for (var i=0, node; node=row[i]; i++) {
                if (height < node.childTop)
                    height = node.childTop;
            }
        }
        drawConnections(root, height);
    }

    function expandNodes(row) {
        var new_row = [];
        for (var i = 0, node; node = row[i]; i++) {
            node.childTop = node.offsetTop + node.offsetHeight + options.vertSpace;
            node.childLeft = node.offsetLeft;
            node.childWidth = node.offsetWidth;
            
            if (node.childIds.length) {
                new_row.push(node);
            }
        }
        
        for (var i=0, node; node=row[i]; i++) {
            var leftNode = row[i - 1];
            var rightNode = row[i + 1];
            
            if (leftNode) {
                node.childLeft = leftNode.offsetLeft + leftNode.offsetWidth;
            } else {
                node.childLeft = 0;
            }
            
            if (rightNode) {
                node.childWidth = rightNode.offsetLeft - node.childLeft -options.horSpace;
            }
        }
        return new_row;
    }
        
    function layoutChildren(row) {
        var lowest;
        var indexLow = 0;
        for (var i = 0, node; node = row[i]; i++) {
            if (!lowest || ( node.childTop < lowest.childTop )) {
                lowest = node;
                indexLow = i;
            }
        }
        
        if (!lowest) return row;
        
        node = lowest;
        row.splice(indexLow, 1);

        var maxChildren = Math.floor(node.childWidth / options.minWidth);
        node.maxChildren = maxChildren;
        var nChildren = Math.min(maxChildren, node.childIds.length);
        var childWidth = node.childWidth / nChildren;
        
        // Add child nodes
        for (var j = 0, child; j < nChildren; j++) {
            var child = document.getElementById(node.childIds[j]);
            
            child.style.top = node.childTop + 'px';
            child.style.left = node.childLeft + (j * childWidth) + options.horSpace + 'px';
            child.style.width = childWidth - 2 * options.horSpace + 'px';
            child.style.display = 'block';
            
            if (childWidth > options.maxWidth) {
                child.style.width = options.maxWidth + 'px';
            }
            
            setNode(child);
            
            //child.childWidth = childWidth + (options.horSpace * j);
            
            node.visibleChildren.push(child);
            row.splice(indexLow++, 0, child);
        }
        
        return row;
    }
    
    function drawConnection(ctx, node) {
        for (var i = 0, child; child = node.visibleChildren[i]; i++) {
            var x = node.offsetLeft + node.offsetWidth / 2;
            var y = node.offsetTop + node.offsetHeight - 5;
            var childX = child.offsetLeft + child.offsetWidth / 2;
            var childY = child.offsetTop + 5;
            var dY = childY - y;
            
            ctx.moveTo(x, y);
            //ctx.lineTo(childX, childY);
            //ctx.quadraticCurveTo(childX, y, childX, childY);
            ctx.bezierCurveTo(x, childY, childX, y + dY / 2, childX, childY);
            drawConnection(ctx, child);
        }
    }
    
    function drawConnections(node, height) {
        var canvas = document.createElement('canvas');
        
        canvas.width = $("#container").width();
        canvas.height = height;
        
        $(canvas).css({
            top: 0,
            left: 0
        }).appendTo("#container");
        
        // Initialize Excanvas
        if (window.G_vmlCanvasManager) {
            window.G_vmlCanvasManager.initElement(canvas);
        }
        
        var ctx = canvas.getContext("2d");
        ctx.strokeStyle = options.linkColor;
        ctx.lineWidth = options.linkWidth;
        
        ctx.beginPath();
        
        drawConnection(ctx, node);
        
        ctx.stroke();
        ctx.closePath();
    }
    
    layout();
}
