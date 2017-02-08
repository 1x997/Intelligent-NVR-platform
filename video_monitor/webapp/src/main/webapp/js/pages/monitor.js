var previewAX;
$(function($) {
	initMenuTree();
	loadMenuTree();

	previewAX = $("#PreviewActiveX").get(0);

	$('#tool_pagination').pagination({
		pageSize: 4,
		pageList: [1,4,9,16],
		showRefresh: false,
		displayMsg: '',
		onSelectPage: function(pageNumber, pageSize) {
			loadMultiple(pageNumber, pageSize);
		}
	});
});

function initMenuTree() {
	$('#menu_tree').tree({
		animate : true,
		checkbox : false,
		formatter : function(node) {
			return node.stationName || node.cameraName;
		},
		onBeforeExpand : function(node) {
			if (node.stationType == 0 && node.children.length == 0) {
				// 变电站，且尚未加载子节点
				var url = 'camera/getCameraList';
				var param = {
					stationId : node.stationId
				};
				doPost(url, param, function(result, total) {
					// 追加数据
					$('#menu_tree').tree('append', {
						parent : node.target,
						data : result
					});
					node.children = result;
					// 数据加载后，手动展开
					$('#menu_tree').tree('expand', node.target);
				});
				// 取消自动展开
				return false;
			}
		},
		onSelect : function(node) {
			if (node.stationId) {
				// 点击变电站
				loadMultiple(1);
			} else if (node.cameraId) {
				// 点击摄像头
				loadSingle(node.cameraId);
			}
		}
	});
}

// 加载显示单个画面
function loadSingle(cameraId) {
	try {
		previewAX.StopRealPlayAll();
	} catch (e) {}
	previewAX.HWP_ArrangeWindow(1);// 默认恢复为单画面
	$('#div_tool').hide();
	$('#div_layout').layout('resize');
	var url = 'camera/getCameraListByPage';
	var param = {cameraId: cameraId};
	doPost(url, param, function(result, total) {
		var item = result[0];
		if (item.url) {
			previewAX.HWP_Play(item.url, item.password, 0, '', '');
		}
	});
}

// 加载显示多个画面
function loadMultiple(pageNum, pageSize) {
	if (!pageSize) {
		// 点击node调用时，不传pageSize，重新获取
		pageSize = $('#tool_pagination').pagination('options').pageSize;
	}
	try {
		previewAX.StopRealPlayAll();
	} catch (e) {}
	previewAX.HWP_ArrangeWindow(Math.sqrt(pageSize));// 设置分屏
	// 判断当前是否有选中的节点
	var node = $('#menu_tree').tree('getSelected');
	if (!node) {
		return;
	}
	
	// 控制工具栏显示状态
	var tool = $('#div_tool');
	if (tool.is(':hidden')) {
		tool.show();
		$('#div_layout').layout('resize');
	}
	// 调用后台取数
	var url = 'camera/getCameraListByPage';
	var param = {};
	param.stationId = node.stationId;
	param.pageNum = pageNum - 1;
	param.pageSize = pageSize;
	doPost(url, param, function(result, total) {
		// 设置分页
		$('#tool_pagination').pagination({
			total: total,
			pageNumber: pageNum,
			pageSize: pageSize
		});
		for (var i = 0;i < result.length;i ++) {
			var item = result[i];
			if (item.url) {
				previewAX.HWP_Play(item.url, item.password, i, '', '');
			}
		}
	});
}

function loadMenuTree() {
	var url = 'camera/getStationTree';
	doPost(url, function(result, total) {
		if (isEmpty(result)) {
			return;
		}
		// 设置id属性，快速查找用
		for ( var i in result) {
			var item = result[i];
			item.id = item.stationType + '_' + item.stationId;
		}
		var t = $('#menu_tree');
		t.tree('loadData', result);
		// 默认展开第一个节点
		t.tree('expand', t.tree('find', result[0].id).target);
	});
}