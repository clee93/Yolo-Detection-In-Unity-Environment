# UDP boiler code: https://github.com/Siliconifier/Python-Unity-Socket-Communication

import UdpComms as U
import time

import cv2
from PIL import Image
import io
import numpy

# Load Yolo ML algo
loc = "./2ClassesTrained/"
CONFIDENCE_THRESHOLD = 0.2
NMS_THRESHOLD = 0.4
COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

class_names = []
with open(loc + "dataset.names", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]

net = cv2.dnn.readNet(loc + "yolov4-gym-2c_last.weights", loc + "yolov4-gym-2c.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

# Create UDP socket to use for sending (and receiving)
sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)

i = 0

while True:
    #sock.SendData('Sent from Python: ' + str(i)) # Send this string to other application
    #i += 1

    data = sock.ReadReceivedData() # read data

    if data != None: # if NEW data has been received since last ReadReceivedData function call
        #print(data) # print new received data
        img = Image.open(io.BytesIO(data))
        frame = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)

        # AI Detect and Classify
        start = time.time()
        classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
        end = time.time()

        start_drawing = time.time()
        for (classid, score, box) in zip(classes, scores, boxes):
            color = COLORS[int(classid) % len(COLORS)]
            #label = "%s : %f" % (class_names[classid[0]], score)
            #print(classid)
            label = str(class_names[classid]) + " : " + str(score)
            cv2.rectangle(frame, box, color, 2)
            cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        end_drawing = time.time()

        fps_label = "FPS: %.2f (excluding drawing time of %.2fms)" % (1 / (end - start), (end_drawing - start_drawing) * 1000)
        cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        ##

        cv2.imshow("detections", frame)
        cv2.waitKey(1)

    time.sleep(0.00001)

