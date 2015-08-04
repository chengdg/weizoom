$.ui.ready(function() {
	initLocalStore();
	$(".list").bind("click", settingFunction);
});

function settingFunction(){
	var isSound = $("#sound").prop("checked");
	var isVibrator = $("#vibrator").prop("checked");
	var isPush = $("#push").prop("checked");
	dthMobileOA.putBooleanData("sound", isSound);
	dthMobileOA.putBooleanData("vibrator", isVibrator);
	dthMobileOA.putBooleanData("push", isPush);
}
