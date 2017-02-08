# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import json
import commands
import os
import time
import Queue
from multiprocessing import Process

 # this file is expected to be in {caffe_root}/examples
class c_cameraServer(Process):
    def __init__(self,action_scheme):
        Process.__init__(self)
        self.action_scheme = action_scheme
        self.current_status = dict()


    def startCamera(self,ip, user, passes, port, grep,root):
        preexename = "cd ../ccode  \n"
        preexename = preexename +"./CameraCapture  %s %s %s %s %s %s %s %s  >camerafirst.out 2>&1 &  "%(str(ip),str(port),user,str(passes),"1",str(grep),"1",root)
        tempname = ip+str(time.time())
        preexename = 'echo  "%s" >> %s.sh'%(preexename,tempname)
        commands.getstatusoutput(preexename)
        exename = "nohup sh  %s.sh >camerastart.out 2>&1 & "%tempname
        os.popen(exename)
        commands.getstatusoutput("rm -rf %s.sh"%tempname)
        print (exename)
        
    def startCameraRegionalInvasion(self,mquri,ip, user, passes,grep, port,staytime,sensitivity,arearait,arearule):
        preexename = "cd ../HIKIntrusion  \n"
#        ye:123456@192.168.0.23:5672// 192.168.0.64 admin dsj-123456 10 8000 1 99 2 0.4,0.4//0.8,0.4//0.8,0.8//0.4,0.8
        preexename = preexename +"./HIKIntrusionClassPacking %s %s %s %s %s %s %s %s %s %s  >cameraRegInvasion.out 2>&1 &"%(mquri,str(ip), user, passes,str(grep), str(port),str(staytime),str(sensitivity),str(arearait),str(arearule))
        tempname = "regInvasion"+ip+str(time.time())
        preexename = 'echo  "%s" >> %s.sh'%(preexename,tempname)
        commands.getstatusoutput(preexename)
        exename = "nohup sh  %s.sh > HIKIntrusion.out 2>&1 & "%(tempname)
        os.popen(exename)
        commands.getstatusoutput("rm -rf %s.sh"%tempname)
        print exename
        
    def stopCameraRegionalInvasion(self,mquri,ip):
        (status, output) =  commands.getstatusoutput("./HIKIntrusionClassPacking %s %s' |awk '{print $2}'"%(mquri,ip))
        print output
        for i in output.split('\n'):
            commands.getstatusoutput("kill -9 "+i)
        print (" regInvasion stoped:%s" % ip)

    def stopCamera(self,ip):
        (status, output) =  commands.getstatusoutput("ps -ef|grep './CameraCapture %s' |awk '{print $2}'"%ip)
        print output
        for i in output.split('\n'):
            commands.getstatusoutput("kill -9 "+i)
        print (" camera stoped:%s" % ip)
    
    # 每隔 几秒检测一次   
    def checkCameraOnOff(self):
        #默认get()是block的  get(False)非block
        if(len(self.current_status) == 0):
            scheme = self.action_scheme.get()
            print "get action_scheme!!!!!"
        else:
            try:
                scheme = self.action_scheme.get(False)
            except Queue.Empty:
                print "scheme empty"
                return
        #初始化则要 block获取
        for item in scheme:
            if(self.current_status.has_key(item["data_ip"])):
                if(self.current_status[item["data_ip"]] == item):
                    continue
                else:
                    if(self.current_status[item["data_ip"]]["active"] == "N" and item["active"]=="F"):
                        self.stopCamera(item["data_ip"])
                        self.stopCameraRegionalInvasion(item["mq_uri"],item["data_ip"])
                    elif(self.current_status[item["data_ip"]]["active"] == "F" and item["active"] == "N"):
                        self.stopCamera(item["data_ip"])
                        self.startCamera(item["data_ip"],item["data_user"],item["data_pass"], item["data_port"], item["data_grap"], None)
                        self.stopCameraRegionalInvasion(item["mq_uri"],item["data_ip"])
                        if(item["reg_active"] == "N"):
                            self.startCameraRegionalInvasion(item["mq_uri"], item["data_ip"],item["data_user"],item["data_pass"],  item["reg_grep"], item["data_port"], item["reg_staytime"], item["reg_sensitivity"], item["reg_arearatio"], item["reg_arearule"])               
                    elif(self.current_status[item["data_ip"]]["active"] == "N" and item["active"] == "N"):
                        self.stopCamera(item["data_ip"])
                        self.startCamera(item["data_ip"],item["data_user"],item["data_pass"], item["data_port"], item["data_grap"], None)  
                        self.stopCameraRegionalInvasion(item["mq_uri"],item["data_ip"])
                        if(item["reg_active"] == "N"):
                            self.startCameraRegionalInvasion(item["mq_uri"], item["data_ip"],item["data_user"],item["data_pass"],  item["reg_grep"], item["data_port"], item["reg_staytime"], item["reg_sensitivity"], item["reg_arearatio"], item["reg_arearule"])                                              
                    self.current_status[item["data_ip"]] =  item
            else:
                if(item["active"] == "F"):
                    self.current_status[item["data_ip"]] =  item
                else:
                    self.current_status[item["data_ip"]] =  item
                    self.stopCamera(item["data_ip"])
                    self.startCamera(item["data_ip"],item["data_user"],item["data_pass"], item["data_port"], item["data_grap"], None)
                    self.stopCameraRegionalInvasion(item["mq_uri"],item["data_ip"])
                    if(item["reg_active"] == "N"):
                        self.startCameraRegionalInvasion(item["mq_uri"], item["data_ip"],item["data_user"],item["data_pass"],  item["reg_grep"], item["data_port"], item["reg_staytime"], item["reg_sensitivity"], item["reg_arearatio"], item["reg_arearule"])               
            
    def run(self):
        while(1):
            self.checkCameraOnOff()
            time.sleep(5)
        