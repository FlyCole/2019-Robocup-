import dlib
import qi
import cv2
import sys


class my_test:
    def __init__(self,params):
        self.ip = params["ip"]
        self.port = params["port"]
        self.lowest_index = 0
        self.session = qi.Session()
        self.switch = True
        try:
            self.session.connect("tcp://" + self.ip + ":" + str(self.port))
        except RuntimeError:
            print("connection Error!!")
            sys.exit(1)
        self.motion =self.session.service("ALMotion")
        self.detector = dlib.get_frontal_face_detector()
        print"detector succeed"
        cap = cv2.VideoCapture(0)
        self.is_detect = False
        count = 0
        success, frame = cap.read()
        while success:
            self.motion.moveto(0,0,-count * 1/6 * 3.14)
            count += 1
            if count > 6:
                break
            self.is_detect = True
            if self.is_detect == True:
                #cv2.imshow("capture",frame)
                frame_copy = frame.copy()
                rects = self.detector(frame_copy, 1)
                if len(rects) != 0:
                    self.lowest_face = rects[0]
                    self.lowest_index = count
                    print "valid"
                    for rect in rects:
                        if rect.bottom() >= self.lowest_face.bottom():
                            self.lowest_face = rect
                    cv2.rectangle(frame_copy, (self.lowest_face.left(), self.lowest_face.top()),
                                  (self.lowest_face.right(), self.lowest_face.bottom()), (0, 0, 255), 2, 8)
                    cv2.imshow("face",frame_copy)
            self.is_detect=False
            if cv2.waitKey(1) >= 0:
                break
            success, frame = cap.read()
        cv2.destroyAllWindows()
        cap.release()

def main():
    params = {
        'ip': "192.168.43.30",
        'port': 9559,
        'rgb_topic': 'pepper_robot/camera/front/image_raw'
    }
    pio = my_test(params)

if __name__ == "__main__":
    main()
