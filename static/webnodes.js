var WebNodes = function(root, graph, options){
    // Fast Tree Layout    
    options = $.extend({
        minWidth: 400,
        linkColor: '#AFAFAF',
        linkWidth: 5,
        vertSpace: 20
    }, options);
    
    function layout(root) {
        var row = [initNode(root)];
        while (row) {
            row = removeNodes(row);
            row = removeNodes(row); // for those hard to reach areas
            row = addChildNodes(row);
        }
    }
    
    layout(root); 
    
    function initNode(node) {
        node.childIds = graph[node.id] || [];
        node.start = node.start || 0;
        node.childTop = node.offsetTop + node.offsetHeight;
        node.childLeft = node.offsetLeft;
        node.childWidth = node.offsetWidth;
        return node;
    }
    
    function setNode(node) {
        node.kidIds = graph[node.id] || [];
        node.start = node.start || 0;
        node.kidsTop = node.offsetTop + node.offsetHeight + 
                        options.vertSpace * node.nKids;
        node.kidsLeft = node.kidsLeft || node.offsetLeft;
        node.kidsWidth = node.kidsWidth || node.offsetWidth;
        
        node.maxKids = Math.floor(node.kidsWidth / options.minWidth);
        node.nKids = Math.min(node.maxKids, node.kidIds.length - node.start);
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
        var lowest = row[0], index = 0;
        for (var i = 0, node; node = row[i]; i++) {
            if (!lowest.childIds.length || (node.childTop < lowest.childTop && node.childIds.length)) {
                lowest = node;
                index = i;
            }
        }
        
        if (!lowest) return null;
        
        var kids = layoutChildren(lowest);
        var left = row.slice(0, index);
        var right = row.slice(index + 1);
        return left.concat(kids, right);
    }
    
    function layoutChildren(node) {
        var maxChildren = Math.floor(node.childWidth / options.minWidth);
        var nChildren = Math.min(maxChildren, node.childIds.length - node.start);
        var childWidth = node.childWidth / nChildren;
        var kids = [];
        
        node.childTop += options.vertSpace * nChildren;
        node.maxChildren = maxChildren;
        node.nChildren = nChildren;
        
        // Add child nodes
        for (var i = 0, child; i < nChildren; i++) {
            var child = document.getElementById(node.childIds[node.start + i]);
            child.style.top = node.childTop + 'px';
            child.style.left = node.childLeft + (i * childWidth) + 'px';
            child.style.display = 'block';
            child.style.width = childWidth + 'px';
            
            initNode(child);
            kids.push(child);
        }
        
        showPagination(node);
        drawConnections(node, kids);
        return kids;
    }
    
    function showPagination(node) {
        $(node).find('.pagination').css('visibility', 'hidden');
        if (node.start + node.nChildren < node.childIds.length) {
            $(node).find('.pagination').css('visibility', 'visible');
            $(node).find('a.next').css('visibility', 'visible')
            .text('Next ' + (node.childIds.length - node.start - node.nChildren) + ' »');
        } else {
            $(node).find('a.next').css('visibility', 'hidden');
        }
        
        if (node.start) {
            $(node).find('.pagination').css('visibility', 'visible');
            $(node).find('a.prev').css('visibility', 'visible')
            .text('« Prev ' + node.start);
        } else {
            $(node).find('a.prev').css('visibility', 'hidden');
        }
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
    
    // Events
    $('.pagination a').live('click', function(e) {
        var node = $(this).closest('.comment_container')[0];

        if ($(this).hasClass('next')) {
            node.start += node.nChildren;
        } else {
            node.start -= node.maxChildren;
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
