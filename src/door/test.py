import cv2

def gen(camera):
        video = cv2.VideoCapture()
        video.open("rtsp://user:pass@IP")
        video.release()
        ret,image = video.read()
        ret,jpeg = cv2.imencode('.jpg',image)
        while True:
            frame = jpeg.tobytes()
            yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        def camerafeed(request): 
            return StreamingHttpResponse(gen(),content_type="multipart/x-mixed-replace;boundary=frame")