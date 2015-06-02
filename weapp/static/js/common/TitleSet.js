//点击头部导航设置图标
$('.ua-set').click(function(event) {
	console.log()
	var type = $('.ua-setBox').attr('type');
	// console.log('type', type);
	if (type=='off'){
		$('.ua-setBox').removeClass('hidden');
		$('.ua-setBox').attr('type', 'on');
		$(this).addClass('on');
	} else {
		$('.ua-setBox').addClass('hidden');
		$('.ua-setBox').attr('type', 'off');
		$(this).removeClass('on');
	}
 });