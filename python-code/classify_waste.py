import os
import numpy as np
import cvzone
from cvzone.SerialModule import SerialObject
from time import sleep
from cvzone.ClassificationModule import Classifier
import cv2
from tensorflow.keras.models import load_model
model = load_model(os.path.join('Resources','testmodel2.h5'))
arduino = SerialObject("COM10")

cap = cv2.VideoCapture(0)

imgArrow = cv2.imread("Resources/arrow.png",cv2.IMREAD_UNCHANGED)
classIDBins = 0

imgWasteList = []
pathFolderWaste = "Resources/waste"
pathlist = os.listdir(pathFolderWaste)
for path in pathlist:
    imgWasteList.append(cv2.imread(os.path.join(pathFolderWaste, path), cv2.IMREAD_COLOR))

imgBinsList = []
pathFolderBins = "Resources/Bins"
pathlist = os.listdir(pathFolderBins)
for path in pathlist:
    imgBinsList.append(cv2.imread(os.path.join(pathFolderBins, path), cv2.IMREAD_COLOR))

classDic = {0:None,
            1:0,
            2:1,
            3:1}


while True:
    _, img = cap.read()
    img1 = cv2.resize(img,(556,294))
    imgResize = cv2.resize(img,(256,256))
    imgBackground = cv2.imread('Resources/background.png')
    prediction = model.predict(np.expand_dims(imgResize/255, 0))
    predicted_class = np.argmax(prediction)
    ar = 0
    if predicted_class >0:
        imgBackground[127:127 + imgWasteList[predicted_class-1].shape[0], 849:849 + imgWasteList[predicted_class-1].shape[1]] = imgWasteList[predicted_class-1]
        imgBackground = cvzone.overlayPNG(imgBackground,imgArrow,(918,320))
        classIDBins = classDic[predicted_class]
        imgBackground[374:374 + imgBinsList[classIDBins].shape[0], 835:835 + imgBinsList[classIDBins].shape[1]] = imgBinsList[classIDBins]
        ar = classIDBins+1

    imgBackground[176:176+294,74:74+556] = img1

    cv2.imshow("Output", imgBackground)
    arduino.sendData([ar])

    cv2.waitKey(1)
