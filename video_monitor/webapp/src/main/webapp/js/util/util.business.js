/**
 * 一些通用的方法，基于Easyui
 */

/**
 * 初始化支持分页的datagrid
 * @param gridId	要创建的datagrid的ID
 * @param param		创建datagrid需要的参数，参考$('').datagrid({});
 * @param url		分页需要的加载数据的接口地址
 * @param funParam 分页加载数据方法需要的额外参数
 */
function dataGridWithPager(gridId, url, param, funParam) {
	if ($.isFunction(param)) {
		onSuccess = param;
		param = undefined;
	}
	var defaultParam = {
			pagination: true,
			pageList: [20, 50, 100, 200],
			pageSize: 20
		};
	if (!isNull(param)) {
		$.each(param, function(n, value){
			defaultParam[n] = value;
		});
	}
	dataGrid(gridId, defaultParam);
	
	var p = $("#" + gridId).datagrid('getPager');
	p.pagination({
		onSelectPage : function(pageNum, pageSize) {
			loadDataForPager(url, gridId, funParam);
		}
	});
	// 初始化后，默认调用一次
	loadDataForPager(url, gridId, funParam);
}
/**
 * 初始化普通的datagrid
 * @param gridId	要创建的datagrid的ID
 * @param param		创建datagrid需要的参数，参考$('').datagrid({});
 */
function dataGrid(gridId, param) {
	var defaultParam = {
			width : '100%',
			height: 'auto',
			singleSelect : true,// 单选
			striped : true,// 奇偶行颜色不同
			collapsible : false,// 可折叠
			rownumbers : true,// 显示行号
			remoteSort : false,// 服务器端排序
			fitColumns: true
		};
	if (!isNull(param)) {
		$.each(param, function(n, value){
			defaultParam[n] = value;
		});
	}
	$('#' + gridId).datagrid(defaultParam);
}

/**
 * 初始化树形结构的treegrid
 * @param gridId	要创建的treegrid的ID
 * @param param		创建treegrid需要的参数，参考$('').treegrid({});
 */
function treeGrid(gridId, param) {
	var defaultParam = {
			width : '100%',
			height: 'auto',
			singleSelect : true,// 单选
			striped : true,// 奇偶行颜色不同
			collapsible : false,// 可折叠
			rownumbers : true,// 显示行号
			remoteSort : false,// 服务器端排序
			fitColumns: false
		};
	if (!isNull(param)) {
		$.each(param, function(n, value){
			defaultParam[n] = value;
		});
	}
	$('#' + gridId).treegrid(defaultParam);
}

/**
 * 通用的加载数据的方法
 * @param url		接口地址
 * @param gridId	datagrid的ID
 * @param param		接口调用的附加参数
 */
function loadDataForPager(url, gridId, param) {
	var p = $("#" + gridId).datagrid('getPager');
	var pageNum = p.pagination('options').pageNumber;
	var pageSize = p.pagination('options').pageSize;
	if (isNull(param)) {
		param = {};
	}
	param.pageNum = Number(pageNum) - 1;
	param.pageSize = pageSize;
	doPost(url, param, 
			function(result, total) {
				$('#' + gridId).datagrid('loadData', result);
				p.pagination('refresh',{total:total, pageNumber: pageNum});
				// 加载后修改Dom，翻页时，让序号列累加显示
				var trs = $('#' + gridId).parent().find('.datagrid-btable:first tr');
				for (var i = 0;i < trs.length;i ++) {
					$(trs[i]).find('td:first div').html((Number(pageNum) - 1) * Number(pageSize) + i + 1);
				}
	});
}

/**
 * 刷新指定行
 * @param gridId
 * @param row
 * @param editable
 */
function refreshRow(gridId, row, editable) {
	var index = $("#" + gridId).datagrid('getRowIndex', row);
	$("#" + gridId).datagrid('refreshRow', index);
	// 可编辑，重新启用编辑
	if (editable) {
		// 需要先结束编辑，再开启编辑，才有效
		$('#' + gridId).datagrid('endEdit', index);
		$('#' + gridId).datagrid('beginEdit', index);
	}
}

/**
 * 更新当前选中的行
 * @param gridId
 * @param row
 * @param editable
 */
function updateSelectedRow(gridId, data) {
	var row = $("#" + gridId).datagrid('getSelected');
	if (isNotNull(row)) {
		var index = $("#" + gridId).datagrid('getRowIndex', row);
		$("#" + gridId).datagrid('updateRow', {index:index, row:data});
	}
}

//参列表点击行后编辑
function clickRowHandlerForEdit(index, gridId) {
	var editIndex = $('#' + gridId).datagrid('options').editIndex;
	if (isNotNull(editIndex)) {
		$('#' + gridId).datagrid('endEdit', editIndex);
	}
	$('#' + gridId).datagrid('beginEdit', index);
	// 记录编辑行的索引
	$('#' + gridId).datagrid('options').editIndex = index;
}

