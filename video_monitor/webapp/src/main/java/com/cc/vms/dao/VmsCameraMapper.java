package com.cc.vms.dao;

import java.util.List;
import java.util.Set;

import org.apache.ibatis.annotations.Param;

import com.cc.vms.model.VmsCamera;

public interface VmsCameraMapper {
	int deleteByPrimaryKey(Integer cameraId);

	int insertSelective(VmsCamera record);

	VmsCamera selectByPrimaryKey(Integer cameraId);

	List<VmsCamera> selectByStationId(@Param("stationId") int stationId, @Param("offset") Integer offset, @Param("rows") Integer rows);

	int updateByPrimaryKeySelective(VmsCamera record);

	int countByStationId(int stationId);

	List<VmsCamera> selectByCameraIds(@Param("ids") Set<Integer> cameraIdSet);

}