var WebNodes = function(root, graph, options){
    // Fast Tree Layout    
    options = $.extend({
        minWidth: 350,
        linkColor: '#AFAFAF',
        linkWidth: 5,
        vertSpace: 20
    }, options);
    
    function layout(rootNode) {
        var row = [setNode(rootNode)];
        while (row.length) {
            row = removeNodes(row);
            row = addChildNodes(row);
        }
    }
    
    layout(root); 
    
    function setNode(node) {
        node.childIds = graph[node.id] || [];
        node.start = node.start || 0;
        node.visibleChildren = [];
        node.childTop = node.offsetTop + node.offsetHeight;
        node.childLeft = node.offsetLeft;
        node.childWidth = node.offsetWidth;
        return node;
    }

    function removeNodes(row) {
        var new_row = [];
        for (var i=0, node; node=row[i]; i++) {
            var leftNode = row[i - 1];
            var rightNode = row[i + 1];
            
            if (node.childIds.length) {
                new_row.push(node);
            } else if (leftNode && node.childTop <= leftNode.childTop && 
                    leftNode.childIds.length - leftNode.start > Math.floor(leftNode.childWidth / options.minWidth)) {
                leftNode.childWidth += node.childWidth;
            } else if (rightNode && node.childTop <= rightNode.childTop && 
                    rightNode.childIds.length - rightNode.start > Math.floor(rightNode.childWidth / options.minWidth)) {
                rightNode.childLeft = node.childLeft;
                rightNode.childWidth += node.childWidth;
            } else {
                new_row.push(node);
            }
        }
        return new_row;
    }
    
    function addChildNodes(row) {
        var lowest, index = 0;
        for (var i = 0, node; node = row[i]; i++) {
            if (!lowest || ( node.childTop < lowest.childTop ) || (!lowest.childIds.length)) {
                lowest = node;
                index = i;
            }
        }
        
        if (!lowest) return row;
        
        var kids = layoutChildren(lowest);
        drawConnections(lowest, kids);
        
        var left = row.slice(0, index);
        var right = row.slice(index + 1);
        return left.concat(kids, right);
    }
    
    function layoutChildren(node) {
        var maxChildren = Math.floor(node.childWidth / options.minWidth);
        var nChildren = Math.min(maxChildren, node.childIds.length - node.start);
        var childWidth = node.childWidth / nChildren;
        var kids = [];
        
        // Pagination
        $(node).find('.pagination').hide();
        if (node.start + nChildren < node.childIds.length) {
            $(node).find('.pagination').show()
            .find('span').text(node.start + 1 + ' / '+ node.childIds.length);
            $(node).find('a.next').css('visibility', 'visible');
        } else {
            $(node).find('a.next').css('visibility', 'hidden');
        }
        
        if (node.start) {
            $(node).find('.pagination').show()
            .find('span').text(node.start + 1 + ' / ' + node.childIds.length);
            $(node).find('a.prev').css('visibility', 'visible');
        } else {
            $(node).find('a.prev').css('visibility', 'hidden');
        }
        
        node.childTop = node.offsetTop + node.offsetHeight;
        node.childTop += options.vertSpace * nChildren;
        node.nChildren = maxChildren;
        
        // Add child nodes
        for (var i = 0, child; i < nChildren; i++) {
            var child = document.getElementById(node.childIds[node.start + i]);
            child.style.top = node.childTop + 'px';
            child.style.left = node.childLeft + (i * childWidth) + 'px';
            child.style.display = 'block';
            child.style.width = childWidth + 'px';
            
            setNode(child);
            kids.push(child);
        }
        return kids;
    }
    
    function drawConnections(node, kids) {
        var x = node.offsetLeft + node.offsetWidth / 2 - node.childLeft;
        var y = node.offsetTop + node.offsetHeight - 5;
        var height = kids.length * options.vertSpace + 10;
        
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
        
        for (var i = 0, child; child = kids[i]; i++) {
            var childX = child.offsetLeft + child.offsetWidth / 2 - node.childLeft;
            
            ctx.beginPath();
            ctx.moveTo(x, 0);
            //ctx.lineTo(childX, height);
            ctx.bezierCurveTo(x, height, childX, height/2, childX, height);
            ctx.stroke();
            ctx.closePath();
        }
    }
    
    
    $('.pagination a').live('click', function(e) {
        var node = $(this).closest('.comment_container')[0];

        if ($(this).hasClass('next')) {
            node.start += node.nChildren;
        } else {
            node.start -= node.nChildren;
        }

        $(document.body).height($(document).height());        
        $('canvas').remove();
        $('.comment_container').hide();
        $(root).show();
        layout(root);
        $(document.body).css('height', 'auto');
        return false;
    });
}
