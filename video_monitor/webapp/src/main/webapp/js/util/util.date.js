/**
 * 获得当前日期<br/>
 * isNumber: 是否以8位数字形式返回
 */
var currentDate = function(isNumber) {
	var date = new Date();
	var separate = '-';
	if (isNumber) {
		separate = '';
	}
	var y = date.getFullYear();
	var m = date.getMonth() + 1;
	m = m < 10 ? ('0' + m) : m;
	var d = date.getDate();
	return y + separate + m + separate + d;
};

/**
 * 将日期转换为8位数字的形式
 */
var dateToNumber = function(value) {
	if (isEmpty(value)) {
		return;
	}
	var s = value.split('-');
	return s[0] + s[1] + s[2];
};

/**
 * 将8位数字形式的日期转换为“-”的格式
 */
var numberToDate = function(value) {
	if (isNull(value) || value.length != 8) {
		return ;
	}
	return value.substr(0,4) + '-' + value.substr(4,6) + '-' + value.substr(6,8);
};
