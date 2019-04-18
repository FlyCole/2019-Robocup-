#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
import qi
import sys
import argparse
import time
import rospy
import atexit
import thread
import datetime
import actionlib
from actionlib_msgs.msg import GoalID
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty
from json import dumps
import os
from take_pic import PhotoCapture
import gender_predict
import dialog_answer

class speech_and_person_recognition():
    number = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
    num_man = 0
    num_woman = 0
    is_Detected = False
    peopleID = []
    is_Face_detected = False

    def __init__(self,params):

        # 退出程序时进入__del__函数
        atexit.register(self.__del__)

        # 初始化pepper的ip和port
        self.ip = params["ip"]
        self.port = params["port"]
        self.session = qi.Session()

        # 尝试连接pepper
        try:
            self.session.connect("tcp://" + self.ip + ":" + str(self.port))
        except RuntimeError:
            print("[Kamerider E] : connection Error!!")
            sys.exit(1)

        # 需要使用的naoqi api
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

        '''
        # topic的回调函数
        start_following_sub = self.Memory.subscribe("follow_switch")
        start_following_sub.signal.connect(self.callback_start_following)
        start_navigation_sub = self.Memory.subscribe("navigation_switch")
        start_navigation_sub.signal.connect(self.callback_start_navigation)
        face_detection_sub = self.Memory.subscribe("FaceDetected")
        face_detection_sub.signal.connect(self.callback_face_detection)
        '''

        # 关闭 basic_awareness
        self.BasicAwa.setEnabled(False)

        # 设置tracker模式为头追踪
        # --------------------------可能没用---------------------------
        self.Tracker.setMode("Head")

        # 初始化平板
        self.TabletSer.cleanWebview()

        # 订阅相机
        self.rgb_top = self.VideoDev.subscribeCamera('rgb_t', 0, 2, 11, 40)
        self.depth = self.VideoDev.subscribeCamera('dep', 2, 1, 17, 20)

        # 设置dialog语言
        self.Dialog.setLanguage("English")
        '''
        # 加载pepper电脑里的topic
        self.Topic_path = '/home/nao/top/competetion_enu.top'
        # 以utf-8的格式编码
        self.Topic_path = self.Topic_path.decode('utf-8')
        # ========================测试删除utf-8行不行===========================================
        self.Topic_name = self.Dialog.loadTopic(self.Topic_path.encode('utf-8'))
        '''
        # 初始化头的位置
        self.Motion.setStiffnesses("Head", 1.0)
        self.Motion.setAngles("Head", [0., -0.25], .05)
        self.TextToSpe.setLanguage("English")

        # 设置说话速度
        self.TextToSpe.setParameter("speed", 70.0)

        print self.AutonomousLife.getState()
        # 关闭AutonomousLife模式
        if self.AutonomousLife.getState() != "disabled":
            self.AutonomousLife.setState("disabled")
        self.RobotPos.goToPosture("Stand", .5)


        # 宣布猜谜
        self.annouce()

        # 等待10s
        time.sleep(1)

        # 转身定位人群
        # self.turn_to_find()


        # if self.AutonomousLife.getState() != "solitary":
        #     self.AutonomousLife.setState("solitary")
        #time.sleep(10)
        #性别检测
        # self.face_detection_sub = self.Memory.subscriber("FaceDetected")
        # self.face_detection_sub.signal.connect(self.on_FaceDetected)
        # while self.is_Face_detected == False:
        #     print("no person detected")
        #     time.sleep(3)
        # #开始检测性别
        # self.take_pic = PhotoCapture(self.session)
        # self.take_pic.takepic()
        # cmd = 'sshpass -p kurakura326 scp nao@' + str(self.ip) + ":/home/nao/picture/image_0.jpg ./person_image.jpg"
        # os.system(cmd)
        # self.num_man, self.num_woman = gender_predict.gender("./person_image.jpg")
        # self.TextToSpe.say("There are " + str(self.num_woman + self.num_man) + "people")
        # self.TextToSpe.say("the number of man is " + str(self.num_man))
        #
        # self.TextToSpe.say("the number of woman is " + str(self.num_woman))
        #
        # self.dialog = dialog_answer.Dialog(self.session,'/home/nao/top/dialog.top')

        #self.gender_detection()
        #self.Memory.removeData("WavingDetection/Waving")
        #邀请操作者

        #声源定位
        self.sound_localization()



        # while 1:
        #     a = self.Memory.getData("WavingDetection/Waving")
        #     b = self.Memory.getData("WavingDetection/PersonWaving")
        #     c = self.Memory.getData("WavingDetection/PersonWavingCenter")
        #     print a
        #     print b
        #     print c
        #     time.sleep(1)

        #挥手检测
        # while 1:
        #     self.waving_detection()
        #     time.sleep(1)

        # while 1:
        #     self.movement_detection()

        time.sleep(100)



    def __del__(self):
        print("shutting down")

    def annouce(self):
        self.TextToSpe.say("I want to play riddle games")

    def request(self):
        self.TextToSpe.say("I want to play riddles")

    def turn_to_find(self):
        self.Motion.moveTo(0,0,3.1415)
        self.Motion.waitUntilMoveIsFinished()


    def gender_detection(self):
        self.PeoplePer.subscribe("PeopleDetected")
        self.people_detection_sub = self.Memory.subscriber("PeoplePerception/PeopleDetected")
        self.people_detection_sub.signal.connect(self.callback_people_detection)

    def callback_people_detection(self,msg):
        if self.is_Detected == False:
            self.is_Detected = True
            print("Detected!")
            PeopleInfo = msg[1]
            people_number = len(PeopleInfo)
            if people_number > 1:
                self.TextToSpe.say("I have seen " + str(people_number) +" people")
            else:
                self.TextToSpe.say("I have seen " + str(people_number) +" person")
            i = 0
            while i < people_number:
                people_ID = PeopleInfo[i][0]
                if self.FaceCha.analyzeFaceCharacteristics(people_ID):
                    self.peopleID.append(people_ID)
                    print("Person NO." + str(i) + " analyze succeed!")
                else:
                    print("Person NO." + str(i) + " analyze failed!")
                    i -= 1
                i += 1
            print self.peopleID
            for j in range(len(self.peopleID)):
                test_result = self.Memory.getData("PeoplePerception/Person/" + str(self.peopleID[j]) + "/GenderProperties")
                if test_result[1] == 0:
                    print "yeah"
                else:
                    print test_result
                if test_result[0] == 1:
                    self.male_num += 1
                else:
                    self.female_num += 1
            self.TextToSpe.say("there are " + str(self.male_num) + " males and " + str(self.female_num) + "females")



            for k in range(len(self.peopleID)):
                self.WavingDet.subscribe("WavingDetection/Waving")
                self.waving_detection_sub = self.Memory.subscriber("WavingDetection/Waving")
                self.waving_detection_sub.signal.connect(self.callback_waving_detection)
                waving_result = self.Memory.getData("WavingDetection/Waving")
                print waving_result

    def sound_localization(self):
        self.SoundDet.setParameter("Sensitivity" , 0.5)
        print "Sensitivity set to 0.5"

        self.SoundDet.subscribe("SoundDetected")
        self.sound_detection_sub = self.Memory.subscriber("SoundDetected")
        self.sound_detection_sub.signal.connect(self.callback_sound_detection)

        self.SoundLoc.subscribe("SoundLocated")
        self.sound_localization_sub = self.Memory.subscriber("SoundLocated")
        #self.sound_localization_sub.signal.connect(self.callback_sound_localization)


    def callback_sound_detection(self,msg):
        print("Detected!")
        sound_loc = self.Memory.getData("ALSoundLocalization/SoundLocated")
        print sound_loc[1]

        self.Motion.moveTo(0,0,sound_loc[1][0])

    def callback_sound_localization(self,msg):
        print("Located!")
        sound_loc = self.Memory.getData("ALSoundLocalization/SoundLocated")
        print sound_loc[1]

    def waving_detection(self):
        #print self.WavingDet.getMaxDistance()
        #print self.WavingDet.getMinSize()
        self.WavingDet.subscribe("WavingDetection/Waving")
        self.waving_detection_sub = self.Memory.subscriber("WavingDetection/Waving")
        self.waving_detection_sub.signal.connect(self.callback_waving_detection)
        movement_loc = self.Memory.getData("WavingDetection/Waving")
        print movement_loc

    def callback_waving_detection(self,msg):
        print "Waving detected!"
        waving_loc = self.Memory.getData("WavingDetection/Waving")
        print waving_loc[1]

    def movement_detection(self):
        self.MovementDet.subscribe("MovementDetection/MovementDetected")
        self.movement_detection_sub = self.Memory.subscriber("MovementDetection/MovementDetected")
        self.movement_detection_sub.signal.connect(self.callback_movement_detection)

    def callback_movement_detection(self,msg):
        movement_loc = self.Memory.getData("WavingDetection/Waving")
        print movement_loc

    def on_FaceDetected(self,msg):
        if self.is_Face_detected == False:
            self.is_Face_detected = True
            if len(msg[1])<= 1:
                self.tts.say("I don't see anyone")
            elif len(msg[1]) >1:
                faceInfoArray = msg[1]
                number_of_people = len(faceInfoArray)-1
                print(number_of_people)
                result = "I've seen "+self.number[number_of_people]+" person"
                self.tts.say(result)
                time.sleep(2)


def main():
    params = {
        'ip': "192.168.3.18",
        'port': 9559,
        'rgb_topic': 'pepper_robot/camera/front/image_raw'
    }

    pio = speech_and_person_recognition(params)

if __name__ == "__main__":
    main()

