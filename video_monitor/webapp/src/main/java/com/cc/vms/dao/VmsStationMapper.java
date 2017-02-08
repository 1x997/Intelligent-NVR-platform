package com.cc.vms.dao;

import java.util.List;

import com.cc.vms.model.VmsStation;

public interface VmsStationMapper {
    int deleteByPrimaryKey(Integer stationId);

    int insertSelective(VmsStation record);

    VmsStation selectByPrimaryKey(Integer stationId);
    List<VmsStation> selectAllActive();
    List<VmsStation> selectAllActiveLeaf();

    int updateByPrimaryKeySelective(VmsStation record);


}