import cv2
import os
from ultralytics import YOLO
import torch
import threading
from fastapi import HTTPException
import time


class Camera:
    def __init__(self, url, camera_id):
        self.frame = None
        self.image = None
        self.detections = []
        self.is_active = True

        self.model = YOLO("models/fire_smoke.pt")
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

        self.width = int(os.getenv("CAMERA_WIDTH", 640))
        self.height = int(os.getenv("CAMERA_HEIGHT", 480))
        self.queue_size = int(os.getenv("CAMERA_QUEUE_SIZE", 30))
        self.confidence = float(os.getenv("MODEL_CONFIDENCE", 0.2))
        self.frame_delay = float(os.getenv("FRAME_DELAY", 0.1))
        self.url = url
        self.camera_id = camera_id
        self.cap = self.__capture_video(url)

        self.thread = threading.Thread(target=self.__update_frame)
        self.thread.daemon = True
        self.thread.start()
        
        self.thread2 = threading.Thread(target=self.__health_check)
        self.thread2.daemon = True
        self.thread2.start()

        self.count2 = 0

    def __del__(self):
        self.cleanup()

    def cleanup(self):
        self.is_active = False
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        if self.thread.is_alive():
            self.thread.join(5)
        if self.thread2.is_alive():
            self.thread.join(5)

    def __capture_video(self, url):
        cap = cv2.VideoCapture(url)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
        return cap

    def __process_prediction(self, results):
        detections = []
        for result in results:
            for detection in result.boxes.data:
                if len(detection) >= 7:
                    x_min, y_min, x_max, y_max, track_id, confidence, class_id = detection[:7]
                    detections.append({"class_id": int(class_id)})
                else:
                    x_min, y_min, x_max, y_max, confidence, class_id = detection[:6]
                    detections.append({"class_id": int(class_id)})
        return detections

    def __update_frame(self):
        count = 0
        while self.is_active:
            count += 1
            if count == 20:
                print(f"__update_frame: {self.camera_id}")    
                count = 0
            success, image = self.cap.read()
            if not success:
                self.stop()
                raise HTTPException(503, "Camera connection Error")
            self.image = image
            # time.sleep(self.frame_delay * 0.5)
        self.stop()

    def get_frame(self):
        self.count2 += 1
        if self.count2 < 15:
            print(f"get_frame: {self.camera_id}")
            self.count2 = 0
        results = self.model.track(source=self.image, conf=self.confidence, verbose=False)
        detections = self.__process_prediction(results)
        annotated_image = results[0].plot()
        annotated_image = cv2.resize(annotated_image, (self.width, self.height))

        ret, jpeg = cv2.imencode('.jpg', annotated_image)

        self.frame = jpeg.tobytes()
        self.detections = detections
        return self.frame, self.detections

    def stop(self):
        self.is_active = False

    def __health_check(self):
        while self.is_active:
            print(f"Camera {self.camera_id} is alive")
            time.sleep(4)