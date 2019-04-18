# -*- encoding: UTF-8 -*-
import qi
import atexit
import sys
import time
class SPR:
    def __init__(self,params):

        self.ip = params["ip"]
        self.port = params["port"]

        self.session = qi.Session()
        self.switch = True
        try:
            self.session.connect("tcp://" + self.ip + ":" + str(self.port))
        except RuntimeError:
            print("connection Error!!")
            sys.exit(1)

        self.tts = self.session.service("ALTextToSpeech")
        self.TabletSer = self.session.service("ALTabletService")
        self.memory = self.session.service("ALMemory")
        self.tts.setLanguage("English")
        self.tts.say("nanobot")
        time.sleep(1)
        self.tts.say("hotel de glace")
        time.sleep(1)
        self.tts.say("chatbot")

    def run(self):
        while True:
            continue

def main():
    params = {
        'ip': "192.168.3.18",
        'port': 9559,
        'rgb_topic': 'pepper_robot/camera/front/image_raw'
    }
    pio = SPR(params)
    pio.run()


if __name__ == "__main__":
    main()