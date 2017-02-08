package com.cc.vms.service;

import java.util.List;
import java.util.Map;

import com.alibaba.fastjson.JSONObject;
import com.cc.vms.model.VmsAlarm;
import com.cc.vms.model.VmsAlarmImage;
import com.cc.vms.model.VmsAlarmSearch;

public interface AlarmService {

	List<VmsAlarm> queryAlarmList(VmsAlarmSearch condition, int pageNum, int pageSize);
	int countAlarmList(VmsAlarmSearch condition);
	
	List<VmsAlarmImage> queryAlarmImageList(int alarmId, int pageNum, int pageSize);
	int countAlarmImageList(int alarmId);
	
	Map<Integer, List<VmsAlarmImage>> queryByAlarmIdsLimit3(List<Integer> alarmIdList);
	
	void saveAlarm(JSONObject json);
	
}
