import cv2
import os
from ultralytics import YOLO
import torch
import threading
from fastapi import HTTPException
import time
from collections import defaultdict, deque


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
        
        self.camera_ready = False
        self.url = url
        self.camera_id = camera_id
        self.cap = self.__capture_video(url)

        self.detect_depth = 180
        self.track_history = defaultdict(lambda: deque(maxlen=self.detect_depth))

        self.thread = threading.Thread(target=self.__update_frame)
        self.thread.daemon = True
        self.thread.start()

    def __del__(self):
        self.cleanup()

    def cleanup(self):
        self.is_active = False
        time.sleep(1)
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        if self.thread.is_alive():
            self.thread.join(5)

    def __capture_video(self, url):
        cap = cv2.VideoCapture(url)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
        if cap.isOpened():
            self.camera_ready = True
        return cap

    def __process_prediction(self, results):
        detections = []
        current_frame_tracks = set()

        for result in results:
            for detection in result.boxes.data:
                if len(detection) >= 7:
                    x_min, y_min, x_max, y_max, track_id, confidence, class_id = detection[:7]
                    track_id = int(track_id)
                    current_frame_tracks.add(track_id)

                    self.track_history[track_id].append(1)
                    print(track_id, self.track_history[track_id])
                    if sum(self.track_history[track_id]) >= self.detect_depth:
                        print("OGO: ", track_id)
                        detections.append({
                            # "track_id": track_id,
                            "class_id": int(class_id),
                            # "confidence": float(confidence),
                            # "bbox": [float(x_min), float(y_min), float(x_max), float(y_max)]
                        })
                else:
                    ...
                    # x_min, y_min, x_max, y_max, confidence, class_id = detection[:6]
                    # detections.append({
                    #     "class_id": int(class_id),
                    #     # "confidence": float(confidence),
                    #     # "bbox": [float(x_min), float(y_min), float(x_max), float(y_max)]
                    # })

        for track_id in list(self.track_history.keys()):
            if track_id not in current_frame_tracks:
                self.track_history[track_id].append(0)

            if sum(self.track_history[track_id]) < self.detect_depth:
                print("PUFF...")
                del self.track_history[track_id]
        
        return detections

    def __update_frame(self):
        while self.is_active and self.camera_ready:
            success, image = self.cap.read()
            if not success:
                self.stop()
                raise HTTPException(503, "Camera connection Error")
            self.image = image
            # time.sleep(self.frame_delay * 0.5)
        self.stop()

    def get_frame(self):
        results = self.model.track(source=self.image, 
                                   conf=self.confidence,
                                   verbose=False,
                                   iou=0.3,
                                   device="cuda:0",
                                #    max_age=30,
                                #    min_hits=4,
                            )

        detections = self.__process_prediction(results)
        annotated_image = results[0].plot()
        annotated_image = cv2.resize(annotated_image, (self.width, self.height))

        ret, jpeg = cv2.imencode('.jpg', annotated_image)

        self.frame = jpeg.tobytes()
        self.detections = detections
        return self.frame, self.detections

    def stop(self):
        self.is_active = False
