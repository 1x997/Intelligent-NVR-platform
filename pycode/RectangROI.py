# -*- coding: UTF-8 -*-
'''
Created on 2016年11月3日

@author: ye
'''
import math
class Rectangle:    
     #分别表示最上下左右上的坐标   
    def __init__(self,left,right,bottom,top,desc): 
        if (left >= right or top <= bottom): 
            print "矩形坐标初始化错误！" 
 #           print"矩形坐标初始化错误！");  
            return 
        self.left = left  
        self.right = right  
        self.top = top  
        self.bottom = bottom 
        self.desc = desc
# 两个矩形都是平行于X,Y轴，判断是否相交。两种方法，都需要检查特殊情况。  
class RectangleIntersect:
    def __init__(self):
        print ""
    #hat矩形在man矩形内 
    def isRectInside(self,hat,man):
        if (hat.top <= man.top and  hat.bottom >= man.bottom and  hat.right <= man.right and  hat.left >= man.left) :
            return True
        return False 
        
    # 方法一：矩阵在X,Y轴上的投影都在另一矩形投影的一侧，则矩阵必定无交集；否则，有交集。  
    def  isRectIntersect(self,a,b):          
        if ((a.top < b.bottom )or(b.top<a.bottom)or(b.right<a.left)or( a.right < b.left)):
            return False 
        return True;  
  
  
    # 若两矩形相交，相交区域必定有：top = min(top),bottom = max(bottom),right =  
    # min(right),left = max(left)  
    def intersectArea(self,a,b):
         
        if (self.isRectIntersect(a, b)): 
            return (min(a.top, b.top) - max(a.bottom, b.bottom)) * (min(a.right, b.right) - max(a.left, b.left));    
        return 0;
    #获取相交面积占帽子面积的百分比  这里 b是帽子
    def getROI(self,man,hat):
        #帽子在人内部则直接返回
        if(self.isRectInside(hat, man)):
            return 1.0
        #帽子跟人相交算ROI
        if (self.isRectIntersect(man, hat)):
            fz = self.intersectArea(man, hat)
            fm = (hat.top - hat.bottom)*(hat.right - hat.left)
#            print "fz %f   fm %f raitis %f"%(fz,fm,float(fz)/fm)
            return float(fz)/fm  
        else:  
            return 0.0  
          

if __name__ == '__main__':
#     man left 142  ritht 177 top 152 bottom 81
# hat left 206  ritht 222 top 124 bottom 110
             #   left  right bottom top
    ra =  Rectangle(142, 177, 81, 152,None);  
    rb =  Rectangle(206, 222, 110, 124,None); 
    r =  RectangleIntersect()
    if (r.isRectIntersect(ra, rb)):
                  
        print ("两矩阵相交")  
    else:  
        print"两矩形不相交"  
              
    if (r.isRectIntersect2(ra, rb)): 
        print"两矩阵相交"
    else:  
        print"两矩形不相交"  
              
      
    print"相交区域面积： %f "%r.intersectArea(ra, rb)
 
 
  

  
  

