import cv2
import numpy as np
import pandas as pd
import os
from ultralytics import YOLO
import torch
import easyocr
from collections import Counter

from src.speed_analysis.speed_estimator import SpeedEstimator
from src.utils.video_utils import save_video
from src.analytics.analyze_traffic import analyze_traffic
from src.reports.generate_report import generate_report

def process_video(video_path, base_path =".", SPEED_LIMIT= 50):


    # Get the points from "src.util.click_perspective_points.py" for a good estimation
    src_pts = np.float32([[216, 374], [35, 381], [73, 215], [228, 217]])  

    # Now write real points in meters 
    dst_pts = np.float32([[3.5, 3.0], [0, 3.0], [0, 0], [3.5, 0]])  

    # Transformation Matrix
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)

    cap = cv2.VideoCapture(video_path) # cv2 read the video # 0 or 1 to get webcam
    fps = cap.get(cv2.CAP_PROP_FPS)  # get the fps


    # Init Model and SpeedEstimator
    model = YOLO("yolov8n.pt") # Model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    speed_estimator = SpeedEstimator(fps, M) # Speed estimator needs fps and matrix
    ocr = easyocr.Reader(['en'], gpu=True)  # OCR = Optical Character Recognition to read text in images





    violations = []
    output_video_frames=[]
    track_log = []

    frame_id = 0 # define the variable
    while cap.isOpened():
        success, frame = cap.read() # Succes =  True or False / frame = each frame of video
        if not success: # if Succes = false -> break
            break

        results = model.track(frame, persist=True, device=device) # Apply yolo in each frame and persist = keep the same ID
        boxes = results[0].boxes # get all the object detected 

        class_counter = Counter()
        
        for box in boxes: # every object

            conf = float(box.conf[0])
            conf = round(conf, 2)

            class_id = int(box.cls[0])
            class_name = results[0].names[class_id]
            class_counter[class_name] += 1

            id = int(box.id[0]) if box.id is not None else -1  # if box.id[0] has something then get the id otherwise -1
            if id == -1: continue # if id = -1 by the code above, dont pay attention to that box

            x1, y1, x2, y2 = map(int,box.xyxy[0]) # Coordinates
            #cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2) # Center of every box
            cx, cy = int(x2), int(y2) # bottom right corner
            ocr1, ocr2 = int(x2/2), int(y2) # bottom middle
            speed_estimator.update(frame_id, id, (cx, cy)) # save the center of every box

            speed = speed_estimator.compute_speed(id) # calculate the speed of that object by the ID
            is_violation = speed > SPEED_LIMIT # Boolean True or false, True= violation commited
            speed_int = f"{int(speed)} km/h" # get the speed 

            # frame from yolo
            annotated = results[0].plot()



            color = (0, 255, 0) if not is_violation else (0, 0, 255) # color dependo on speed
            cv2.putText(annotated, speed_int, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2) # print speed

            # Draw if is_violation = True
            if is_violation:
                cv2.putText(annotated, "Out of speed limit", (cx, cy + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2) # draw over the frame if there's a infringement

            # Save data each speeding
                violations_data={
                    "frame": frame_id,
                    "id": id,
                    "clase": class_name,
                    "speed_kph": int(speed),
                    "violation": is_violation,
                    "position": (int((x1 + x2) / 2), int((y1 + y2) / 2)),
                    "plate" : "cant be read"
                }

                # OCR on the box 
                w, h = x2-x1, y2-y1 # width and height
                plate_y_start= int(y1+h*0.7) # 30 percent of the box
                plate_y_end= y2 # bottom
                plate_crop= frame[plate_y_start:plate_y_end, x1:x2] #get that size from box
                if plate_crop.size ==0: 
                    continue

                plate= ocr.readtext(plate_crop) #predict
                
                if plate:
                    text, score = plate[0][1], plate[0][2]
                    if score > 0.5:  # Puedes ajustar este umbral
                        plate_text = text
                        violations_data['plate']=plate_text
                        cv2.putText(annotated, f"Placa: {plate_text}", (ocr1, ocr2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                violations.append(violations_data)
            
            track_log.append({
                "frame": frame_id,
                "id": id,
                "class": class_name,
                "conf": conf,
                "speed_kph": int(speed)
            })
            output_video_frames.append(annotated)


        start_y = 30
        for i, (cls_name, count) in enumerate(class_counter.items()):
            text = f"{cls_name}: {count}"
            cv2.putText(annotated, text, (20, start_y + i * 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            

        #cv2.imshow("Speed Tracking", annotated)
        #if cv2.waitKey(1) & 0xFF == 27:
         #   break

        frame_id += 1

    cap.release()
    #cv2.destroyAllWindows()


    # violations csv
    df=pd.DataFrame(violations)
    output_path_speed_limit_csv = os.path.join(base_path,"data","output_data", "violations.csv")
    df.to_csv(output_path_speed_limit_csv,index=False)

    # video analyzed
    output_video_path_avi= os.path.join(base_path,"data","output_data","video_analyzed.avi")
    output_video_path_mp4= os.path.join(base_path,"data","output_data","video_analyzed.mp4")
    save_video(output_video_frames,output_video_path_avi,output_video_path_mp4)

    # tracking data
    df_track = pd.DataFrame(track_log)
    output_track_path= os.path.join(base_path,"data","output_data","tracking_data.csv")
    df_track.to_csv(output_track_path, index=False)

    # tracking data_analyzed
    output_path_data_analyzed= os.path.join(base_path,"data","output_data")
    analyze_traffic(output_path_data_analyzed)

    # Report data_analyzed
    output_pdf= os.path.join(base_path,"data","output_data","report_traffic.pdf")
    generate_report(output_track_path,output_path_speed_limit_csv,output_path_data_analyzed,output_pdf)


    print("Analysis files saved")

    return {
        "video_analyzed": output_video_path_mp4,
        "violations_csv": output_path_speed_limit_csv,
        "tracking_csv": output_track_path,
        "report_pdf": output_pdf,
        "data_folder": output_path_data_analyzed
    }