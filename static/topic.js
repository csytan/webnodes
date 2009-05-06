(function($){

$.fn.initTopic = function(graph, options){
    var root = this.css({
        left: 0,
        width: this.parent().width()
    });
    var container = this.parent();
    options = $.extend({
        minWidth: 400,
        linkColor: '#8F8F8F',
        linkWidth: 6,
        vertSpace: 5
    }, options);
    
    root.find('.comment').css('width', 600);
    layout();
    
    function layout() {
        root.show();
        var row = [initNode(root[0])];
        while (row) {
            row = removeNodes(row);
            row = removeNodes(row); // for those hard to reach areas
            row = addNodes(row);
        }
    }
    
    function update() {
        $(document.body).css('min-height', $(document).height());
        $('canvas').remove();
        $('.comment_box').hide();
        layout();
    }
    
    function initNode(node) {
        node.kids = node.kids || graph[node.id] || []; // list of DOM ids
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
        if (node.perPage) {
            node.perPage = Math.max(node.perPage, node.maxKids);
        } else {
            node.perPage = node.maxKids;
        }
    }

    function expand(node, node2) {
        if (node.needsSpace && !node2.kids.length && 
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
        var y = node.offsetTop + node.offsetHeight - 35;
        var height = node.kidsTop - node.offsetTop - node.offsetHeight + 40;
        var canvas = document.createElement('canvas');

        canvas.width = node.kidsWidth;
        canvas.height = height;

        $(canvas).css({
            top: y,
            left: node.kidsLeft
        }).appendTo(container);

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
            ctx.bezierCurveTo(x, height, kidX, height/2, kidX, height);
            ctx.stroke();
            ctx.closePath();
        }
    }

    // Comment button events
    $('a.next, a.prev').live('click', function(e) {
        if (e.button != 0) return;
        
        var node = $(this).closest('.comment_box')[0];
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
    
    var tiny_mce = false;
    var reply_node = null;
    $('a.reply').live('click', function(e){
        if (e.button != 0) return;
        
        var node = $(this).closest('.comment_box')[0];
        
        if (reply_node) {
            delete reply_node.kids;
            reply_node.start = reply_node.old_start;
        }
        reply_node = node;
        
        node.kids = ['reply_box'];
        node.old_start = node.start;
        node.start = 0;
        
        update();
        
        if (!tiny_mce) {
            tinyMCE.init({
                mode : "exact",
                elements: 'reply_textarea',
                auto_focus: 'reply_textarea',
                theme : 'advanced',
                theme_advanced_buttons1 : "bold,italic,|,blockquote,code,|,link,unlink,image",
                theme_advanced_buttons2 : "",
                theme_advanced_buttons3 : "",
                content_css : "/static/webnodes.css"
            });
            tiny_mce = true;
        }
        
        $('#parent_id').val(node.id);
        return false;
    });
    
    $('#reply_cancel').click(function(e){
        if (e.button != 0) return;
        reply_node.start = reply_node.old_start;
        delete reply_node.kids;
        update();
        return false;
    });
}

})(jQuery);

