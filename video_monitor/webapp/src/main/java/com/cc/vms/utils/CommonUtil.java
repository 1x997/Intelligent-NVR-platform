package com.cc.vms.utils;

import java.net.URLEncoder;
import java.text.SimpleDateFormat;
import java.util.Date;

import org.apache.commons.lang.StringUtils;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.cc.vms.utils.exception.RtException;

public class CommonUtil {
	
	public static JSONObject trimStringValue(JSONObject json) {
		if (json != null) {
			JSONObject result = new JSONObject();
			for (String key : json.keySet()) {
				Object value = json.get(key);
				if (value != null) {
					if (value instanceof String) {
						value = ((String) value).trim();
					}
					result.put(key, value);
				}
			}
			return result;
		} else {
			return null;
		}
	}
	
	/**
	 * 返回当前日期字符串，如：2015-09-15
	 */
	public static String currentDay() {
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
		return sdf.format(new Date());
	}
	
	/**
	 * 是否json object文本
	 */
	public static boolean isJSONObjectText(String text) {
		if (StringUtils.isNotEmpty(text)) {
			try {
				JSON.parseObject(text);
				return true;
			} catch (Exception e) {
				// do nothing
			}
		}
		return false;
	}
	
	public static String urlEncode(String s) {
		try {
			return URLEncoder.encode(s, "utf-8");
		} catch (Exception e) {
			throw new RtException("urlEncode error: " + e);
		}
		
	}
	
}
