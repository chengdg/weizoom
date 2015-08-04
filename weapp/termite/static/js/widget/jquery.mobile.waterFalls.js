 $.fn.waterFalls = function(options) {
    options = options || {};
    var maxHeight = 0;
    var $container;
    if(this[0].tarName === 'UL') {
        $container = this;
    }
    else {
        $container = this.find('ul:eq(0)');
    }
    var $item = options.$item || $container.find('li');
    var rowCount = options.rowCount || 3;
    var spacingY = options.spacingY || 5;
    var spacingX = options.spacingX || 5;
    var itemHeight;
    var itemWidth;
    var top = 0;
    var left = 0;
    var itemHeights = {};
    var rowMaxHeight = 0;
    $container.css({
        position: 'relative'
    })
    $item.each(function(i) {
        itemHeight = $(this).height();
        itemWidth = itemWidth || ($container.width() - (spacingY * (rowCount-1))) / rowCount;
        var index = i % rowCount;
        itemHeights[index] = !itemHeights[index] ? [] : itemHeights[index];
        itemHeights[index].push(itemHeight);
        top = 0
        
        var j, k;
        for(j = 0, k = itemHeights[index].length; j < k; j++) {
            if (itemHeights[index][j-1]) {
	    		top += itemHeights[index][j-1] + spacingY;
	    	}
            maxHeight = maxHeight > top + itemHeight ? maxHeight : top + itemHeight;
        }
        if(!itemHeights[index].length) {
        	maxHeight = top + itemHeight;
        }
        left = itemWidth * index;
        left = left ? left + (index * spacingX) : 0;
        rowMaxHeight = rowMaxHeight > top ? rowMaxHeight : top;
        $(this).css({
            position: 'absolute',
            top: top + 'px',
            left: left + 'px',
            width: itemWidth + 'px',
            'box-sizing': 'border-box',
            '-moz-box-sizing': 'border-box',
            '-webkit-box-sizing': 'border-box'
        });
    });
    $container.height(maxHeight);
};


// taking into account of the component when creating the window
// or at the create event
$(document).bind("pagecreate create", function(e) {
    $(":jqmData(ui-role=waterFalls)", e.target).waterFalls();
});
