import cv2
import numpy as np

# YOLOv4-tiny modelini yükleme
net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")

# Sınıf etiketlerini yükleme
classes = []
with open("coco.names.txt", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Giriş görüntüsünü yükleme
cap = cv2.VideoCapture("Toplu.mp4")

while True:
    ret,frame = cap.read()

    if ret == False:
        break
    # Giriş görüntüsünü modelin girdi boyutuna yeniden boyutlandırma
    blob = cv2.dnn.blobFromImage(frame, 1/255, (416,416), swapRB=True, crop=False)

    # YOLOv4-tiny modelini yapılandırma
    net.setInput(blob)

    # Nesne tespiti yapma
    outs = net.forward(net.getUnconnectedOutLayersNames())

    # Tespit edilen nesneleri sınırlayıcı kutularla çizme
    conf_threshold = 0.5
    nms_threshold = 0.4
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                width = int(detection[2] * frame.shape[1])
                height = int(detection[3] * frame.shape[0])
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                class_name = classes[class_id]
                cv2.rectangle(frame, (left, top), (left + width, top + height), (0, 255, 0), 2)
                cv2.putText(frame, class_name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Nesne tespiti yapılan görüntüyü gösterme
    cv2.imshow("Nesne Tespiti", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
