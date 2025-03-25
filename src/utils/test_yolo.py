from ultralytics import YOLO
import cv2

img=cv2.imread(r"C:\Todos mis documentos\vehicle-intelligent-traffic\data\test_yolo.jpg")

# Yolo v8
modelv8= YOLO("yolov8n.pt")
resultv8=modelv8(img)
save_resultv8=resultv8[0].plot()
cv2.imwrite(r"C:\Todos mis documentos\vehicle-intelligent-traffic\data\result_test_yolo_v8.jpg", save_resultv8)


# Yolo v11
modelv11= YOLO(r"C:\Todos mis documentos\vehicle-intelligent-traffic\models\yolo11n.pt")
resultv11=modelv11(img)
save_resultv11=resultv11[0].plot()
cv2.imwrite(r"C:\Todos mis documentos\vehicle-intelligent-traffic\data\result_test_yolo_v11.jpg", save_resultv11)

# Yolo v5
modelv5= YOLO("yolov5nu.pt")
resultv5=modelv5(img)
save_resultv5=resultv5[0].plot()
cv2.imwrite(r"C:\Todos mis documentos\vehicle-intelligent-traffic\data\result_test_yolo_v5.jpg", save_resultv5)


#resultv8[0].show()

#resultv11[0].show()


