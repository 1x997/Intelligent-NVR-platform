# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import pika
import json
import time
from multiprocessing import Process, Queue

class c_schemeServer(Process):
    def __init__(self,adjust_scheme,action_scheme):
        Process.__init__(self)
    # 连接 rabbitmq接收 摄像头发来的图片
        credentials = pika.PlainCredentials('ye', '123456')
        parameters = pika.ConnectionParameters('192.168.0.23', 5672, '/', credentials)
            # 监听通道
        counectCounts = 0
        while(counectCounts < 3):
            try:
                connection = pika.BlockingConnection(parameters)
                counectCounts = 3
            except Exception, e:
                time.sleep(1)
                counectCounts += 1
                print "reconnectiong mq ..."
        print(' [*] SchemeProcess Waiting for messages. To exit press CTRL+C')
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange='topic_action2', type='topic')
        result = self.channel.queue_declare(exclusive=True)
        self.queue_name = result.method.queue
        binding_keys = list()
        binding_keys.append("app.*")
        binding_keys.append("camera.*")
        for binding_key in binding_keys:
            self.channel.queue_bind(exchange='topic_action2',
                               queue=self.queue_name,
                               routing_key=binding_key)
        
        self.adjust_scheme = adjust_scheme
        self.action_scheme = action_scheme
            


    def on_request(self, ch, method, props, body):
            if body.strip() == '':
                return None 
            print "receive body %s"%body
            receive = json.loads(body, "utf-8")
            if(receive["action_type"] =="action"):
                self.action_scheme.put(receive["list_action"])
                print "action_scheme put!!"
            elif(receive["action_type"] =="adjust"):
                self.adjust_scheme.put(receive["list_adjust"])
                print "adjust_scheme put!! %s"%receive["list_adjust"]
                
    def run(self):
            self.channel.basic_consume(self.on_request, queue=self.queue_name, no_ack=True)
            self.channel.start_consuming()