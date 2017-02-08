package com.cc.vms.utils.exception;


public class RtException extends RuntimeException {

	private static final long serialVersionUID = -4727376093552328314L;

	private int errorCode;

	private String errorMessage;

	public RtException(int errorCode, String errorMessage) {
		super();
		this.errorCode = errorCode;
		this.errorMessage = errorMessage;
	}
	
	public RtException(String errorMessage) {
		super();
		this.errorCode = -1;
		this.errorMessage = errorMessage;
	}
	
	public int getErrorCode() {
		return errorCode;
	}

	public String getErrorMessage() {
		return errorMessage;
	}
	
	@Override
	public String getMessage() {
		return errorMessage;
	}
	
}
