$.fn.initTopic = function(graph){
    var ROOT = this.css({
        left: 0,
        width: this.parent().width() - 20
    });
    var CONTAINER = this.parent();
    var NODE_WIDTH = 350;
    var LINK_COLOR = '#6F6F6F';
    var LINK_WIDTH = 8;
    var VERT_SPACE = 10; // unit of vertical spacing between nodes
    
    
    function layout() {
        ROOT.show();
        var row = [initNode(ROOT[0])];
        while (row) {
            row = removeNodes(row);
            row = removeNodes(row); // for those hard to reach areas
            row = addNodes(row);
        }
        $('#content').css('min-height', $(document).height());
    }
    
    function update() {
        $('canvas').remove();
        $('.container').hide();
        layout();
    }
    
    function initNode(node) {
        node.kids = node.kids || graph[node.id] || []; // list of DOM ids
        node.start = node.start || 0; // pagination index
        node.kidsLeft = node.offsetLeft;
        node.kidsWidth = node.offsetWidth;
        node.kidsTop = node.offsetTop + node.offsetHeight;
        updateNode(node);
        return node;
    }
    
    function updateNode(node) {
        node.maxKids = Math.floor(node.kidsWidth / NODE_WIDTH);
        node.nKids = Math.min(node.maxKids, node.kids.length - node.start);
        node.needsSpace = node.kids.length - node.start > node.maxKids;
        node.perPage = Math.max(node.perPage, node.maxKids) || node.maxKids;
    }
    
    function expand(node, node2) {
        if (node.needsSpace && !node2.nKids &&
                node.kidsTop + 100 > node2.kidsTop) {
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
        for (var i=0, node; node=row[i]; i++){
            var node2 = row[i+1];
            if (node2) {
                if (expand(node, node2)) {
                    i++;
                } else if (expand(node2, node)) {
                    continue;
                }
            }
            next_row.push(node);
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
        node.kidsTop += VERT_SPACE * node.nKids;
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
        
        showNavButtons(node);
        drawConnections(node, kids);
        return kids;
    }
    
    function showNavButtons(node) {
        var next = node.kids.length - node.start - node.nKids;
        if (next > 0) {
            $(node).find('a.next').css('visibility', 'visible');
        } else {
            $(node).find('a.next').css('visibility', 'hidden');
        }
        
        if (node.start) {
            $(node).find('a.prev').css('visibility', 'visible');
        } else {
            $(node).find('a.prev').css('visibility', 'hidden');
        }
        
        if (next > 0 || node.start) {
            var curr_page = Math.ceil((node.start + node.nKids) / node.perPage);
            $(node).find('span.page_num').css('visibility', 'visible')
            .text(curr_page + ' of ' + Math.ceil(node.kids.length / node.perPage));
        } else {
            $(node).find('span.page_num').css('visibility', 'hidden');
        }
    }
    
    function drawConnections(node, kids) {
        var x = node.offsetLeft + node.offsetWidth / 2 - node.kidsLeft;
        var y = node.offsetTop + node.offsetHeight - 30;
        var height = node.kidsTop - node.offsetTop - node.offsetHeight + 30;
        var canvas = document.createElement('canvas');
        
        canvas.width = node.kidsWidth;
        canvas.height = height;
        
        $(canvas).css({
            top: y,
            left: node.kidsLeft
        }).appendTo(CONTAINER);
        
        // Initialize Excanvas
        if (window.G_vmlCanvasManager) {
            window.G_vmlCanvasManager.initElement(canvas);
        }
        
        var ctx = canvas.getContext('2d');
        ctx.strokeStyle = LINK_COLOR;
        ctx.lineWidth = LINK_WIDTH;
        
        for (var i = 0, kid; kid = kids[i]; i++) {
            var kidX = kid.offsetLeft + kid.offsetWidth / 2 - node.kidsLeft;
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.bezierCurveTo(x, height, kidX, height/2, kidX, height);
            ctx.stroke();
            ctx.closePath();
        }
    }
    
    
    // EVENTS
    $('a.next, a.prev').live('click', function(e) {
        // Reply pagination
        if (e.button != 0) return;
        
        var node = $(this).closest('.container')[0];
        if ($(this).hasClass('next')) {
            node.prev_starts = node.prev_starts || [];
            node.prev_starts.push(node.start);
            node.start += node.nKids;
        } else {
            node.start = node.prev_starts.pop();
        }
        update();
        return false;
    });
    
    layout();
    return this;
}
 
 