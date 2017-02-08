package com.cc.vms.service;

import java.util.List;
import java.util.Map;
import java.util.Set;

import com.cc.vms.model.VmsCamera;

public interface CameraService {

	List<VmsCamera> queryByStationId(int stationId);
	
	List<VmsCamera> queryByStationId(int stationId, int pageNum, int pageSize);
	
	int countByStationId(int stationId);

	VmsCamera queryByCameraId(int cameraId);

	Map<Integer, VmsCamera> queryByCameraIds(Set<Integer> cameraIdSet);
	
}
