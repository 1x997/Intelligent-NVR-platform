# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import logging
import cv2
from fdfs_client.client import *
import RectangROI

class TaskCollections:
    def __init__(self,client_file):
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='allCaffe.log',
                    filemode='w')
#        client_file='/etc/fdfs/client.conf'
        self.fileclient = Fdfs_client(client_file)
        self.ROI = RectangROI.RectangleIntersect()

    def get_labelname(self,labelmap, labels):
        num_labels = len(labelmap.item)
        labelnames = []
        if type(labels) is not list:
            labels = [labels]
        for label in labels:
            found = False
            for i in xrange(0, num_labels):
                if label == labelmap.item[i].label:
                    found = True
                    labelnames.append(labelmap.item[i].display_name)
                    break
            assert found == True
        return labelnames

    def filterScore(self,scoremap,typekey,score):
        logging.info("scoremap is :%s" %scoremap)
        if(len(scoremap)==0):
            return True
        print typekey
        print score 
        for item in scoremap:
            if(item["alg_classid"] == typekey and float(item["threshold"])<= float(score)):
                return True
        return False
#画框框 并保存
    def drewRectangleAndSave(self,xmin,xmax,ymin,ymax,imagedata):
        for i in range(len(xmin)):
            cv2.rectangle(imagedata,(xmin[i],ymin[i]),(xmax[i],ymax[i]),(0,0,255),1)
        r, buf = cv2.imencode(".jpg",imagedata)           
        return self.upbuffer_func(bytearray(buf))
            
    def upbuffer_func(self,fileBuffer):
        meta_buffer = {
            'ext_name' : 'jpg',
        }
        try:
            ret_dict = self.fileclient.upload_by_buffer(fileBuffer, "jpg", meta_buffer)
            return ret_dict
        except (ConnectionError, ResponseError, DataError), e:
            print e
        return None
    
#返回的是没带帽子人的坐标       
    def checkhat(self,hats,mans):
        nohat = list()
        for man in mans:
#            print "man left %d  ritht %d top %d bottom %d"%(man.left,man.right,man.top,man.bottom)
            rait = 0.0
            for hat in hats:
#                print "hat left %d  ritht %d top %d bottom %d"%(hat.left,hat.right,hat.top,hat.bottom)
                rait = self.ROI.getROI(man, hat)
#                print "%f"%rait
                if(rait >=0.5):
#                    print "break"
                    break
             
            if(rait < 0.5):
                nohat.append(man)
        
        return nohat   
    #图片后处理
    def personAndCar(self,cameraid,img_np,detections,imgshape,scoremap,labelmap):
                returnMessage = "{label_list:["
                needsend= False
                det_label = detections[0,0,:,1]
                det_conf = detections[0,0,:,2]
                det_xmin = detections[0,0,:,3]
                det_ymin = detections[0,0,:,4]
                det_xmax = detections[0,0,:,5]
                det_ymax = detections[0,0,:,6]
                top_indices = [i for i, conf in enumerate(det_conf) if conf >= 0.3]
    #            top_indices2 = [i for i, conf in enumerate(det_label) if (conf <= 3) ]
    #            top_indices = [val for val in top_indices1 if val in top_indices2]
                top_conf = det_conf[top_indices]
                top_label_indices = det_label[top_indices].tolist()
                top_labels = self.get_labelname(labelmap, top_label_indices)
                top_xmin = det_xmin[top_indices]
                top_ymin = det_ymin[top_indices]
                top_xmax = det_xmax[top_indices]
                top_ymax = det_ymax[top_indices]
                xminlist = list()
                yminlist = list()
                xmaxlist = list()
                ymaxlist = list()
                for i in xrange(top_conf.shape[0]):
                    xmin = int(round(top_xmin[i] * imgshape[1]))
                    ymin = int(round(top_ymin[i] * imgshape[0]))
                    xmax = int(round(top_xmax[i] * imgshape[1]))
                    xmax = xmax if xmax < imgshape[1] else xmax-1
                    ymax = int(round(top_ymax[i] * imgshape[0]))
                    ymax = ymax if ymax < imgshape[0] else ymax-1
                    xminlist.append(xmin)
                    yminlist.append(ymin)
                    xmaxlist.append(xmax)
                    ymaxlist.append(ymax)
                    score = top_conf[i]
