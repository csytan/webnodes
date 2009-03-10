var WebNodes = function(root, graph, options){
    // Fast Tree Layout    
    options = $.extend({
        minWidth: 300,
        linkColor: '#00557F',
        linkWidth: 4,
        vertSpace: 20
    }, options);
    
    function setNode(node) {
        node.childIds = graph[node.id] || [];
        node.visibleChildren = [];
        node.childTop = node.offsetTop + node.offsetHeight;
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
        }
        drawConnections(root);
    }

    function expandNodes(row) {
        var new_row = [];
        for (var i=0, node; node=row[i]; i++) {
            var leftNode = row[i - 1];
            var rightNode = row[i + 1];
            
            if (node.childIds.length) {
                new_row.push(node);
            } else if (leftNode && node.childTop <= leftNode.childTop) {
                leftNode.childWidth += node.childWidth;
            } else if (rightNode && node.childTop <= rightNode.childTop) {
                rightNode.childLeft = node.childLeft;
                rightNode.childWidth += node.childWidth;
            } else {
                new_row.push(node);
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
        
        node.childTop = node.offsetTop + node.offsetHeight + options.vertSpace * nChildren;
        
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
    
    function drawConnections(node) {
        var x = node.offsetLeft + node.offsetWidth / 2 - node.childLeft;
        var y = node.offsetTop + node.offsetHeight - 5;
        var height = node.visibleChildren.length * options.vertSpace + 10;
        
        var canvas = document.createElement('canvas');
        
        canvas.width = node.childWidth;
        canvas.height = height;

        $(canvas).css({
            top: y,
            left: node.childLeft
        }).appendTo(document.body);
        
        // Initialize Excanvas
        if (window.G_vmlCanvasManager) {
            window.G_vmlCanvasManager.initElement(canvas);
        }
        
        var ctx = canvas.getContext('2d');
        ctx.strokeStyle = options.linkColor;
        ctx.lineWidth = options.linkWidth;
        
        for (var i = 0, child; child = node.visibleChildren[i]; i++) {
            var childX = child.offsetLeft + child.offsetWidth / 2 - node.childLeft;
            
            ctx.beginPath();
            ctx.moveTo(x, 0);
            //ctx.lineTo(childX, height);
            ctx.bezierCurveTo(x, height, childX, height/2, childX, height);
            ctx.stroke();
            ctx.closePath();
            drawConnections(child);
        }
    }
    
    layout(root);
}
