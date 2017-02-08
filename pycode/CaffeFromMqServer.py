# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import pika
import logging
import CaffeModule
import time
import multiprocessing
from multiprocessing import Process
import Queue
import random
try: 
  import xml.etree.cElementTree as ET 
except ImportError: 
  import xml.etree.ElementTree as ET
  
class ContextStructure:
    def __init__(self,cameraid,preData,scoremap,methods):
        self.cameraid = cameraid
        self.preData = preData
        self.scoremap = scoremap
        self.methods = methods
  
class ModuleStructure:
     def __init__(self,requestlist,modulename,caffe_root,labelmap_file,model_def,model_weights,image_resize,client_file,num,method,caffelist):
        self.modulename = modulename
        self.caffe_root = caffe_root 
        self.labelmap_file = labelmap_file
        self.model_def = model_def
        self.model_weights = model_weights
        self.client_file = client_file
        self.method = method
        self.image_resize = image_resize
        self.num = num
        self.requestlist = requestlist
        self.caffelist =caffelist 
    

 # this file is expected to be in {caffe_root}/examples
class CaffeFromMqServer(Process):
    #一个camera对应多个module或则多个function,list_threshold应该是所有得分配置的集合
    ipScoreMap = dict()
    moduleFunctionMap = dict()
    ipCheckTypeMap = dict()
    #处理任务进程池,默认10个
    pool = None
    
    def __init__(self, cameraScheme):
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
                print "reconnectiong mq"
        self.channel = connection.channel()
        self.scoremap = cameraScheme
        self.flags = False
        self.timegrep = time.time()
        self.channel.queue_declare(queue='q2', durable=False)
            

    def initCaffe(self):
        tree = ET.parse("moduleFunctionMap.xml")     #打开xml文档 
          #root = ET.fromstring(country_string) #从字符串传递xml 
        root = tree.getroot()         #获得root节点  
        for country in root.findall('module'): #找到root节点下的所有module节点 
            modulename = country.get('name')
            caffe_root = country.find('caffe_root').text    
            labelmap_file = country.find('labelmap_file').text
            model_def = country.find('model_def').text
            model_weights = country.find('model_weights').text
            client_file = country.find('client_file').text
            image_resize = country.find('image_resize').text
            method = country.find('method').text
            num = country.find('num').text
            print num
            templist = list()
            requestlist = list()
            for i in range(int(num)):
                request = multiprocessing.Queue()
                caffeModule = CaffeModule.CaffenetUsage(request,caffe_root,labelmap_file,model_def,model_weights,image_resize,client_file)
                caffeModule.start()
                templist.append(caffeModule)
                requestlist.append(request)
                
            moduleStructure = ModuleStructure(requestlist,modulename,caffe_root,labelmap_file,model_def,model_weights,image_resize,client_file,num,method,templist)
            self.moduleFunctionMap[modulename] = moduleStructure
            
            
            
            
        
    #传入的是cameraip,checktype  根据这些找对应的module
    def matchModule(self,typestring):
#        types = typestring.split(',')
        #需要调用的模型列表
        modulelist = list()
        #ip可能只要处理一个function 但module实际可以处理多个function
        #根据ip的配置，过滤下获得实际这个module要处理的function，
        realmoduleFunctionMap = dict()
        for typ in typestring:
            for item in  self.moduleFunctionMap:
                if(self.moduleFunctionMap[item].method.find(typ)!= -1):
                    modulelist.append(item)
                    if(realmoduleFunctionMap.has_key(item)):  
                        realmoduleFunctionMap[item] = "%s,%s"%(realmoduleFunctionMap[item],typ)
                    else:
                        realmoduleFunctionMap[item] = typ   
        return set(modulelist),realmoduleFunctionMap
    


    def on_request(self, ch, method, props, body):
            print props
            print "received!!"
            if body.strip() == '':
                return None
            #每5秒检查一次            
            if(time.time() - self.timegrep >5 or self.flags == False):
                print "checkk!!"
                self.checkCameraScheme()
                self.timegrep = time.time()
                self.flags == True
            #caffe初始化
            if(len(self.moduleFunctionMap)==0):
                self.initCaffe()
            if(self.pool == None):
                self.pool = multiprocessing.Pool(processes=2)
            splitedmsg = body.split('*', 1)
            preData = splitedmsg[1]
            cameraid = splitedmsg[0]
            print "cameraid is %s"%cameraid
            modulelist,realmoduleFunctionMap = self.matchModule(self.ipCheckTypeMap[cameraid])
            print realmoduleFunctionMap
            result = list()
            
            
            for module in modulelist:
                num = self.moduleFunctionMap[module].num
                #module load balance,default using random
                requestqueue = self.moduleFunctionMap[module].requestlist[int(random.random()*100)%int(num)]
                requestContext = ContextStructure(cameraid,preData,self.ipScoreMap[cameraid],realmoduleFunctionMap[module]);
                requestqueue.put(requestContext)
                #多进程处理请求，上面确认module后就开多进程处理任务
                #发送图

            ch.basic_ack(delivery_tag=method.delivery_tag)
                    
                    
            

        
# 不是每张图片来了都检测这个配置 而是 每隔 几秒检测一次   
    def checkCameraScheme(self):
        #默认get()是block的  get(False)非block
        if(len(self.ipCheckTypeMap) == 0):
            scheme = self.scoremap.get()
            print "get adjust_scheme!!!!!"
        else:
            try:
                    scheme = self.scoremap.get(False)
                    print "get adjust_scheme!!!!!"
            except Queue.Empty:
                    print " adjust scheme empty"
                    return          
        #初始化则要 block获取
        for item in scheme:
            self.ipScoreMap[item["data_ip"]] = item["list_threshold"]
            if(len(item["check_type"])>0):
                self.ipCheckTypeMap[item["data_ip"]] = item["check_type"]
        
         

                                               
    def run(self):
            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(self.on_request, queue='q2')
            self.channel.start_consuming()

  
   
