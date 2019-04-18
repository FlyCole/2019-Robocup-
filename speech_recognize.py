import qi
import sys
import time


class recognization:
    def __init__(self, params):
        self.ip = params["ip"]
        self.port = params["port"]
        self.session = qi.Session()
        self.swith = True
        try:
            self.session.connect("tcp://" + self.ip + ":" + str(self.port))
        except RuntimeError:
            print("connection Error!!")
            sys.exit(1)
        self.speechrec = self.session.service("ALSpeechRecognition")
        self.memory = self.session.service("ALMemory")


        self.speechrec.setLanguage("English")
        self.vocabulary = ["what", "when", "date", "dreams", "desert", "disk", "who", "where"]
        self.speechrec.setVocabulary(self.vocabulary, True)
        self.speechrec.subscribe("Mytest")
        self.speech_recog_sub = self.memory.subscriber("WordRecognized")
        # self.switch = True

        self.speech_recog_sub.signal.connect(self.call_back_recog)


        time.sleep(30)
        self.speechrec.unsubscribe("Mytest")

        print "Start Speech Recognization"
        while True:
            time.sleep(1)
            print self.memory.getData("WordRecognized")

    def call_back_recog(self, msg):
        # if self.switch == True:
        self.result = msg
        print self.result
            # self.switch = False

def main():
    params = {
        'ip': "192.168.43.30",
        'port': 9559,
        'rgb_topic': 'pepper_robot/camera/front/image_raw'
    }
    pio = recognization(params)
    pio.run()

if __name__ == "__main__":
    main()