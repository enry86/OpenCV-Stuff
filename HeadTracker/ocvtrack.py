#!/usr/bin/python

import threading
import cv
import time

class FaceTracker (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)
        self.lastFace = (0,0)
        self.track = True
        self.cap = cv.CaptureFromCAM (0)
        cv.SetCaptureProperty(self.cap, cv.CV_CAP_PROP_FRAME_WIDTH, 800)
        cv.SetCaptureProperty(self.cap, cv.CV_CAP_PROP_FRAME_HEIGHT, 600)
        self.hc = cv.Load("haarcascade_frontalface_alt2.xml")


    def stop (self):
        self.track = False

    def getLastFace(self):
        return self.lastFace

    def run(self):
        while self.track:
            image = cv.QueryFrame(self.cap)

            #New instance of Haar classifier, the .xml file contains the pattern information for face recognition
            #option cv.CV_HAAR_FIND_BIGGEST_OBJECT restricts the tracking to only one face (the bigger one)
            #use cv.CV_HAAR_DO_CANNY_PRUNING do track multiple faces at once (I just did some experiment with this,
            #surely doc online provides more information about the different options)
            #(30,30) is the fixed dimension of the face to be tracked (this saves me by some shaking of head
            #position due to variation in face size recognized by openCV).
            #use (0,0) to let OpenCV determine the size of the head (useful to trak Z-axis position, TODO)
            face = cv.HaarDetectObjects(image, self.hc, cv.CreateMemStorage(), 1.2,2, cv.CV_HAAR_FIND_BIGGEST_OBJECT, (30,30) )

            if len(face) == 1:
                f = face[0]
                x,y,w,h = f[0]
                sx, sy = cv.GetSize(image)
                fx = float(x) + float(w) / 2
                fy = float(y) + float(h) / 2

                ogx = (fx - (float(sx) / 2.0)) / (float(sx) / 2.0)
                ogy = (fy - (float(sy) / 2.0)) / (float(sy) / 2.0)

                #yeah, I know I should use semaphores and stuff, but I'm on a hurry...
                self.lastFace = (ogx, ogy)
                time.sleep(0.05)
