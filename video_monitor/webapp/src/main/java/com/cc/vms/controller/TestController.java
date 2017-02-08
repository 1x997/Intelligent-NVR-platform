package com.cc.vms.controller;

import javax.annotation.Resource;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import com.cc.vms.model.VmsTestBean;
import com.cc.vms.service.TestService;
import com.cc.vms.utils.JsonWrapper;

@Controller
@RequestMapping("test")
public class TestController {

	private static final Logger log = LoggerFactory.getLogger(TestController.class);

	@Resource
	private TestService testService;

	@RequestMapping("q")
	@ResponseBody
	public JsonWrapper q(@RequestParam("param") String s) {
		VmsTestBean bean = testService.query();
		
		JsonWrapper jsonWrapper = new JsonWrapper();
		jsonWrapper.setResult(bean);
		return jsonWrapper;
	}
	
}
