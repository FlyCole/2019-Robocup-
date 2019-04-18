#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
import sys
import time
import atexit
import argparse
import os
import gender_predict
import dialog_answer

class Presentation():
    def __init__(self, params):
        atexit.register(self.__del__)

        self.ip = params["ip"]
        self.port = params["port"]

        self.session = qi.Session()

        try:
            self.session.connect("tcp://" + self.ip + ":" +str(self.port))
        except RuntimeError:
            print("[Kamerider E] : connection Error!!")
            sys.exit(1)

        # 需要用到的naoqi_service
        self.VideoDev = self.session.service("ALVideoDevice")
        self.FaceCha = self.session.service("ALFaceCharacteristics")
        self.FaceDet = self.session.service("ALFaceDetection")
        self.Memory = self.session.service("ALMemory")
        self.Dialog = self.session.service("ALDialog")
        self.AnimatedSpe = self.session.service("ALAnimatedSpeech")
        self.AudioDev = self.session.service("ALAudioDevice")
        self.BasicAwa = self.session.service("ALBasicAwareness")
        self.AutonomousLife = self.session.service("ALAutonomousLife")
        self.TabletSer = self.session.service("ALTabletService")
        self.TextToSpe = self.session.service("ALTextToSpeech")
        self.Motion = self.session.service("ALMotion")
        self.RobotPos = self.session.service("ALRobotPosture")
        self.Tracker = self.session.service("ALTracker")
        self.PeoplePer = self.session.service("ALPeoplePerception")
        self.SoundDet = self.session.service("ALSoundDetection")
        self.SoundLoc = self.session.service("ALSoundLocalization")
        self.WavingDet = self.session.service("ALWavingDetection")
        self.MovementDet = self.session.service("ALMovementDetection")
        self.SpeakingMov = self.session.service("ALSpeakingMovement")

        # # 需要设置的参数
        # self.TextToSpe.setParameter("speed", 50.0)
        # self.TextToSpe.setLanguage("Chinese")
        # self.PeoplePer.resetPopulation()

        # 运行部分
        # 取消自动感知模式
        print "---Disabling the AutonomousLife Mode---"
        self.BasicAwa.setEnabled(False)
        if self.AutonomousLife.getState() != "disabled":
            self.AutonomousLife.setState("disabled")
        print "---AutonomousLife Mode Disable!---"

        # self.AnimatedSpe.say("I am saying the word testword !")

        # ttw = {"hello": ["hey", "yo", "testword"],
        #        "everything": ["everybody"] }
        # self.SpeakingMov.addTagsToWords(ttw)


        self.TextToSpe.setLanguage("English")
        self.TextToSpe.setParameter("pitchShift", 1.1)
        self.TextToSpe.setParameter("speed", 50)

        # self.Dialog.setLanguage("English")
        time.sleep(0)
        # 开始介绍
        print self.TextToSpe.getAvailableVoices()
        # self.TextToSpe.setParameter("pitchShift", 0.9)
        self.TextToSpe.setParameter("speed", 100)
        print self.TextToSpe.getParameter("defaultVoiceSpeed")
        self.AnimatedSpe.say("hello,I'm pepper,i'm the happiest boy here!")
        # self.AnimatedSpe.say("我是\\pau=50\\pepper")
        # self.AnimatedSpe.say("我们的\\pau=50\\OPEN项目做的是无人商场\\pau=200\\在商场中\\pau=200\\我会完成迎接顾客\\pau=200\\推荐商品\\pau=200\\"
        #                      "提供商品详细信息\\pau=200\\引导顾客到达商品所在地点\\pau=200\\结账等目前由人工完成的简单劳动")
        # self.AnimatedSpe.say("接下来\\pau=200\\由我为大家介绍\\pau=200\\我们商场项目的初创理念及流程")
        # self.AnimatedSpe.say("首先\\pau=200\\由于劳动力价格日益增长,机器人代替人工可以大幅度降低成本\\pau=200\\其次\\pau=200\\"
        #                      "在货物众多的商场中\\pau=200\\"
        #                      "单由人工寻找货物过于复杂\\pau=200\\也不可能掌握所有货物精确的位置\\pau=200\\而机器人能够通过数据库寻找货物\\pau=200\\"
        #                      "对其进行定位\\pau=200\\同时能够利用地图以及算法\\pau=100\\最快地导航到货物所在位置\\pau=200\\"
        #                      "从而引导顾客最快到达期望的位置\\pau=200\\同时\\pau=200\\所有货物的信息都能够出储存在电脑中\\pau=200\\"
        #                      "因此可以给顾客列出物品详细的信息\\pau=200\\以供他们进行选择\\pau=200\\最后\\pau=200\\我们会对顾客进行识别\\pau=200\\"
        #                      "并根据数据为他们推荐之前购买过的商品\\pau=200\\最高效且准确地找到顾客期望购买的物品\\pau=200\\在一定程度上能够帮助顾客回忆\\pau=200\\"
        #                      "以免忘记某些需要购买的物品"
        #                      )
        # Introduction

    def __del__(self):
        print("shutting down")

def main():
    params = {
        'ip': "192.168.3.18",
        'port': 9559,
        'rgb_topic': 'pepper_robot/camera/front/image_raw'
    }

    pio = Presentation(params)


if __name__ == "__main__":
    main()