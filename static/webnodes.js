var WebNodes = function(root, graph, options){
    // Fast Tree Layout    
    options = $.extend({
        minWidth: 400,
        linkColor: '#AFAFAF',
        linkWidth: 5,
        vertSpace: 20
    }, options);
        
    layout(root);
    
    function layout(root) {
        $(root).css({
            left: 0,
            width: '95%',
            display: 'block'
        });
        var row = [initNode(root)];
        while (row) {
            row = removeNodes(row);
            row = removeNodes(row); // for those hard to reach areas
            showNavButtons(row);
            row = addNodes(row);
        }
    }
    
    function initNode(node) {
        node.kids = graph[node.id] || []; // list of DOM ids
        node.start = node.start || 0; // pagination index
        node.priority = node.priority || 0;
        node.kidsLeft = node.offsetLeft;
        node.kidsWidth = node.offsetWidth;
        node.kidsTop = node.offsetTop + node.offsetHeight;
        updateNode(node);
        return node;
    }
    
    function updateNode(node) {
        node.maxKids = Math.floor(node.kidsWidth / options.minWidth);
        node.nKids = Math.min(node.maxKids, node.kids.length - node.start);
        node.needsSpace = node.kids.length - node.start > node.maxKids;
    }
    
    function expand(node, node2) {
        if (node.needsSpace && 
            ((node.kidsTop + 50 > node2.kidsTop && !node2.kids.length) ||
            node.priority > node2.priority)) {
            
            node.kidsLeft = Math.min(node.kidsLeft, node2.kidsLeft);
            node.kidsLeft = Math.min(node.kidsLeft, node2.kidsLeft);
            node.kidsWidth += node2.kidsWidth;
            node.kidsTop = Math.max(node.kidsTop, node2.kidsTop);
            updateNode(node);
            return true;
        }
        return false;
    }
    
    function removeNodes(row) {
        var next_row = [];
        for (var i=0, node; node=row[i]; i+=2){
            var node2 = row[i+1];
            if (!node2) {
                next_row.push(node);
            } else if (expand(node, node2)) {
                next_row.push(node);
            } else if (expand(node2, node)) {
                next_row.push(node2);
            } else {
                next_row.push(node, node2);
            }
        }
        return next_row;
    }
    
    function addNodes(row) {
        var lowest = row[0], index = 0;
        for (var i = 0, node; node = row[i]; i++) {
            if (!lowest.kids.length || (node.kidsTop < lowest.kidsTop && node.kids.length)) {
                lowest = node;
                index = i;
            }
        }
        if (!lowest) return null;
        
        var kids = layoutKids(lowest);
        var left = row.slice(0, index);
        var right = row.slice(index + 1);
        return left.concat(kids, right);
    }
    
    function layoutKids(node) {
        var width = node.kidsWidth / node.nKids;
        node.kidsTop += options.vertSpace * node.nKids;
        var kids = [];
        
        for (var i = 0, kid; i < node.nKids; i++) {
            var kid = document.getElementById(node.kids[node.start + i]);
            kid.style.top = node.kidsTop + 'px';
            kid.style.left = node.kidsLeft + (i * width) + 'px';
            kid.style.display = 'block';
            kid.style.width = width + 'px';
            
            initNode(kid);
            kids.push(kid);
        }
        
        drawConnections(node, kids);
        return kids;
    }
    
    function showNavButtons(nodes) {
        for (var i=0, node; node=nodes[i]; i++) {
            $(node).find('.pagination').css('visibility', 'hidden');
            var next = node.kids.length - node.start - node.nKids;
            if (next > 0) {
                $(node).find('.pagination').css('visibility', 'visible');
                $(node).find('a.next').css('visibility', 'visible')
                .text('Next ' + next + ' »');
                $(node).find('a.expand').css('visibility', 'visible');
            } else {
                $(node).find('a.next, a.expand').css('visibility', 'hidden');
            }
        
            if (node.start) {
                $(node).find('.pagination').css('visibility', 'visible');
                $(node).find('a.prev').css('visibility', 'visible')
                .text('« Prev ' + node.start);
            } else {
                $(node).find('a.prev').css('visibility', 'hidden');
            }
        }
    }
    
    function drawConnections(node, kids) {
        var x = node.offsetLeft + node.offsetWidth / 2 - node.kidsLeft;
        var y = node.offsetTop + node.offsetHeight - 5;
        var height = node.kidsTop - node.offsetTop - node.offsetHeight + 10;
        var canvas = document.createElement('canvas');
        
        canvas.width = node.kidsWidth;
        canvas.height = height;

        $(canvas).css({
            top: y,
            left: node.kidsLeft
        }).appendTo(document.body);
        
        // Initialize Excanvas
        if (window.G_vmlCanvasManager) {
            window.G_vmlCanvasManager.initElement(canvas);
        }
        
        var ctx = canvas.getContext('2d');
        ctx.strokeStyle = options.linkColor;
        ctx.lineWidth = options.linkWidth;
        
        for (var i = 0, kid; kid = kids[i]; i++) {
            var kidX = kid.offsetLeft + kid.offsetWidth / 2 - node.kidsLeft;
            
            ctx.beginPath();
            ctx.moveTo(x, 0);
            //ctx.lineTo(kidX, height);
            ctx.bezierCurveTo(x, height, kidX, height/2, kidX, height);
            ctx.stroke();
            ctx.closePath();
        }
    }
    
    // Events
    var priority = 1;
    $('.pagination a').live('click', function(e) {
        var node = $(this).closest('.comment_container')[0];

        if ($(this).hasClass('next')) {
            node.prev_starts = node.prev_starts || [];
            node.prev_starts.push(node.start);
            node.start += node.nKids;
        } else if ($(this).hasClass('prev')) {
            node.start = node.prev_starts.pop();
        } else {
            node.priority = priority++;
        }
        
        $(document.body).css('min-height', $(document).height());        
        $('canvas').remove();
        $('.comment_container').hide();
        $(root).show();
        layout(root);
        return false;
    });
}
