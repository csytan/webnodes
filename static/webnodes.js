var WebNodes = function(root, graph, options){
    // Fast Tree Layout    
    options = $.extend({
        minWidth: 250,
        maxWidth: 400,
        linkColor: '#00557F',
        linkWidth: 5,
        vertSpace: 60
    }, options);
    
    function setNode(node) {
        node.childIds = graph[node.id] || [];
        node.visibleChildren = [];
        node.childTop = node.offsetTop + node.offsetHeight + options.vertSpace;
        node.childLeft = node.offsetLeft;
        node.childWidth = node.offsetWidth;
        return node;
    }
    
    function layout(rootNode) {
        var row = [setNode(rootNode)];
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
        for (var i=0, node; node=row[i]; i++) {
            var leftNode = row[i - 1];
            var rightNode = row[i + 1];
            
            if (node.childIds.length) {
                new_row.push(node);
            } else if (leftNode && node.childTop < leftNode.childTop) {
                leftNode.childWidth += node.childWidth;
            } else if (rightNode && node.childTop < rightNode.childTop) {
                rightNode.childLeft = node.childLeft;
                rightNode.childWidth += node.childWidth;
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
        var nChildren = Math.min(maxChildren, node.childIds.length);
        var childWidth = node.childWidth / nChildren;
        
        // Add child nodes
        for (var j = 0, child; j < nChildren; j++) {
            var child = document.getElementById(node.childIds[j]);
            
            child.style.top = node.childTop + 'px';
            child.style.left = node.childLeft + (j * childWidth) + 'px';
            child.style.width = childWidth + 'px';
            child.style.display = 'block';
            
            setNode(child);
            
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
    
    layout(root);
}
