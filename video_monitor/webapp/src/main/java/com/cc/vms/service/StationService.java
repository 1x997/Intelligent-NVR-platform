package com.cc.vms.service;

import java.util.List;

import com.alibaba.fastjson.JSONArray;
import com.cc.vms.model.VmsStation;

public interface StationService {

	JSONArray queryStationTree();
	
	List<VmsStation> queryStationLeafList();
	
}
