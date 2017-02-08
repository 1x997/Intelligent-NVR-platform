package com.cc.vms.utils;

import java.util.HashMap;
import java.util.Map;

/**
 * 响应适配类
 *
 * @param <T>
 */
public class JsonWrapper<T> {
	public static final int LOGIN_FAIL = -2;
	public static final int CODE_SUCC = 0;
	public static final int CODE_FAIL = -1;

	public static final String CODE_KEY = "status_code";
	public static final String REASON_KEY = "status_reason";

	private Map<String, Object> status = new HashMap<String, Object>();
	private T result; // 结果a
	private Integer total; // 需要分页时，返回列表总数

	public JsonWrapper() {
		status.put(CODE_KEY, CODE_SUCC);
		status.put(REASON_KEY, "");
	}

	public JsonWrapper(int statusCode, String failReason) {
		status.put(CODE_KEY, statusCode);
		status.put(REASON_KEY, failReason);
	}

	public JsonWrapper(String failReason) {
		status.put(CODE_KEY, CODE_FAIL);
		status.put(REASON_KEY, failReason);
	}

	public JsonWrapper(T result) {
		this();
		setResult(result);
	}

	public void setStatus(int statusCode, String statusReason) {
		status.put(CODE_KEY, statusCode);
		status.put(REASON_KEY, statusReason);
	}
	
	public void setSuccessStatus(String statusReason) {
		status.put(CODE_KEY, CODE_SUCC);
		status.put(REASON_KEY, statusReason);
	}

	public void setFailStatus(String statusReason) {
		status.put(CODE_KEY, CODE_FAIL);
		status.put(REASON_KEY, statusReason);
	}

	public Map<String, Object> getStatus() {
		return status;
	}

	public T getResult() {
		return result;
	}

	public void setResult(T result) {
		this.result = result;
	}

	public Integer getTotal() {
		return total;
	}

	public void setTotal(Integer total) {
		this.total = total;
	}

	@Override
	public String toString() {
		return "JsonWrapper{" + "status=" + status + ", result=" + result + ", total=" + total + '}';
	}
}
