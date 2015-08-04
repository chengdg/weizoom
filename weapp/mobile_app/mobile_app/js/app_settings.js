var sound;
var vibrator;
var push;
mui.init();
mui.ready(function(){
	mui.plusReady(function(){

		setSettings();
		getSettings();

	// 获取左侧设置栏
		function getSettings(){
			sound = plus.storage.getItem("sound");
			vibrator = plus.storage.getItem("vibrator");
			push = plus.storage.getItem("push");
			if (sound=='true') {
				document.getElementById("sound").classList.add('mui-active');
			}else{
				document.getElementById("sound").classList.remove('mui-active');
			}
			if (vibrator=='true') {
				document.getElementById("vibrator").classList.add('mui-active');
			}else {
				document.getElementById("vibrator").classList.remove('mui-active');
			}
			if (push=='true') {
				document.getElementById("push").classList.add('mui-active');
			}else {
				document.getElementById("push").classList.remove('mui-active');
			}
		}

		function setSettings(){
			document.getElementById("sound").addEventListener('toggle', function(event) {
				status = (this.classList.contains('mui-active') ? 'true' : 'false')
				plus.storage.setItem("sound",status);

			});
			document.getElementById("vibrator").addEventListener('toggle', function(event) {
				status = (this.classList.contains('mui-active') ? 'true' : 'false')
				plus.storage.setItem("vibrator",status);

			});
			document.getElementById("push").addEventListener('toggle', function(event) {
				status = (this.classList.contains('mui-active') ? 'true' : 'false')
				plus.storage.setItem("push",status);

			});

		}
	});
});