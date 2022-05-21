import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PySide2 import *
from PyQt5.QtCore import *
import numpy as np
import time
import cv2
from videostream1 import *
from yolodetection4 import *
import time
# IMPORTING GUI FILE
from interface import *
# from threading import Thread
import threading
# thread = threading.Thread(target=f)
# thread.start()


class WorkingThread4(QThread):
    ImageUpdate = pyqtSignal(QImage)
   
    
    def run(self):
        self.ThreadActive = True

        # cv2.startWindowThread()

        


        Capture = cv2.VideoCapture("C:\\Users\\AAA\Desktop\\others\\FYP\\FYP WORK -threading\\FYP FEB 2022\\yoloModelData\\video2.mp4")
        # Capture = cv2.VideoCapture(0)

        
        # the output will be written to output.avi
        # out = cv2.VideoWriter(
        #     'output.avi',
        #     cv2.VideoWriter_fourcc(*'MJPG'),
        #     15.,
        #     (640,480))
        frame_width = int(Capture.get(3))
        frame_height = int(Capture.get(4))
        size = (frame_width, frame_height)
        # result = cv2.VideoWriter('demo.avi', 
        #                  cv2.VideoWriter_fourcc(*'MJPG'),
        #                  10, size)
        threadalive=0
        personDetectedInNewFrame=99
        firstthreadactivated=0
        imgno=0
        
        while self.ThreadActive:
            ret, frame = Capture.read()
            # frame1 = frame.copy()
            ret, frame1 = Capture.read()
            # ret1, frame2 = Capture.read()
            # print(frame.shape,"frame shape")
            # print(frame1.shape,"frame1 shape")

            
            
            
            
            # blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

            if ret:
                # frame = cv2.resize(frame, (300, 300))
                
                
                # diff = cv2.absdiff(frame1, frame2)

                # # res = cv2.absdiff(img1, img2)

                # #--- convert the result to integer type ---
                # diff = diff.astype(np.uint8)
                # # #--- find percentage difference based on number of pixels that are not zero ---
                # percentage = int((np.count_nonzero(diff) * 100)/ diff.size)
                

                # # print("percentage",percentage)
                # diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                # blur = cv2.GaussianBlur(diff_gray, (5, 5), 0)
                # _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
                # dilated = cv2.dilate(thresh, None, iterations=3)
                # contours, _ = cv2.findContours( dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                # for contour in contours:
                #         (x, y, w, h) = cv2.boundingRect(contour)
                #         if cv2.contourArea(contour) < 1000:
                #             continue
                #         cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                #         cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                #                 1, (255, 0, 0), 3)
                
                
                if threadalive==0:
                    thread = threading.Thread(target=YoloSSPModelDetection,args=[frame1])
                    thread.start()
                    threadalive=1
                    

                    # print("thread started")
               
                #This if will be false when a frame processing is completed by yolo
                if thread.is_alive()==False:
                    threadalive=0
                    myimg=frame
                    # print("inside,",framelist)         
                    if "person" in framelist:
                        print("yes person")
                        # print(framelist)
                        font = cv2.FONT_HERSHEY_PLAIN
                        for i in range(len(framelist[7])):
                            if i in framelist[8]:
                                label = str(framelist[10][framelist[9][i]])
                                x, y, w, h = framelist[7][i]
                                # label = str(classes[class_ids[i]])
                                # person_confidence=confidences[i]
                                # print("person conf",person_confidence)
                                if label=="person":
                                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255,0,0), 1)
                                    # cv2.putText(frame, label, (x, y + 30), font, 3, (255,0,0), 1)
                                    
                        cv2.imwrite('imagestaken\\image'+str(imgno)+".png",framelist[5])
                        imgno+=1
                        #Remoing "person" string from framelist cuz the frame processing is completed
                        #and we want the list to be restored to default format.
                        

                        personDetectedInNewFrame=1
                        # print("yes person detected in new frame")
                        framelist[4]="reseted"
                        
                        confidence=framelist[6]
                    else:
                        personDetectedInNewFrame=0
                        # print("Noperson detected in new frame")
                        framelist[4]="n"


                #this code will keep running untill the thread complete its processing
                #providing real time view .
                else:

                    if personDetectedInNewFrame==1:
                        font = cv2.FONT_HERSHEY_PLAIN
                        for i in range(len(framelist[7])):
                            if i in framelist[8]:
                                label = str(framelist[10][framelist[9][i]])
                                x, y, w, h = framelist[7][i]
                                # label = str(classes[class_ids[i]])
                                # person_confidence=confidences[i]
                                # print("person conf",person_confidence)
                                if label=="person":
                                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255,0,0), 1)
                                    #cv2.putText(frame, label, (x, y + 30), font, 3, (255,0,0), 1)
                                    # print(framelist[6][i])
                                    # cv2.putText(frame,str(round(framelist[6][i]*100,2)),(framelist[0]+20,framelist[1]+30),
                                    # cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),1)                 
                    myimg=frame
                    
                    # print(thread.is_alive())
                    # print(threadalive,"outside")
                    # myimg=thread.join()
                
                # thread.join()
                # print("test completed")
                
                # YoloSSPModelDetection(frame1)
                
                


                    # YoloSSPModelDetection(frame1)
                # result.write(frame1)
                
                # if diff>40:
                #     print("yes")
                # if writer is not None:
                #     writer.write(frame)
                cv2.waitKey(60)
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # FlippedImage = cv2.flip(Image, 1)

                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)

                Picture = ConvertToQtFormat.scaled(1024, 720)
                self.ImageUpdate.emit(Picture)



   
    def stop(self):
        self.ThreadActive = False
        self.quit()
