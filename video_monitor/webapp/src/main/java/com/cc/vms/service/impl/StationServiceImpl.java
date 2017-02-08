package com.cc.vms.service.impl;

import java.util.LinkedHashMap;
import java.util.List;

import javax.annotation.Resource;

import org.springframework.stereotype.Service;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.cc.vms.dao.VmsStationMapper;
import com.cc.vms.model.VmsStation;
import com.cc.vms.service.StationService;

@Service
public class StationServiceImpl implements StationService {
	
	@Resource
	private VmsStationMapper vmsStationMapper;

	@Override
	public JSONArray queryStationTree() {
		List<VmsStation> list = vmsStationMapper.selectAllActive();
		LinkedHashMap<Integer, JSONObject> map = new LinkedHashMap<>();
		
		for (VmsStation bean : list) {
			JSONObject json = new JSONObject();
			json.put("stationId", bean.getStationId());
			json.put("parentId", bean.getParentId());
			json.put("stationName", bean.getStationName());
			json.put("stationType", bean.getStationType());		
			
			// 前端展示成文件夹
			json.put("children", new JSONArray());
			json.put("state", "closed");
			
			map.put(bean.getStationId(), json);
		}
		
		return this.buildTree(map);
	}
	
	@Override
	public List<VmsStation> queryStationLeafList() {
		return vmsStationMapper.selectAllActiveLeaf();
	}
	
	protected JSONArray buildTree(LinkedHashMap<Integer, JSONObject> map) {
		JSONArray root = new JSONArray();
		for (JSONObject item : map.values()) {
			int parentId = item.getIntValue("parentId");
			JSONObject parentItem = map.get(parentId);
			
			if (parentId == 0) {
				// 根
				root.add(item);
			} else if (parentItem != null) {
				// 叶子
				JSONArray children = null;
				if (parentItem.containsKey("children")) {
					children = parentItem.getJSONArray("children");
				} else {
					children = new JSONArray();
					parentItem.put("children", children);
				}
				children.add(item);
			}
		}
		
		return root;
	}

}
