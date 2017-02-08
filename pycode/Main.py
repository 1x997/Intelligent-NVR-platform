# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import SchemeServer
import CameraServer
import CaffeFromMqServer
from multiprocessing import Queue

adjust_scheme = Queue()
action_scheme = Queue()
sche = SchemeServer.c_schemeServer(adjust_scheme,action_scheme)
camera = CameraServer.c_cameraServer(action_scheme)
caffe = CaffeFromMqServer.CaffeFromMqServer(adjust_scheme)
sche.start()
camera.start()
caffe.start()
caffe.join()
sche.join()
camera.join()

   
