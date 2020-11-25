# Reference:
# Author = Leondi Soetojo

import sys
import speech_recognition as sr



class Voice_Commmand:
    def __init__(self,filename):
        self.filename = filename
        self.r = sr.Recognizer()
        self.text = None
        self.command = None
        self.clarify = False

    def processing(self):
        self.start_action()
        self.clarified()
        if(self.find_substring('yes',self.text)):
            self.action()
        else:
            self.processing()
        self.end_action()

                
    def action(self):
        cmnd = self.command.lower()
        if (self.find_substring('listen',cmnd)):
            self.do_action(1)
        elif (self.find_substring('not',cmnd) and self.find_substring('listen',cmnd)):
            self.do_action(2)
        else:
            print('There is no such command here.')
            self.processing()

    def do_action(self, type_num):
        if(type_num == 1):
            print ('Action 1')
        elif (type_num == 2):
            print ('Action 2')
        elif (type_num == 3):
            print ('Action 3')


    def convert_audio_to_txt(self):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source, phrase_time_limit=3)
            try:
                self.text = self.r.recognize_google(audio)
            except:
                print('I did not get that. Please say again.')
                self.convert_audio_to_txt()
                
                
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
        if(self.clarify == False):
            print('How can I help you? ')
            self.convert_audio_to_txt()
            self.command = self.text
            self.clarify = True
        else:
            print('Please repeated again?')
            self.convert_audio_to_txt()
            self.command = self.text

    def clarified(self):
        print('You said:  {}'. format(self.command))
        print('Was it what you meant?')
        print('Say: yes or no')
        self.convert_audio_to_txt()


    def end_action(self):
        print('If you want to end the program, please say "close the application": ')
        self.convert_audio_to_txt()
        if(self.find_substring('close', self.text) == True):
            sys.exit()
        else:
            self.processing()


    def find_substring (self, substring, txt):
        if substring in txt:
            return True
        else:
            return False

vc = Voice_Commmand('test.wav')
vc.processing()