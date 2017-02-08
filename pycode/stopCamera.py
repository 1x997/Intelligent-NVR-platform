# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import commands


        
def stopCamera():
        (status, output) =  commands.getstatusoutput("ps -ef|grep 'CameraCapture' |awk '{print $2}'")
        print output
        for i in output.split('\n'):
            commands.getstatusoutput("kill -9 "+i)
        print (" camera stoped!")


stopCamera()

