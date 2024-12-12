import cv2

class Camera():
    def __init__(self, url, width, height):
        self.url = url
        self.width = width
        self.height = height
        self.video = cv2.VideoCapture(url)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        resized_image = cv2.resize(image, (self.width, self.height))
        ret, jpeg = cv2.imencode('.jpg', resized_image)
        return jpeg.tobytes()
