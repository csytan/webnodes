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
        while (row) {
            row = removeNodes(row);
            row = removeNodes(row); // for those hard to reach areas
            row = addChildNodes(row);
        }
    }
    
    layout(root); 
    
    function setNode(node) {
        node.childIds = graph[node.id] || [];
        node.start = node.start || 0;
        node.childTop = node.offsetTop + node.offsetHeight;
        node.childLeft = node.offsetLeft;
        node.childWidth = node.offsetWidth;
        return node;
    }

    function removeNodes(row) {
        var new_row = [];
        for (var i=0, node; node=row[i]; i++) {
            var left = row[i - 1];
            var right = row[i + 1];
            
            if (node.childIds.length) {
                new_row.push(node);
            } else if (left && node.childTop <= left.childTop && 
                    left.childIds.length - left.start > Math.floor(left.childWidth / options.minWidth)) {
                left.childWidth += node.childWidth;
            } else if (right && node.childTop <= right.childTop && 
                    right.childIds.length - right.start > Math.floor(right.childWidth / options.minWidth)) {
                right.childLeft = node.childLeft;
                right.childWidth += node.childWidth;
            } else {
                new_row.push(node);
            }
        }
        return new_row;
    }
    
    function addChildNodes(row) {
        var lowest=row[0], index = 0;
        for (var i = 0, node; node = row[i]; i++) {
            if (node.childTop < lowest.childTop && node.childIds.length) {
                lowest = node;
                index = i;
            }
        }
        
        if (!lowest) return null;
        if (!lowest.childIds.length) return null;
        
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
            $(node).find('.pagination').show();
            $(node).find('a.next').css('visibility', 'visible')
            .text('Next ' + (node.childIds.length - node.start - nChildren) + ' >');
        } else {
            $(node).find('a.next').css('visibility', 'hidden');
        }
        
        if (node.start) {
            $(node).find('.pagination').show();
            $(node).find('a.prev').css('visibility', 'visible')
            .text('< Prev ' + node.start);
        } else {
            $(node).find('a.prev').css('visibility', 'hidden');
        }
        
        node.childTop = node.offsetTop + node.offsetHeight;
        node.childTop += options.vertSpace * nChildren;
        
        if (!node.kids_per_page) node.kids_per_page = maxChildren;
        
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
            node.start += node.kids_per_page;
        } else {
            node.start -= node.kids_per_page;
            if (node.start < 0) node.start = 0;
        }
        
        $(document.body).css('min-height', $(document).height());        
        $('canvas').remove();
        $('.comment_container').hide();
        $(root).show();
        layout(root);
        
        return false;
    });
}
