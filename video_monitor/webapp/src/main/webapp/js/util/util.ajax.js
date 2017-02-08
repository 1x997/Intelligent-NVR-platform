function doPost(url, data, onSuccess) {
	if ($.isFunction(data)) {
		onSuccess = data;
		data = undefined;
	}
	// 同域调用
	$.ajax({
		type : "POST",
		url : API_URL + url,
		dataType : 'json',
		data : {param:JSON.stringify(data)},
		success : function(data) {
			unblockUI();
			if (data.status.status_code == 0) {
				onSuccess(data.result, data.total);
			} else if (data.status.status_code == -2) {
				// 用户未登录，跳转至登录页面
				top.location.href = BASE_URL + 'login.html';
			} else {
				alert(data.status.status_reason);
			}
		}
	});
	// JSONP方式，跨域调用，调用测试机
/*	$.ajax({
		type : "POST",
		url : REMOTE_API_URL + url,
		dataType : 'jsonp',
		data : data,
		jsonp : 'callback',
		success : function(data) {
			if (data.status.status_code == 0) {
				onSuccess(data.result, data.total);
			} else if (data.status.status_code == 9999) {
				// 提示未登录的异常，跳转至指定页面
				window.location.replace(BASE_URL + 'timeout.html');
			} else {
				alert(data.status.status_reason);
			}
		}
	});*/
}