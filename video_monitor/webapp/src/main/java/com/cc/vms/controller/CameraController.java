package com.cc.vms.controller;

import java.util.ArrayList;
import java.util.List;

import javax.annotation.Resource;

import org.apache.commons.lang.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.cc.vms.model.VmsCamera;
import com.cc.vms.model.VmsStation;
import com.cc.vms.service.CameraService;
import com.cc.vms.service.StationService;
import com.cc.vms.utils.JsonWrapper;

@Controller
@RequestMapping("camera")
public class CameraController {

	private static final Logger log = LoggerFactory.getLogger(CameraController.class);

	@Resource
	private CameraService cameraService;
	
	@Resource
	private StationService stationService;

	@RequestMapping("getStationTree")
	@ResponseBody
	public JsonWrapper getStationTree() {
		JSONArray result = stationService.queryStationTree();
		JsonWrapper jsonWrapper = new JsonWrapper();
		jsonWrapper.setResult(result);
		return jsonWrapper;
	}
	
	@RequestMapping("getStationList")
	@ResponseBody
	public JsonWrapper getStationList() {
		List<VmsStation> list = stationService.queryStationLeafList();
		JSONArray result = new JSONArray();
		
		for (VmsStation bean : list) {
			JSONObject json = new JSONObject();
			json.put("stationId", bean.getStationId());
			json.put("stationName", bean.getStationName());
			result.add(json);
		}
		
		JsonWrapper jsonWrapper = new JsonWrapper();
		jsonWrapper.setResult(result);
		jsonWrapper.setTotal(result.size());
		return jsonWrapper;
	}
	
	@RequestMapping("getCameraList")
	@ResponseBody
	public JsonWrapper getCameraList(@RequestParam("param") String s) {
		JSONObject param = JSON.parseObject(s);
		int stationId = param.getIntValue("stationId");
		
		List<VmsCamera> list = cameraService.queryByStationId(stationId);
		JSONArray result = new JSONArray();
		for (VmsCamera bean : list) {
			JSONObject json = new JSONObject();
			json.put("cameraId", bean.getCameraId());
			json.put("cameraName", bean.getCameraName());

			result.add(json);
		}
		
		JsonWrapper jsonWrapper = new JsonWrapper();
		jsonWrapper.setResult(result);
		jsonWrapper.setTotal(result.size());
		return jsonWrapper;
	}
	
	@RequestMapping("getCameraListByPage")
	@ResponseBody
	public JsonWrapper getCameraListByPage(@RequestParam("param") String s) {
		JSONObject param = JSON.parseObject(s);
		
		JsonWrapper jsonWrapper = new JsonWrapper();
		JSONArray result = new JSONArray();
		jsonWrapper.setResult(result);
		
		List<VmsCamera> list = null;
		int cameraId = param.getIntValue("cameraId");
		if (cameraId > 0) {
			// 单个摄像头
			list = new ArrayList<>();
			VmsCamera bean = cameraService.queryByCameraId(cameraId);
			if (bean != null) {
				list.add(bean);
			}
			jsonWrapper.setTotal(list.size());
		} else {
			// 变电站，多个摄像头分屏
			int stationId = param.getIntValue("stationId");
			int pageNum = param.getIntValue("pageNum");
			int pageSize = param.getIntValue("pageSize");
			
			list = cameraService.queryByStationId(stationId, pageNum, pageSize);
			
			int count = cameraService.countByStationId(stationId);
			jsonWrapper.setTotal(count);
		}
		
		
		for (VmsCamera bean : list) {
			JSONObject json = new JSONObject();
			json.put("cameraId", bean.getCameraId());
			json.put("cameraName", bean.getCameraName());
			
			if (StringUtils.isNotEmpty(bean.getExtend())) {
				JSONObject extend = JSON.parseObject(bean.getExtend());
				if (cameraId > 0) {
					// 单个摄像头，使用主码流
					json.put("url", extend.getString("urlMain"));
				} else {
					// 多个摄像头，使用子码流
					json.put("url", extend.getString("urlSon"));
				}
				json.put("password", extend.getString("password"));
			}
			
			result.add(json);
		}
		
		return jsonWrapper;
	}
	
}
