#Intelligent-NVR-platform
 this project contain 3 parts <br />
    1:)camera side: use c++ to invoke camera SDK <br />
    2:)caffe side:use python to invoke caffe module,and do some business <br />
    3:)web side:use java ,j2ee to get results from caffe side,to exhibit <br />
   
 It's complex,We are  familiar with java&python, but Hikvision Camera  only has c++  SDK, so  we need to use c++ to invoke it's original service.  <br />
 We use rabbitMQ as the RPC server to connect  each layers;use FastDfs+nginx as image server;use Caffe's SSD branch as object detection module <br />
 
#Installation

tools:<br />
    1.rabbitMQ <http://www.rabbitmq.com/><br />
    2.FastDfs + nginx <https://sourceforge.net/projects/fastdfs/><br />
    3.caffe SSD branch <http://caffe.berkeleyvision.org/><br />
    4.python2.7,java7,tomcat8<br />
    
    
 




    
    