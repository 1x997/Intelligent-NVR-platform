package com.cc.vms.utils;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

import org.codehaus.jackson.JsonGenerator;
import org.codehaus.jackson.JsonProcessingException;
import org.codehaus.jackson.map.JsonSerializer;
import org.codehaus.jackson.map.ObjectMapper;
import org.codehaus.jackson.map.SerializerProvider;
import org.codehaus.jackson.map.ser.CustomSerializerFactory;

public class CustomObjectMapper extends ObjectMapper {
	
	public CustomObjectMapper(){
		CustomSerializerFactory factory = new CustomSerializerFactory();
		factory.addGenericMapping(Date.class, new JsonSerializer<Date>(){
			@Override
			public void serialize(Date value, 
					JsonGenerator jsonGenerator, 
					SerializerProvider provider)
					throws IOException, JsonProcessingException {
				if (value instanceof java.sql.Date) {
					// sdf线程不安全，需要每次实例化，或者可以用ThreadLocal的方式
					SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
					jsonGenerator.writeString(sdf.format(value));
				} else {
					SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
					jsonGenerator.writeString(sdf.format(value));
				}
			}
		});
		this.setSerializerFactory(factory);
	}
	
}