package com.cc.vms.service.impl;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import javax.annotation.Resource;

import org.springframework.stereotype.Service;

import com.cc.vms.dao.VmsCameraMapper;
import com.cc.vms.model.VmsCamera;
import com.cc.vms.service.CameraService;

@Service
public class CameraServiceImpl implements CameraService {
	
	@Resource
	private VmsCameraMapper vmsCameraMapper;

	@Override
	public List<VmsCamera> queryByStationId(int stationId) {
		return vmsCameraMapper.selectByStationId(stationId, null, null);
	}
	
	@Override
	public List<VmsCamera> queryByStationId(int stationId, int pageNum, int pageSize) {
		int rows = Math.max(pageSize, 1);
		int offset = Math.max(pageNum, 0) * rows;
		return vmsCameraMapper.selectByStationId(stationId, offset, rows);
	}
	
	@Override
	public int countByStationId(int stationId) {
		return vmsCameraMapper.countByStationId(stationId);
	}
	
	@Override
	public VmsCamera queryByCameraId(int cameraId) {
		return vmsCameraMapper.selectByPrimaryKey(cameraId);
	}
	
	@Override
	public Map<Integer, VmsCamera> queryByCameraIds(Set<Integer> cameraIdSet) {
		Map<Integer, VmsCamera> map = new HashMap<>();
		if (cameraIdSet != null && cameraIdSet.size() > 0) {
			List<VmsCamera> list = vmsCameraMapper.selectByCameraIds(cameraIdSet);
			for (VmsCamera bean : list) {
				map.put(bean.getCameraId(), bean);
			}
		}
		return map;
	}
	
}
