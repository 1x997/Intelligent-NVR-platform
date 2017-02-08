//=============global
// 从url地址中获取参数
function getUrlParam(name) {
	var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
	var r = window.location.search.substr(1).match(reg);  //匹配目标参数
	if (r!=null) {
		// return unescape(r[2]);
		return decodeURIComponent(r[2]);
	}
	return null; //返回参数值
}
// 往Session中添加属性
function setGlobalAttr(name, value) {
	$.session.set(name, value)
}
// 从Session中获得属性值
function getGlobalAttr(name) {
	return $.session.get(name);
}
// 从Session中移除指定属性
function removeGlobalAttr(name) {
	$.session.remove(name);
}
// ============= show message
function showWarn(message) {
	$.messager.alert('提示', message, 'warning');
}
function showInfo(message) {
	$.messager.alert('提示', message, 'info');
}
function showSuccess(message) {
	$.messager.alert('提示', message, 'success');
}

function deleteConfirm(onConfirm) {
	doConfirm('是否确定删除？', onConfirm);
}

function doConfirm(msg, onConfirm) {
	$.messager.confirm('提示', msg, function(result) {
		if (result) {
			onConfirm();
		}
	});
}
// ============== BlockUI
// 锁定页面，禁止操作
function blockUI(message, targetId) {
	if (isEmpty(message)) {
		message = "正在处理，请稍等...";
	}
	var options = {
		message : message,
		css : {
			color : '#fff',
			border : '3px solid #fff',
			backgroundColor : '#177cb0',
			padding : 20,
			margin : 30
		},
		overlayCSS : {
			opacity : '0.3',
			backgroundColor : '#aaa'
		}
	};
	if (isEmpty(targetId)) {
		$.blockUI(options);
	} else {
		$('#' + targetId).block(options);
	}
}
// 解除页面锁定
function unblockUI(targetId) {
	if (!$.unblockUI) {
		return;
	}
	if (isEmpty(targetId)) {
		$.unblockUI();
	} else {
		$('#' + targetId).unblock();
	}
}
// ============== tools
/**
 * 判断一个对象是否为空，null或者undefined
 * 
 * @param value
 * @returns {Boolean}
 */
function isNull(value) {
	return value == undefined || value == null;
}

function isNotNull(value) {
	return !isNull(value);
}

/**
 * 判断一个对象是否为空，null、undefined、空串、空数组
 * 
 * @param value
 * @returns {Boolean}
 */
function isEmpty(value) {
	return value == undefined || value == null || $.trim(value) == ""
			|| value.length == 0;
}

function isNotEmpty(value) {
	return !isEmpty(value);
}

// 是否存在指定函数
function isExitsFunction(funcName) {
	try {
		if (typeof (eval(funcName)) == "function") {
			return true;
		}
	} catch (e) {
	}
	return false;
}
// 是否存在指定变量
function isExitsVar(variableName) {
	try {
		if (typeof (eval(variableName)) != "undefined") {
			return true;
		}
	} catch (e) {
	}
	return false;
}
/**
 * 从表单中获得填写的数据，返回一个Object对象<br/> key为input中的name，value为输入的数据
 */
function getObjectInForm(formId) {
	var fields = $('#' + formId).serializeArray();
	var o = {};
	$.each(fields, function(n, value) {
		o[value.name] = value.value;
	});
	return o;
}
// 获得combobox选择的Value
function getValue(id) {
	return $('#' + id).textbox('getValue');
}

/**
 * 将数组组装成字符串返回
 * @param array		源数组
 * @param sep		字符串分割符
 * @param field		如果是Object的数组，指定field，否则为空
 */
function arrayToString(array, sep, field) {
	var result = '';
	if (isEmpty(array)) {
		return result;
	}
	$.each(array, function(n, value) {
		var v = isNull(field) ? value : value[field];
		result += (v + sep);
	});
	if (result.length > 0) {
		result = result.substr(0, result.length - 1);
	}
	return result;
}
/**
 * 滚动页面后，再次弹出编辑框，窗口停留在上次位置	
 * 以下代码，动态调整位置，始终出现在页面中央
 * @param dialogId
 */
function moveDialogToCenter(dialogId) {
	var top = $(document).scrollTop() + ($(window).height()-$("#" + dialogId).height() - 60) * 0.5;
	var left = ($(window).width()-$("#" + dialogId).width()) * 0.5;
	$("#" + dialogId).panel("move",{top:top, left:left});
	$('.window-shadow').css('top', top + 'px');
	$('.window-shadow').css('left', left + 'px');
}

// 替换所有匹配的字符
function replaceAll(str, targetValue, replaceValue) {
	if (isEmpty(str)) {
		return str;
	}
	return str.split(targetValue).join(replaceValue);
}

// 从数组中获取id匹配的text值，也可以自定义属性
function getValueFromArray(array, value, matchField, valueField) {
	if (!matchField) {
		matchField = 'id';
	}
	if (!valueField) {
		valueField = 'text';
	}
	for (var i in array) {
		var item = array[i];
		if (item[matchField] == value) {
			return item[valueField];
		}
	}
}
