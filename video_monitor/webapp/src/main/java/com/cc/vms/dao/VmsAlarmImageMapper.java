package com.cc.vms.dao;

import java.util.List;

import org.apache.ibatis.annotations.Param;

import com.cc.vms.model.VmsAlarmImage;

public interface VmsAlarmImageMapper {

	int deleteByPrimaryKey(Integer imageId);
    int insertSelective(VmsAlarmImage record);
    int updateByPrimaryKeySelective(VmsAlarmImage record);

    VmsAlarmImage selectByPrimaryKey(Integer imageId);
	List<VmsAlarmImage> selectByAlarmId(@Param("alarmId") int alarmId, @Param("offset") int offset, @Param("rows") int rows);
	int countByAlarmId(@Param("alarmId") int alarmId);

	List<VmsAlarmImage> selectByAlarmIdsLimit3(@Param("ids") List<Integer> alarmIdList);
}
