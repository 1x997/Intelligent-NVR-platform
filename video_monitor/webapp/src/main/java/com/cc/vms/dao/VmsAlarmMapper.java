package com.cc.vms.dao;

import java.util.List;

import org.apache.ibatis.annotations.Param;

import com.cc.vms.model.VmsAlarm;
import com.cc.vms.model.VmsAlarmSearch;

public interface VmsAlarmMapper {
	
    int deleteByPrimaryKey(Integer alarmId);
    int insertSelective(VmsAlarm record);
    int updateByPrimaryKeySelective(VmsAlarm record);

    VmsAlarm selectByPrimaryKey(Integer alarmId);
	List<VmsAlarm> selectByCondition(@Param("condition") VmsAlarmSearch condition, @Param("offset") int offset, @Param("rows") int rows);
	int countByCondition(@Param("condition") VmsAlarmSearch condition);
	
}