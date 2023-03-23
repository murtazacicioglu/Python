import cv2
import math
import keyboard


# Yolov4 Modelleri Yüklenmesi
net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(320, 320), scale=1/255)



classes = []
with open("dnn_model/classes.txt", "r") as file_object:
    for class_name in file_object.readlines():

        class_name = class_name.strip()  # satır arası boşluklar için

        classes.append(class_name)



cap = cv2.VideoCapture("pythonproje2.mp4")

#########################################
## Futbolcular tespit edilip dikdörtgenlerle etrafı çevrelenecek.
## Futbolcuların birbiri ile temas halinde olduğunu göstermek için
## Futbolcuların etrafındaki dikdörtgen çerçevelerden yararlanilacak.
## Eğer dikdörtgenler birbirlerine belli bir mesafedelerse,kesişiyorlarsa futbolcular temas halinde sayilacak.

def fonk1(rect1, rect2): ## bölgeden bulma
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    if x1 > (x2 + w2) or x2 > (x1 + w1):
        return False
    if y1 > (y2 + h2) or y2 > (y1 + h1):
        return False


    return True
#########################################

def fonk2(rect1, rect2): ## koordinatlara göre bulma
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    max_x = max(x1,x2)
    min_x = min(w1,w2)

    if max_x <= min_x:
        return True
    return False



################################################
def fonk3(rect1, rect2, threshold=120): ######### merkezler arası uzaklıktan bulma

    rect1_center = ((rect1[0] + rect1[2]) / 2, (rect1[1] + rect1[3]) / 2)
    rect2_center = ((rect2[0] + rect2[2]) / 2, (rect2[1] + rect2[3]) / 2)
    mesafe = math.sqrt((rect1_center[0] - rect2_center[0]) ** 2 + (rect1_center[1] - rect2_center[1]) ** 2)
    if mesafe <= threshold: ## mesafe belli bir seviyeden kücükse True döndür.
        ##Kamera acisina gore threshold degisitirilebilir..
        return True
    else:
        return False

##########################################################

def pause(): ## Temas var dikdortgenini izlemek icin.
    while True:
        if keyboard.read_key() == 'space':
            break


while True:

    ret, frame = cap.read()


    ## Yolov4 nesne tespiti
    (class_ids, scores, bboxes) = model.detect(frame, confThreshold=0.1, nmsThreshold=0.1)

    for i, bbox in enumerate(bboxes):
        x, y, w, h = bbox
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        for j in range(i + 1, len(bboxes)):
                x2, y2, w2, h2 = bboxes[j]

                intersection1 = fonk1((x, y, x + w, y + h), (x2, y2, x2 + w2, y2 + h2))
                intersection2 = fonk2((x, y, x + w, y + h), (x2, y2, x2 + w2, y2 + h2))
                intersection3 = fonk3((x, y, x + w, y + h), (x2, y2, x2 + w2, y2 + h2))




                 #intersection varsa eğer dikdörtgen çiz
                if ( (intersection1 == True) and (intersection2==True) and (intersection3==True)):
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        cv2.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2), (0, 0, 255), 2)
                        cv2.putText(frame,"Temas Var" ,(x, y - 10), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2)
                        ##time.sleep(1)
                        ##pause()  ## temas var goruntulemek icin...







    cv2.imshow("Futbolcu Temas Tespiti", frame)
    key = cv2.waitKey(1)
    if key == 27:
         break

cap.release()
cv2.destroyAllWindows()


##########################

