'''
Created on Nov 16, 2013

@author: nicodjimenez

Data visualization functions.
'''

import cv2

def view_bitmap(bitmap):
    img = cv2.cvtColor(bitmap*255,cv2.COLOR_GRAY2BGR)
    cv2.imshow('thresh_after_dilation',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()