// 根据显示类型的编号，返回显示类型的名称
function getDisplayType(value) {
	for (var i in data_display_type) {
		var item = data_display_type[i];
		if (item.value == value) {
			return item.label;
		}
	}
}
// 表格数据上移
function moveUp(gridId) {
	var row = $('#' + gridId).datagrid('getSelected');
	if (isEmpty(row)) {
		showInfo('请选中一条记录！');
		return;
	}
	var index = $('#' + gridId).datagrid('getRowIndex', row);
	if (index <= 0) {
		return;
	}
	$('#' + gridId).datagrid('deleteRow', index);
	$('#' + gridId).datagrid('insertRow', {index:index - 1, row:row});
	$('#' + gridId).datagrid('selectRow', index - 1);
	
//	$(".table_button").linkbutton({height:20});
}
//表格数据下移
function moveDown(gridId) {
	var row = $('#' + gridId).datagrid('getSelected');
	if (isEmpty(row)) {
		showInfo('请选中一条记录！');
		return;
	}
	var index = $('#' + gridId).datagrid('getRowIndex', row);
	var rows = $('#' + gridId).datagrid('getRows');
	if (index >= rows.length - 1) {
		return;
	}
	$('#' + gridId).datagrid('insertRow', {index:index + 2, row:row});
	$('#' + gridId).datagrid('deleteRow', index);
	$('#' + gridId).datagrid('selectRow', index + 1);
	
//	$(".table_button").linkbutton({height:20});
}
// 计算字段界面
function editCalculateFields(dataSetCode, dialogId, gridId, areaId) {
	$('#' + dialogId).show();
	$('#' + dialogId).dialog({
		title: '计算字段',
		modal: true,
		width: $(window).width() * 0.6,
		height: $(window).height() * 0.6,
		buttons: [{
			text: '保存',
			handler: function() {
				var url = 'dataManage/saveCalcFieldList';
				var param = {dataSetCode:dataSetCode};
				if (isNotEmpty(areaId)) {
					param.areaId = areaId;
				}
				var rows = $('#' + gridId).datagrid('getRows');
				if (isNotEmpty(rows)) {
					for (var i = 0;i < rows.length;i ++) {
						var item = rows[i];
						if (isEmpty(item.fieldName)) {
							showInfo('字段名不能为空！');
							return;
						}
						if (isEmpty(item.precision)) {
							showInfo('精度不能为空！');
							return;
						}
						if (isEmpty(item.formula)) {
							showInfo('公式不能为空！');
							return;
						}
					}
				}
				param.list = rows;
				doPost(url, param, function(result, total){
					showSuccess('保存成功！');
					$('#' + dialogId).dialog('close');
				});
			}
		},{
			text: '关闭',
			handler: function() {
				$('#' + dialogId).dialog('close');
			}
		}],
		onOpen: function() {
			if (isEmpty($('#' + gridId).attr('class'))) {
				var columns = [{
					title : '字段名',
					width : '100',
					field : 'fieldName',
					editor : {
						type : 'textbox',
						options:{
							onChange: function(newValue,oldValue){
								var row = $('#' + gridId).datagrid('getSelected');
								row.fieldName = newValue;
							}
						}
					}
				},{
					title : '精度',
					width : '100',
					field : 'precision',
					editor : {
						type : 'numberbox',
						min : 0,
						options:{
							onChange: function(newValue,oldValue){
								var row = $('#' + gridId).datagrid('getSelected');
								row.precision = newValue;
							}
						}
					}
				},{
					title : '公式',
					width : '350',
					field : 'formula',
					editor : {
						type : 'textbox',
						options:{
							onChange: function(newValue,oldValue){
								var row = $('#' + gridId).datagrid('getSelected');
								row.formula = newValue;
							}
						}
					}
				}];
				// 初始化列表
				dataGrid(gridId, {
					fit: true,
					columns: [columns],
					toolbar: [{
						text: '新增',
						handler: function(){
							var rows = $('#' + gridId).datagrid('getRows');
							$('#' + gridId).datagrid('appendRow',{
								fieldName: '字段' + rows.length,
								precision: 0,
								formula: ''
							});
						}
					},'-',{
						text: '删除',
						handler: function(){
							var row = $('#' + gridId).datagrid('getSelected');
							if (isNull(row)) {
								showInfo('请选择数据！');
								return;
							}
							deleteConfirm(function(){
								var index = $('#' + gridId).datagrid('getRowIndex', row);
								$('#' + gridId).datagrid('deleteRow', index);
							});
						}
					},'-',{
						text: '上移',
						handler: function(){
							moveUp(gridId);
						}
					},'-',{
						text: '下移',
						handler: function(){
							moveDown(gridId);
						}
					}],
					onClickRow:function(rowIndex, rowData){
						clickRowHandlerForEdit(rowIndex, 'calculate_fields_grid');
					}
				});
			}
			var url = 'dataManage/getCalcFieldList';
			var param = {dataSetCode:dataSetCode};
			if (isNotEmpty(areaId)) {
				param.areaId = areaId;
			}
			doPost(url, param, function(result, total){
				$('#' + gridId).datagrid('loadData', result);
			});
		}
	});
}