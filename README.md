#Intelligent-NVR-platform

 this project contain 3 parts
    1:)camera side: use c++ to invoke camera SDK
    2:)caffe side:use python to invoke caffe module,and do some business
    3:)web side:use java ,j2ee to get results from caffe side,to exhibit
   
 It's complex,We are  familiar with java&python, but Hikvision Camera  only has c++  SDK, so  we need to use c++ to invoke it's original service. 
 We use rabbitMQ as the RPC server to connect  each layers;use FastDfs+nginx as image server;use Caffe's SSD branch as object detection module
 
Installation
    1.rabbitMQ http://www.rabbitmq.com/
    2.FastDfs + nginx https://sourceforge.net/projects/fastdfs/
    3.caffe SSD branch http://caffe.berkeleyvision.org/
    4.python2.7,java7,tomcat8
    
 




    
    