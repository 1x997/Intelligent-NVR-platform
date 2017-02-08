var checkType = [ {
	id : null,
	text : '全部'
}, {
	id : 'manAndHat',
	text : '安全帽检测'
}, {
	id : 'personAndCar',
	text : '人车识别'
}, {
	id : 'regionDection',
	text : '区域入侵'
} ];

$(function($) {
	initStationCC();
	$('#cc_check_type').combobox('loadData', checkType);
});

function initStationCC() {
	$('#cc_station').combobox({
		onSelect : function(rec) {
			loadCamera(rec.stationId);
		}
	});
	var url = 'camera/getStationList';
	doPost(url, function(result, total) {
		$('#cc_station').combobox('loadData', result);
		if (result.length > 0) {
			$('#cc_station').combobox('setValue', result[0].stationId);
		}
		doSearch();
	});
}

function loadCamera(stationId) {
	var url = 'camera/getCameraList';
	var param = {
		stationId : stationId
	};
	doPost(url, param, function(result, total) {
		result.reverse();
		result.push({
			cameraId: null,
			cameraName: '全部'
		});
		$('#cc_camera').combobox('loadData', result.reverse());
	});
}

function initAlarmGrid(param) {
	var columns = [ {
		title : '开始时间',
		width : '140',
		field : 'beginTime'
	}, {
		title : '结束时间',
		width : '140',
		field : 'endTime'
	}, {
		title : '摄像头',
		width : '100',
		field : 'cameraName'
	}, {
		title : '检测类型',
		width : '100',
		field : 'checkType',
		formatter: function(value){
			return getValueFromArray(checkType, value);
		}
	}, {
		title : '图片列表',
		width : '100',
		field : 'images',
		formatter:function(value, row, index) {
			if (value && value.length > 0) {
				var imagesDiv = $('<div/>');
				for (var i in value) {
					imagesDiv.append('<img class="image" src="' + value[i] + '"/>');
				}
				imagesDiv.append('<a href="javascript:;" onclick="showMoreImages(' + row.alarmId + ')">更多</a>');
				return imagesDiv.html();
			}
		}
	} ];
	// 初始化列表
	dataGridWithPager('alarm_grid', 'alarm/getAlarmList', {
		title : '告警',
		height : $(window).height() - 78,
		columns : [ columns ],
		onLoadSuccess: function() {
			$('.image').viewer({
				toolbar: false,
				navbar: false,
				movable: false
			});
		}
	}, param);
}

function doSearch() {
	var param = {};
	param.stationId = getValue('cc_station');
	param.cameraId = getValue('cc_camera');
	param.beginTime = getValue('dd_begin');
	param.endTime = getValue('dd_end');
	param.checkType = getValue('cc_check_type');
	initAlarmGrid(param);
}

function showMoreImages(alarmId) {
	$('#alarm_pic_dialog').show();
	$('#alarm_pic_dialog').dialog({
		title: '告警图片',    
		width: $(window).width() * 0.75,
		height: $(window).height() * 0.75,
		modal: true,
		href: './pic_wall.html',
		onLoad: function() {
			$('#tool_pagination').pagination({
				showRefresh: false,
				displayMsg: '',
				onSelectPage: function(pageNumber, pageSize) {
					loadMoreImages(alarmId,pageNumber, pageSize);
				}
			});
			loadMoreImages(alarmId, 1, 10);
		}
	});
}

function loadMoreImages(alarmId, pageNumber, pageSize) {
	var url = 'alarm/getAlarmImageList';
	var param = {
			alarmId: alarmId,
			pageNum: pageNumber - 1,
			pageSize: pageSize
	};
	doPost(url, param, function(result, total) {
		$('#tool_pagination').pagination({
			total: total
		});
		$('#div_img').empty();
		for (var i in result) {
			$('#div_img').append('<img src="' + result[i].imageUrl + '" alt="' + result[i].imageTime + '"/>');
		}
		$('#div_img img').css('width', '300px').css('margin', '8px')
		.css('float', 'left').css('box-shadow', '0 0 10px #888');
		$('#div_img img').viewer({
			toolbar: false,
			navbar: false,
			movable: false
		});
	});
}
