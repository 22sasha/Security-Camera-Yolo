import cv2
import os
from ultralytics import YOLO
import torch


# TODO threading camera
class Camera():
    def __init__(self, url):
        self.model = YOLO("models/fire_smoke.pt")
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

        self.width = int(os.getenv("CAMERA_WIDTH", 640))
        self.height = int(os.getenv("CAMERA_HEIGHT", 480))
        self.confidence = float(os.getenv("MODEL_CONFIDENCE", 0.2))
        self.url = url
        self.cap = self.__capture_video(url)

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

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

                    detections.append({
                        "class_id": int(class_id),
                        # "confidence": float(confidence),
                        # "bbox": [int(x_min), int(y_min), int(x_max), int(y_max)]
                    })
                else:
                    x_min, y_min, x_max, y_max, confidence, class_id = detection[:6]

                    detections.append({
                        "class_id": int(class_id),
                        # "confidence": float(confidence),
                        # "bbox": [int(x_min), int(y_min), int(x_max), int(y_max)]
                    })
        return detections

    def get_frame(self):
        success, image = self.cap.read()
        if not success:
            return
        
        image = cv2.resize(image, (self.width, self.height))
        results = self.model.track(source=image, conf=self.confidence, verbose=False)
        detections = self.__process_prediction(results)

        annotated_image = results[0].plot()
        ret, jpeg = cv2.imencode('.jpg', annotated_image)
        return jpeg.tobytes(), detections
