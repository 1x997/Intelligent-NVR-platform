# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import cPickle as pickle
import pika
import logging
import numpy as np
import skimage
import os
import cv2
import sys
import caffe
import time
import copy
from fdfs_client.client import *
from google.protobuf import text_format
from caffe.proto import caffe_pb2
from FunctionAfterCaffe import TaskCollections
from multiprocessing import Process
# def load_image(datas, color=True):
#         """
#         Load an image converting from grayscale or alpha as needed.
# 
#         Parameters
#         ----------
#         filename : string
#         color : boolean
#             flag for color format. True (default) loads as RGB while False
#             loads as intensity (if image is already grayscale).
# 
#         Returns
#         -------
#         image : an image with type np.float32 in range [0, 1]
#             of size (H x W x 3) in RGB or
#             of size (H x W x 1) in grayscale.
#         """
#         img = skimage.img_as_float(datas).astype(np.float32)
#         if img.ndim == 2:
#             img = img[:, :, np.newaxis]
#             if color:
#                 img = np.tile(img, (1, 1, 3))
#         elif img.shape[2] == 4:
#             img = img[:, :, :3]
#         return img
# 
# 
# def caffenet(cameraid,preData,scoremap,methods,transformer,net,functions):
#                 print 'received a message from  %s '%cameraid
#                 nparr = np.fromstring(preData, np.uint8)
#                 img_np = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
#                 image = load_image(img_np)
#                 transformed_image = transformer.preprocess('data', image)
#                 net.blobs['data'].data[...] = transformed_image
#                 detections = net.forward()['detection_out']
#                 returnlist = list()
#                 if(methods == None):
#                     return returnlist
#                 methodslist = methods.slipt(",")
#                 for method in methodslist:
#                     temp_img_np =copy.deepcopy(img_np)
#                     #利用反射功能动态调用
#                     print "反射调用"
#                     func = getattr(functions,method)
#                     returnlist.append(func(cameraid,temp_img_np,detections,image.shape,scoremap))
#                 return returnlist

class CaffenetUsage(Process):
    def __init__(self,request,caffe_root,labelmap_file,model_def,model_weights,image_resize,client_conf):
#        caffe_root = '../caffemodule'  # this file is expected to be in {caffe_root}/examples
        Process.__init__(self)
        self.caffe_root = caffe_root
        self.labelmap_file = labelmap_file
        self.model_def = model_def
        self.model_weights = model_weights
        self.image_resize = image_resize
        self.client_conf = client_conf
        self.request = request
        self.hasinit = False
        
    def initCaffeModule(self):
        os.chdir(self.caffe_root)
        sys.path.insert(0, 'python')
        caffe.set_device(0)
        caffe.set_mode_gpu()
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='allCaffe.log',
                    filemode='w')
#        labelmap_file = '../caffemodule/supervisormodule/labelmap_voc.prototxt'
        file = open(self.labelmap_file, 'r')
        self.labelmap = caffe_pb2.LabelMap()
        text_format.Merge(str(file.read()), self.labelmap)
#        model_def = '../caffemodule/supervisormodule/deploy.prototxt'
#        model_weights = '../caffemodule/supervisormodule/VGG_VOC0712_SSD_300x300_iter_60000.caffemodel'
        self.net = caffe.Net(self.model_def,      # defines the structure of the model
                self.model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)
        # input preprocessing: 'data' is the name of the input blob == net.inputs[0]
        self.transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
        self.transformer.set_transpose('data', (2, 0, 1))
        self.transformer.set_mean('data', np.array([104,117,123])) # mean pixel
        self.transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
        self.transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB
        # set net to batch size of 1
#        image_resize = 300
        self.net.blobs['data'].reshape(1,3,int(self.image_resize),int(self.image_resize))
        self.functions = TaskCollections(self.client_conf)
        
        credentials = pika.PlainCredentials('ye', '123456')
        parameters = pika.ConnectionParameters('192.168.0.23', 5672, '/', credentials)
          #这里要设置重连机制
        counectCounts =0
        while(counectCounts<3):
            try:
                connection = pika.BlockingConnection(parameters)
                counectCounts=3
            except Exception,e:
                time.sleep(1)
                counectCounts +=1
                print "reconnecting..."
        self.channel = connection.channel()
        self.channel.queue_declare(queue='picture_process', durable=True)






    def load_image(self,datas, color=True):
        """
        Load an image converting from grayscale or alpha as needed.
 
        Parameters
        ----------
        filename : string
        color : boolean
            flag for color format. True (default) loads as RGB while False
            loads as intensity (if image is already grayscale).
 
        Returns
        -------
        image : an image with type np.float32 in range [0, 1]
            of size (H x W x 3) in RGB or
            of size (H x W x 1) in grayscale.
        """
        img = skimage.img_as_float(datas).astype(np.float32)
        if img.ndim == 2:
            img = img[:, :, np.newaxis]
            if color:
                img = np.tile(img, (1, 1, 3))
        elif img.shape[2] == 4:
            img = img[:, :, :3]
        return img
 
 
 
 
    #caffe处理
    def caffenet(self,cameraid,preData,scoremap,methods):
                logging.info('received a message from  %s '%cameraid)
                nparr = np.fromstring(preData, np.uint8)
                img_np = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
                image = self.load_image(img_np)
                transformed_image = self.transformer.preprocess('data', image)
                self.net.blobs['data'].data[...] = transformed_image
                detections = self.net.forward()['detection_out']
                returnlist = list()
                if(methods == None):
                    return returnlist
                
    
                if(methods.find(",") != -1):
                    methodslist = methods.slipt(",")
                    for method in methodslist:
                        temp_img_np =copy.deepcopy(img_np)
                        #利用反射功能动态调用
                        func = getattr(self.functions,method)
                        returnlist.append(func(cameraid,temp_img_np,detections,image.shape,scoremap,self.labelmap))
                else:
                    temp_img_np =copy.deepcopy(img_np)
                    func = getattr(self.functions,methods)
                    returnlist.append(func(cameraid,temp_img_np,detections,image.shape,scoremap,self.labelmap))
                    
                return returnlist
    
    def run(self):
        while(1):
            if(self.hasinit == False):
                self.initCaffeModule()
                self.hasinit = True
            contextStruct = self.request.get()
            returnlist = self.caffenet(contextStruct.cameraid, contextStruct.preData, contextStruct.scoremap, contextStruct.methods)
            if(len(returnlist) == 0):
                continue
            for it in returnlist:
                self.channel.basic_publish(exchange='',
                                              routing_key='picture_process',
                                              body=str(it))
                logging.info('send result  %s '%str(it))
               
