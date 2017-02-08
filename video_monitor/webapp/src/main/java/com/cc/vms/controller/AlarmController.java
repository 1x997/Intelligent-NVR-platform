package com.cc.vms.controller;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import javax.annotation.Resource;

import org.apache.commons.lang.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.cc.vms.model.VmsAlarm;
import com.cc.vms.model.VmsAlarmImage;
import com.cc.vms.model.VmsAlarmSearch;
import com.cc.vms.model.VmsCamera;
import com.cc.vms.service.AlarmService;
import com.cc.vms.service.CameraService;
import com.cc.vms.utils.JsonWrapper;
import com.cc.vms.utils.exception.RtException;

@Controller
@RequestMapping("alarm")
public class AlarmController {

	private static final Logger log = LoggerFactory.getLogger(AlarmController.class);
	
	@Value("#{urlConfigProperties['image.url.prefix']}")
	private String imageUrlPrefix;

	@Resource
	private AlarmService alarmService;
	
	@Resource
	private CameraService cameraService;
	
	@RequestMapping("getAlarmList")
	@ResponseBody
	public JsonWrapper getAlarmList(@RequestParam("param") String s) throws ParseException {
		JSONObject param = JSON.parseObject(s);
		VmsAlarmSearch condition = this.parseCondition(param);
		int pageNum = param.getIntValue("pageNum");
		int pageSize = param.getIntValue("pageSize");
		
		List<VmsAlarm> list = alarmService.queryAlarmList(condition, pageNum, pageSize);
		Set<Integer> cameraIdSet = new HashSet<>();
		List<Integer> alarmIdList = new ArrayList<>();
		for (VmsAlarm bean : list) {
			cameraIdSet.add(bean.getCameraId());
			alarmIdList.add(bean.getAlarmId());
		}
		Map<Integer, VmsCamera> cameraMap = cameraService.queryByCameraIds(cameraIdSet);
		Map<Integer, List<VmsAlarmImage>> imageListMap = alarmService.queryByAlarmIdsLimit3(alarmIdList);
		
		
		JSONArray result = new JSONArray();
		for (VmsAlarm bean : list) {
			JSONObject json = new JSONObject();
			
			json.put("alarmId", bean.getAlarmId());
			
			Integer cameraId = bean.getCameraId();
			VmsCamera camera = cameraMap.get(cameraId);
			String cameraName = camera != null ? camera.getCameraName() : "";
			json.put("cameraId", cameraId);
			json.put("cameraName", cameraName);
			
			json.put("checkType", bean.getCheckType());
			json.put("beginTime", bean.getBeginTime());
			json.put("endTime", bean.getEndTime());
			
			List<VmsAlarmImage> imageList = imageListMap.get(bean.getAlarmId());
			JSONArray images = new JSONArray();
			if (imageList != null) {
				for (VmsAlarmImage image : imageList) {
					if (StringUtils.isNotEmpty(image.getImageUrl())) {
						images.add(imageUrlPrefix+ image.getImageUrl());
					}
				}
			}
			json.put("images", images);

			result.add(json);
		}
		int count = alarmService.countAlarmList(condition);
		
		JsonWrapper jsonWrapper = new JsonWrapper();
		jsonWrapper.setResult(result);
		jsonWrapper.setTotal(count);
		return jsonWrapper;
	}
	
	private VmsAlarmSearch parseCondition(JSONObject param) throws ParseException {
		VmsAlarmSearch condition = new VmsAlarmSearch();
		
		int stationId = param.getIntValue("stationId");
		if (stationId <= 0) {
			throw new RtException("变电站是必须的");
		}
		Integer cameraId = param.getInteger("cameraId");
		String checkType = param.getString("checkType");
		condition.setStationId(stationId);
		condition.setCameraId(cameraId);
		condition.setCheckType(checkType);
		
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
		String beginTimeStr = StringUtils.trimToNull(param.getString("beginTime"));
		String endTimeStr = StringUtils.trimToNull(param.getString("endTime"));
		if (StringUtils.isNotEmpty(beginTimeStr)) {
			Date beginTime = sdf.parse(beginTimeStr);
			condition.setBeginTime(beginTime);
		}
		if (StringUtils.isNotEmpty(endTimeStr)) {
			Date endTime = sdf.parse(endTimeStr);
			condition.setEndTime(endTime);
		}
		
		return condition;
	}
	
	@RequestMapping("getAlarmImageList")
	@ResponseBody
	public JsonWrapper getAlarmImageList(@RequestParam("param") String s) throws ParseException {
		JSONObject param = JSON.parseObject(s);
		int alarmId = param.getIntValue("alarmId");
		if (alarmId <= 0) {
			throw new RtException("alarmId是必须的");
		}
		int pageNum = param.getIntValue("pageNum");
		int pageSize = param.getIntValue("pageSize");
		
		List<VmsAlarmImage> list = alarmService.queryAlarmImageList(alarmId, pageNum, pageSize);
		JSONArray result = new JSONArray();
		for (VmsAlarmImage bean : list) {
			JSONObject json = new JSONObject();
			
			json.put("imageId", bean.getImageId());
			json.put("imageTime", bean.getImageTime());
			json.put("imageUrl", imageUrlPrefix + bean.getImageUrl());

			result.add(json);
		}
		int count = alarmService.countAlarmImageList(alarmId);
		
		JsonWrapper jsonWrapper = new JsonWrapper();
		jsonWrapper.setResult(result);
		jsonWrapper.setTotal(count);
		return jsonWrapper;
	}
	
}
