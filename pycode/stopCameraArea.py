# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import commands


        
def stopCameraHIK():
        (status, output) =  commands.getstatusoutput("ps -ef|grep './HIKIntrusionFastdfs ' |awk '{print $2}'")
        print output
        for i in output.split('\n'):
            commands.getstatusoutput("kill -9 "+i)
        print (" regInvasion stoped")


stopCameraHIK()

