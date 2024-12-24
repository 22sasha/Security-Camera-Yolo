import cv2
import os
from ultralytics import YOLO
import torch
import threading
from fastapi import HTTPException


class Camera:
    def __init__(self, url):
        self.model = YOLO("models/fire_smoke.pt")
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

        self.width = int(os.getenv("CAMERA_WIDTH", 640))
        self.height = int(os.getenv("CAMERA_HEIGHT", 480))
        self.queue_size = int(os.getenv("CAMERA_QUEUE_SIZE", 30))
        self.confidence = float(os.getenv("MODEL_CONFIDENCE", 0.2))

        self.url = url
        self.cap = self.__capture_video(url)

        self.frame = None
        self.detections = []
        self.image = None

        self.thread = threading.Thread(target=self.__update_frame)
        self.thread.daemon = True
        self.thread.start()

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.thread.join(5)  # TODO RuntimeError: cannot join current thread

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
        while True:
            success, image = self.cap.read()
            if not success:
                raise HTTPException(503, "Camera connection Error")
            self.image = image

    def get_frame(self):
        results = self.model.track(source=self.image, conf=self.confidence, verbose=False)
        detections = self.__process_prediction(results)
        annotated_image = results[0].plot()
        annotated_image = cv2.resize(annotated_image, (self.width, self.height))

        ret, jpeg = cv2.imencode('.jpg', annotated_image)
        
        self.frame = jpeg.tobytes()
        self.detections = detections
        return self.frame, self.detections
