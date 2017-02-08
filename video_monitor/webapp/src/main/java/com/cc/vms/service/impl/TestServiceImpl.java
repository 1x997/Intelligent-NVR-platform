package com.cc.vms.service.impl;

import javax.annotation.PostConstruct;
import javax.annotation.Resource;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.core.AmqpTemplate;
import org.springframework.stereotype.Service;

import com.cc.vms.dao.VmsTestBeanMapper;
import com.cc.vms.model.VmsTestBean;
import com.cc.vms.service.TestService;

@Service
public class TestServiceImpl implements TestService {

	@Resource
	private VmsTestBeanMapper mapper;

	@Override
	public VmsTestBean query() {
		return mapper.selectByPrimaryKey(2);
	}

	private static final Logger log = LoggerFactory.getLogger(TestServiceImpl.class);

	// @Resource
	private AmqpTemplate amqpTemplate;

	public void sendMessage(Object message) {
		log.info("send message:{}", message);
		amqpTemplate.convertAndSend("daiTestQueueKey", message);
	}

	
	// @PostConstruct
	public void test() {
		log.info("dai mq test");
		
		for (int i=0; i < 10; i++) {
			this.sendMessage("dai_" + i);
		}
		
		log.info("dai mq send finish");
	}
	
	
}
