package com.cc.vms.service.impl;

import javax.annotation.Resource;

import org.apache.commons.lang.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.core.MessageListener;
import org.springframework.stereotype.Service;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.cc.vms.service.AlarmService;

@Service("queueListener")
public class QueueListener implements MessageListener {
	
	private Logger log = LoggerFactory.getLogger(QueueListener.class);
	
	@Resource
	private AlarmService alarmService;

	@Override
	public void onMessage(Message message) {
		String body = new String(message.getBody());
		
		if (StringUtils.isNotEmpty(body) && !StringUtils.equalsIgnoreCase(body, "None")) {
			try {
				log.info("get msg from mq: {}", body);
				JSONObject json = JSON.parseObject(body);
				alarmService.saveAlarm(json);
			} catch (Exception e) {
				log.error("get msg from mq error: " + e, e);
			}
		} else {
			log.error("msg is empty, body: {}, msg: {}", body, message);
		}
	}

}
