# Reference:
# Author = Leondi Soetojo

import sys
import speech_recognition as sr
import pub_cmd

client = pub_cmd.connect_mqtt()


class Voice_Commmand:
    def __init__(self):
        self.r = sr.Recognizer()
        self.text = None
        self.command = None

    def processing(self):
        while (True):
            self.start_action()
            self.action()

    def action(self):
        cmnd = self.command.lower()
        if ((self.find_substring('stop', cmnd) and self.find_substring('listen', cmnd)) or (self.find_substring('stop', cmnd) and self.find_substring('hear', cmnd))):
            self.do_action(1)
        elif (self.find_substring('listen', cmnd) or self.find_substring('hear', cmnd)):
            self.do_action(2)
        elif (self.find_substring('stop', cmnd) and (self.find_substring('song', cmnd) or self.find_substring('music', cmnd))):
            self.do_action(3)
        elif (self.find_substring('second', cmnd)):
            self.do_action(4)
        elif (self.find_substring('first', cmnd)):
            self.do_action(5)
        elif (self.find_substring('close', cmnd)):
            self.do_action(6)
        else:
            print('There is no such command here. \n Please say your command again.')
            self.command = self.convert_audio_to_txt()
            self.action()

    def do_action(self, type_num):
        if(type_num == 1):
            print('Action 1')
        elif (type_num == 2):
            print('Action 2')
        elif (type_num == 3):
            print('Action 3')
            pub_cmd.publish(client, "stop")
        elif (type_num == 4):
            print('Action 4')
            pub_cmd.publish(client, "lullaby2.mp3")
        elif (type_num == 5):
            print('Action 5')
            pub_cmd.publish(client, "lullaby1.mp3")
        elif (type_num == 6):
            sys.exit()

    def start_action(self):
        print('How can I help you? \n***Say: "play second song" OR Say: "play first song"***')
        print('If you want to end the program, please say "close the Nightlight": ')
        self.command = self.convert_audio_to_txt()

    def convert_audio_to_txt(self):
        with sr.Microphone() as source:
            # self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source)
            try:
                self.text = self.r.recognize_google(audio)
                return (self.text)
            except:
                print('I did not get that. Please say again.')
            self.convert_audio_to_txt()
                

    def find_substring(self, substring, txt):
        if substring in txt:
            return True
        else:
            return False


vc = Voice_Commmand()
vc.processing()
