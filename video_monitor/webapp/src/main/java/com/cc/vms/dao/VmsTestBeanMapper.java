package com.cc.vms.dao;

import com.cc.vms.model.VmsTestBean;

public interface VmsTestBeanMapper {
    int deleteByPrimaryKey(Integer id);

    int insert(VmsTestBean record);

    int insertSelective(VmsTestBean record);

    VmsTestBean selectByPrimaryKey(Integer id);

    int updateByPrimaryKeySelective(VmsTestBean record);

    int updateByPrimaryKey(VmsTestBean record);
}