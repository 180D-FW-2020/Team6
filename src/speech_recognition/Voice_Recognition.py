# Reference:
# Author = Leondi Soetojo

import sys
import speech_recognition as sr
import pub_cmd

client = pub_cmd.connect_mqtt()


class Voice_Commmand:
    def __init__(self, filename):
        self.filename = filename
        self.r = sr.Recognizer()
        self.text = None
        self.command = None

    def processing(self):
        self.start_action()
        self.action()
        self.end_action()

    def action(self):
        cmnd = self.command.lower()

        if ((self.find_substring('stop', cmnd) and self.find_substring('listen', cmnd)) or (self.find_substring('stop', cmnd) and self.find_substring('hear', cmnd))):
            self.do_action(1)
        elif (self.find_substring('listen', cmnd) or self.find_substring('hear', cmnd)):
            self.do_action(2)
        elif (self.find_substring('stop', cmnd)):
            self.do_action(3)
        elif (self.find_substring('second', cmnd)):
            self.do_action(4)
        elif (self.find_substring('first', cmnd)):
            self.do_action(5)
        else:
            print('There is no such command here. \n Please say your command again.')
            self.processing()

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

    def convert_wav_to_txt(self):
        with sr.WavFile(self.filename) as source:
            self.r.adjust_for_ambient_noise(source, duration=1)
            rec = self.r.record(source)
            try:
                ls = self.r.recognize_google(rec, True)
                print("Possible Transcript: ")
                for prediction in ls:
                    print(" " + prediction)
            except:
                print('I could not understand the audio file')

    def start_action(self):
        print('How can I help you? ***Say: "play second song" OR Say: "play first song"***')
        self.convert_audio_to_txt()
        self.command = self.text
        self.first_action = True

    def end_action(self):
        print('If you want to end the program, please say "close the application": ')
        self.convert_audio_to_txt()
        if(self.find_substring('close', self.text) == True):
            sys.exit()
        else:
            self.processing()

    def convert_audio_to_txt(self):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source, phrase_time_limit=3)
            try:
                self.text = self.r.recognize_google(audio)
            except:
                print('I did not get that. Please say again.')
                self.convert_audio_to_txt()

    def find_substring(self, substring, txt):
        if substring in txt:
            return True
        else:
            return False


vc = Voice_Commmand('test.wav')
vc.processing()
