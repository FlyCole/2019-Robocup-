# -*- encoding: UTF-8 -*-
import qi
import atexit
import time
import sitting
import os

class Dialog:
    answer_num = 0
    def __init__(self, session, topic_path, num_sitting, num_standing):
        print topic_path
        self.tran = 0
        self.end = False
        self.conv = session.service("ALDialog")
        self.memo = session.service("ALMemory")
        self.conv.setLanguage("English")
        self.SoundDet = session.service("ALSoundDetection")
        self.TabletSer = session.service("ALTabletService")

        self.start_time = time.localtime(time.time())
        self.sec0 = self.start_time[3] * 3600 + self.start_time[4] * 60 + self.start_time[5]
        self.if_second_time = False

        topf_path = topic_path.decode('utf-8')
        if self.conv.getLoadedTopics('enu')== []:
            topic_name = self.conv.loadTopic(topf_path.encode('utf-8'))
            self.conv.activateTopic(topic_name)
        else:
            print self.conv.getLoadedTopics('enu')
        self.memo= session.service("ALMemory")
        print "initialize succeed"
        self.tts = session.service("ALTextToSpeech")
        self.tts.say("I'm ready to answer question. If you want to stop, please say stop. If I've answered 5 questions, I would stop too")
        time.sleep(0.5)
        self.conv.subscribe("Talking")
        self.end_of_conv = self.memo.subscriber("stop_talking")
        self.end_of_conv.signal.connect(self.callback_stoptalking)
        self.conv_count = self.memo.subscriber("answered")
        self.conv_count.signal.connect(self.callback_answered)
        self.sit_ans = self.memo.subscriber("sitting")
        self.sit_ans.signal.connect(self.callback_sit)
        self.stand_ans = self.memo.subscriber("standing")
        self.stand_ans.signal.connect(self.callback_stand)
        self.wave_ans = self.memo.subscriber("waved")
        self.wave_ans.signal.connect(self.callback_wave)

        self.num_sitting = num_sitting
        self.num_standing = num_standing

        # now that the dialog engine is stopped and there are no more activated topics,
        # we can unload our topic and free the associated memory
        while True:
            time.sleep(1)
            current_time = time.localtime(time.time())
            sec = current_time[3] * 3600 + current_time[4] * 60 + current_time[5]
            if self.end == True:
                break
            elif self.answer_num >= 5:
                self.tts.say(" Thanks for your cooperation")
                self.conv.unsubscribe('Talking')
                self.conv.deactivateTopic('Talking')
                self.tran = 5
                self.if_second_time = True
                self.reset_count()


                #通过 回答5次结束
                break
            elif sec - self.sec0 > 150:
                if self.if_second_time:
                    continue
                self.tts.say(" Thanks for your cooperation")
                self.conv.unsubscribe('Talking')
                self.conv.deactivateTopic('Talking')
                self.tran = 5
                self.if_second_time = True
                self.reset_count()
                break



    def get_answer_num(self):
        return self.tran


    def callback_stand(self,msg):
        self.answer_num +=1
        self.tts.say("The number of people who standing is " + str(self.num_standing))

        last_ans = self.memo.getData("Dialog/LastAnswer")

        file = open('question_record.txt', 'a')
        file.write(last_ans)
        file.close()

        print last_ans

    def callback_wave(self,msg):
        self.answer_num +=1
        self.tts.say("The number of people who waving is 1")
        last_ans = self.memo.getData("Dialog/LastAnswer")

        file = open('question_record.txt', 'a')
        file.write(last_ans)
        file.close()

        print last_ans

    def callback_sit(self,msg):
        self.answer_num +=1
        self.tts.say("The number of people who sitting is " + str(self.num_sitting))
        last_ans = self.memo.getData("Dialog/LastAnswer")

        file = open('question_record.txt', 'a')
        file.write(last_ans)
        file.close()

        print last_ans

    def callback_stoptalking(self,msg):
        print msg
        self.conv.unsubscribe('Talking')
        self.conv.deactivateTopic('Talking')
        self.tts.say("Thanks for your cooperation")
        self.reset_count()
        self.end = True
        #通过that's all结束

    def callback_answered(self,msg):
        self.answer_num += 1
        last_ans = self.memo.getData("Dialog/LastAnswer")

        file = open('question_record.txt', 'a')
        file.write(last_ans)
        file.close()

    def reset_count(self):
        self.answer_num = 0
