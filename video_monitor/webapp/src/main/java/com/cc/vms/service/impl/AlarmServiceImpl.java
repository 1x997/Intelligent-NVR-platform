package com.cc.vms.service.impl;

import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.annotation.Resource;

import org.springframework.stereotype.Service;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.cc.vms.dao.VmsAlarmImageMapper;
import com.cc.vms.dao.VmsAlarmMapper;
import com.cc.vms.model.VmsAlarm;
import com.cc.vms.model.VmsAlarmImage;
import com.cc.vms.model.VmsAlarmSearch;
import com.cc.vms.model.VmsCamera;
import com.cc.vms.service.AlarmService;
import com.cc.vms.service.CameraService;
import com.cc.vms.utils.exception.RtException;

@Service
public class AlarmServiceImpl implements AlarmService {
	
	@Resource
	private VmsAlarmMapper vmsAlarmMapper;
	
	@Resource
	private VmsAlarmImageMapper vmsAlarmImageMapper;
	
	@Resource
	private CameraService cameraService;

	@Override
	public List<VmsAlarm> queryAlarmList(VmsAlarmSearch condition, int pageNum, int pageSize) {
		int rows = Math.max(pageSize, 1);
		int offset = Math.max(pageNum, 0) * rows;
		return vmsAlarmMapper.selectByCondition(condition, offset, rows);
	}
	
	@Override
	public int countAlarmList(VmsAlarmSearch condition) {
		return vmsAlarmMapper.countByCondition(condition);
	}
	
	@Override
	public List<VmsAlarmImage> queryAlarmImageList(int alarmId, int pageNum, int pageSize) {
		int rows = Math.max(pageSize, 1);
		int offset = Math.max(pageNum, 0) * rows;
		return vmsAlarmImageMapper.selectByAlarmId(alarmId, offset, rows);
	}
	
	@Override
	public int countAlarmImageList(int alarmId) {
		return vmsAlarmImageMapper.countByAlarmId(alarmId);
	}
	
	@Override
	public Map<Integer, List<VmsAlarmImage>> queryByAlarmIdsLimit3(List<Integer> alarmIdList) {
		Map<Integer, List<VmsAlarmImage>> map = new HashMap<>();
		if (alarmIdList != null && alarmIdList.size() > 0) {
			List<VmsAlarmImage> totalList = vmsAlarmImageMapper.selectByAlarmIdsLimit3(alarmIdList);
			for (VmsAlarmImage bean : totalList) {
				List<VmsAlarmImage> list = map.get(bean.getAlarmId());
				if (list == null) {
					list = new ArrayList<>();
					map.put(bean.getAlarmId(), list);
				}
				list.add(bean);
			}
		}
		return map;
	}
	
	@Override
	public void saveAlarm(JSONObject json) {
		/*
{label_list=[{xmin=1137, ymin=232,xmax=1265, ymax=404, score=0.402305,label="person"},
{xmin=386, ymin=200,xmax=587, ymax=357, score=0.917971,label="tvmonitor"}],
img_width=1280, img_height=720, 
img_src="{'Status': 'Upload successed.', 'Storage IP': '192.168.0.23', 'Remote file_id': 'group1/M00/00/0C/wKgAF1h9zhaAXCifAB-kABqOMiw501.jpg', 'Group name': 'group1', 'Local file name': '', 'Uploaded size': '1.00MB'}",
check_type="personAndCar",cameraid="192.168.0.24"}
		 */
		
		Date now = new Date();
		Integer cameraId = 14;
		String checkType = json.getString("check_type");
		
		VmsAlarmSearch cond = new VmsAlarmSearch();
		cond.setCameraId(cameraId);
		cond.setCheckType(checkType);
		cond.setNowTime(now);
		
		VmsAlarm bean = null;
		List<VmsAlarm> list = this.queryAlarmList(cond, 0, 1);
		if (list.isEmpty()) {
			bean = new VmsAlarm();
			bean.setBeginTime(now);
			bean.setEndTime(now);
			
			bean.setCameraId(cameraId);
			bean.setCheckType(checkType);
			
			VmsCamera camera = cameraService.queryByCameraId(cameraId);
			if (camera == null) {
				throw new RtException("camera not exist: " + cameraId);
			}
			
			bean.setStationId(camera.getStationId());
			
			vmsAlarmMapper.insertSelective(bean);
		} else {
			bean = list.get(0);
			// 修改最后时间
			bean.setEndTime(now);
			vmsAlarmMapper.updateByPrimaryKeySelective(bean);
		}
		
		String imageSrc = json.getString("img_src");
		JSONObject imageSrcJson = JSON.parseObject(imageSrc);
		
		VmsAlarmImage image = new VmsAlarmImage();
		image.setAlarmId(bean.getAlarmId());
		image.setExtend(json.toJSONString());
		image.setImageTime(now);
		image.setImageUrl(imageSrcJson.getString("Remote file_id").substring(imageSrcJson.getString("Group name").length())); // 去掉group1
		vmsAlarmImageMapper.insertSelective(image);
	}
	
}