#                    label = int(top_label_indices[i])
                    label_name = top_labels[i]
                    if(needsend == False):
                        needsend = self.filterScore(scoremap,label_name, score)
                    innerbox =  "{xmin:%d, ymin:%d,xmax:%d, ymax:%d, score:%f,label:\"%s\"},"% (xmin, ymin,xmax,ymax,score,label_name)
                    returnMessage = returnMessage + innerbox
                returnMessage = returnMessage + "],"
                returnMessage = returnMessage.replace("},],", "}],")
                #save file
                logging.info("needSave is :%s" %needsend)
                if(needsend):
                    realname = self.drewRectangleAndSave(xminlist,xmaxlist,yminlist,ymaxlist,img_np)
                    realname =  str(realname).replace("\\x005","")
                    restMessage = "img_width:%d, img_height:%d, img_src:\"%s\",check_type:\"%s\",cameraid:\"%s\"}"%(imgshape[1],imgshape[0],realname,"personAndCar",cameraid)
                    returnMessage = returnMessage+restMessage
                    logging.info(returnMessage)
                    return returnMessage
                else:
                    return None
        
    #人是否戴安全帽
    def manAndHat(self,cameraid,img_np,detections,imgshape,scoremap,labelmap):
                returnMessage = "{label_list:["
                det_label = detections[0,0,:,1]
                det_conf = detections[0,0,:,2]
                det_xmin = detections[0,0,:,3]
                det_ymin = detections[0,0,:,4]
                det_xmax = detections[0,0,:,5]
                det_ymax = detections[0,0,:,6]
                top_indices = [i for i, conf in enumerate(det_conf) if conf >= 0.1]
    #            top_indices2 = [i for i, conf in enumerate(det_label) if (conf <= 3) ]
    #            top_indices = [val for val in top_indices1 if val in top_indices2]
                top_conf = det_conf[top_indices]
                top_label_indices = det_label[top_indices].tolist()
                top_labels = self.get_labelname(labelmap, top_label_indices)
                top_xmin = det_xmin[top_indices]
                top_ymin = det_ymin[top_indices]
                top_xmax = det_xmax[top_indices]
                top_ymax = det_ymax[top_indices]
                hat  = list()
                man = list();
                xminlist = list()
                yminlist = list()
                xmaxlist = list()
                ymaxlist = list()
                for i in xrange(top_conf.shape[0]):
                    xmin = int(round(top_xmin[i] * imgshape[1]))
                    ymin = int(round(top_ymin[i] * imgshape[0]))
                    xmax = int(round(top_xmax[i] * imgshape[1]))
                    xmax = xmax if xmax < imgshape[1] else xmax - 1
                    ymax = int(round(top_ymax[i] * imgshape[0]))
                    ymax = ymax if ymax < imgshape[0] else ymax - 1
                    score = top_conf[i]
#                    label = int(top_label_indices[i])
                    label_name = top_labels[i]
                    needsend = self.filterScore(scoremap,label_name, score)
                    if(needsend == False):
                        continue
                    if(label_name == "hat"):
                        hat.append(RectangROI.Rectangle(xmin,xmax,ymin,ymax,None))
                    elif(label_name == "person"):
                        innerbox = "{xmin:%d, ymin:%d,xmax:%d, ymax:%d, score:%f,label:\"%s\"}," % (xmin, ymin, xmax, ymax, score, label_name)
                        man.append(RectangROI.Rectangle(xmin,xmax,ymin,ymax,innerbox))
                logging.info("hat %d  man %d" %(len(hat),len(man)))
                manlist = self.checkhat(hat, man)
                #人人都戴帽子则 放弃报警
                if (len(manlist)==0):
                    return   None             
                for m in manlist:
                    returnMessage = returnMessage + m.desc
                    xminlist.append(m.left)
                    yminlist.append(m.bottom)
                    xmaxlist.append(m.right)
                    ymaxlist.append(m.top)
                returnMessage = returnMessage + "],"
                returnMessage = returnMessage.replace("},],", "}],")
                realname = self.drewRectangleAndSave(xminlist,xmaxlist,yminlist,ymaxlist,img_np)
                realname =  str(realname).replace("\\x005","")
                restMessage = "img_width:%d, img_height:%d, img_src:\"%s\",check_type:\"%s\",cameraid:\"%s\"}" % (imgshape[1], imgshape[0], realname, "manAndHat", cameraid)
                returnMessage = returnMessage + restMessage
                logging.info(returnMessage)
                return returnMessage