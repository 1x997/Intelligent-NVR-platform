# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import commands

def stopMain():
        (status, output) =  commands.getstatusoutput("ps -ef|grep 'Main.py' |awk '{print $2}'")
        print output
        for i in output.split('\n'):
            commands.getstatusoutput("kill -9 "+i)
        print (" caffeserver stoped!")
        

stopMain()

