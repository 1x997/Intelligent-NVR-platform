#Intelligent-NVR-platform
This project consists of 3 parts: <br />
* Data input layer: use C++ to invoke camera SDK. <br />
* Caffe layer:use Python to invoke caffe module,and do some business. <br />
* Web layer:use Java&J2EE to get results from caffe layer,to exhibit. <br />
You can email yeliangm@126.com if you have any questions about this site.<br />

#External Components
Install all components below:
* [rabbitMQ](http://www.rabbitmq.com/): Robust messaging for applications,it also can be  used as a RPC server to connect each layer. <br />
* [FastDfs](https://sourceforge.net/projects/fastdfs/)[Nginx](http://nginx.org/):FastDFS is a distributed file system, its HTTP service is relatively simple, you can use nginx and its [plugin](https://sourceforge.net/projects/fastdfs/files/FastDFS%20Nginx%20Module%20Source%20Code/) to replace.<br />
* [caffe](http://caffe.berkeleyvision.org/) SSD branch:Caffe is a deep learning framework,we use it to train object detection model.<br />
* python2.7,java7,tomcat8:we use Python to invoke caffe, use Java components to create websites. <br />
* [PostgreSQL](https://www.postgresql.org/):we use PostgreSQL to store image metadata and other messages<br />

#Usage
change rabbitMQ and fastDfs  connection messages  in code.
sh pycode/startup.sh<br />
create database in PostgreSQL and run video-monitor/db/ddl.sql and data.sql <br />
change  address in video_monitor/webapp/src/main/resources/??.xml <br />
cp video-monitor/deploy/video-monitor.war  to your tomcat8/webapps/ <br />
sh tomcat8/bin/startup.sh<br />
