from os import system
system("sudo pigpiod")
from transitions.extensions import GraphMachine as Machine
from gpiozero import Button, DigitalOutputDevice, TonalBuzzer
from gpiozero.tones import Tone

import keyboard
import time
import cv2
import pandas as pd

import I2C_LCD_driver
from yolo import yolo
from contours import contours
from util import colorWipe, theaterChase, take_picture
from rpi_ws281x import PixelStrip, Color

mylcd = I2C_LCD_driver.lcd()
relay1 = DigitalOutputDevice(23)
relay2 = DigitalOutputDevice(24)

# LED strip configuration:
LED_COUNT = 54        # Number of LED pixels.
LED_PIN = 12          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

class idle(object):
    def __init__(self):
        relay1.off()
        relay2.off()
        colorWipe(strip, Color(255, 255, 255), (0,25))
        colorWipe(strip, Color(0, 255, 0), (25,54))

    def execute(self):
        mylcd.lcd_display_string("press green", 1, 0)
        mylcd.lcd_display_string("to start", 2, 0)    
        print('idle')

class start(object):
    def __init__(self):
        relay1.off()
        relay2.off()
        colorWipe(strip, Color(255, 255, 255), (0,25))
        colorWipe(strip, Color(0, 255, 0), (25,54))

    def execute(self):
        mylcd.lcd_display_string("close door", 1, 0)  
        print('close door')

class scan_objects(object):
    desinfect_time = None
    scanning = False
    def __init__(self):
       
        strip_1 = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, 200, LED_CHANNEL)
        strip_1.begin()
        colorWipe(strip_1, Color(255, 205, 50), (0,25))
        colorWipe(strip_1, Color(0, 0, 255), (25,54))

        take_picture(0)
        # name_image = take_picture(1)
        # name_image = take_picture(2)

        self.index_list =[]
        self.start = 0
        self.total_area = 0 
        self.value = 0
        scan_objects.scanning = False

    def execute(self):
        if self.start == 0 or self.start == 1:      
            mylcd.lcd_display_string("scanning objects", 1, 0)
            mylcd.lcd_display_string("please wait", 2, 0)
       
        elif(self.start == 2):
            mylcd.lcd_clear()
        else:
            reedswitch = Button(16)
            if (reedswitch.is_active and self.value == 2):
                mylcd.lcd_clear()
                self.value = 0
            elif (reedswitch.is_active == False and self.value == 1):
                mylcd.lcd_clear()
                self.value = 0

            elif reedswitch.is_active:
                mylcd.lcd_display_string("door closed", 1, 0)
                mylcd.lcd_display_string("please wait", 2, 0)
                self.value = 1
            else:
                mylcd.lcd_display_string("close door", 1, 0)
                self.value = 2

        if self.start == 0:
            contour = contours('scans/objects_0.jpg')
            contour.filters()
            contour.contours()
            print('Main area', contour.get_areas_of_contours())

            area_list, self.total_area = contour.get_areas_of_contours()
            self.contour_count = contour.get_amout_of_contours()

            contour.show_image()
            self.start = 1
 
        elif self.start == 1:
            detect = yolo('scans/objects_0.jpg')
            detect.detect_object()

            print('scan index', detect.get_index_list())
            self.index_list = detect.get_index_list()
   
            self.object_count, object_names = detect.get_name_of_object()
            print('scan name',self.object_count, object_names)

            detect.show_image()
            self.start = 2
       
        elif self.start == 2:
            if self.object_count >= self.contour_count:
                dataframe = pd.read_csv('object_list.csv')
                total_object_time = 0

                for index in self.index_list:
                    object_time = dataframe.iloc[index,1]
                    total_object_time = object_time + total_object_time

                scan_objects.desinfect_time = total_object_time
            else:
                scan_objects.desinfect_time = self.total_area * 0.0005
               
            self.start = 3
            scan_objects.scanning = True

        print('scan_objects')

class desinfect(object):
    def __init__(self):
        relay1.on()
        relay2.on()
        colorWipe(strip, Color(0, 0, 0), (0,25))
        colorWipe(strip, Color(136, 13, 190), (25,54))

    def execute(self):  
        mylcd.lcd_display_string("desinfecting", 1, 0)
        mylcd.lcd_display_string("time left: {}".format(Model.time_left), 2, 0)
        mylcd.lcd_display_string("s", 2, 15)
        print('desinfecting')

class finish(object):
    def __init__(self):
        relay1.off()
        relay2.off()
        colorWipe(strip, Color(0, 255, 0), (0,25))
        colorWipe(strip, Color(0, 255, 0), (25,54))
        print("finished")

    def execute(self):
        b = TonalBuzzer(13)
        mylcd.lcd_display_string("finished", 1, 0)
        mylcd.lcd_display_string("take out objects", 2, 0)
        b.play(Tone("C4"))
        time.sleep(0.5)
        b.stop()
        time.sleep(0.5)

class pause(object):
    def __init__(self):
        relay1.off()
        relay2.off()
        colorWipe(strip, Color(255, 255, 255), (0,25))
        colorWipe(strip, Color(255, 95, 0), (25,54))

    def execute(self):
        mylcd.lcd_display_string("paused", 1, 0)
        print('pause')

class stop(object):
    def __init__(self):
        relay1.off()
        relay2.off()
        colorWipe(strip, Color(255, 255, 255), (0,25))
       
    def execute(self):
        mylcd.lcd_display_string("stopped", 1, 0)
        theaterChase(strip, Color(255, 0, 0), (25,54))
        print('stop')

class resume(object):
    def __init__(self):
        colorWipe(strip, Color(255, 255, 255), (0,25))
        colorWipe(strip, Color(0, 0, 255), (25,54))

    def execute(self):        
        mylcd.lcd_display_string("resume programm", 1, 0)
        print('resume')

class error(object):
    def __init__(self):
        relay1.off()
        relay2.off()
        colorWipe(strip, Color(255, 0, 0), (0,25))
        colorWipe(strip, Color(255, 0, 0), (25,54))

    def execute(self):        
        mylcd.lcd_display_string("error!", 1, 0)
        mylcd.lcd_display_string("press red", 2, 0)
        print('error')

class Model(object):
    time_left = 0
    def __init__(self):
        relay1.off()
        relay2.off()
        self.strategy = idle()

        self.start = 0
        self.start1 = 0
        self.start_time = 0

        self.cap = None
        self.fgbg = None

    def execute(self):
        self.strategy.execute()

    def on_enter_idle(self):
        self.strategy = idle()

    def on_enter_start(self):
        self.strategy = start()

    def on_enter_scan_objects(self):
        self.strategy = scan_objects()

    def on_enter_desinfect(self):
        self.strategy = desinfect()

    def on_enter_finish(self):
        self.strategy = finish()

    def on_enter_pause(self):
        self.strategy = pause()

    def on_enter_stop(self):
        self.strategy = stop()

    def on_enter_resume(self):
        self.strategy = resume()

    def on_enter_error(self):
        self.strategy = error()

    def green_button(self):
        button_green = Button(17)
        if button_green.is_active:
            time.sleep(0.01)  
            return True
        else:
            time.sleep(0.01)  
            return False

    def orange_button(self):
        button_orange = Button(27)
       
        if button_orange.is_active:
            time.sleep(0.01)  
            return True
        else:
            time.sleep(0.01)  
            return False

    def red_button(self):
        button_red = Button(22)
        if button_red.is_active:
            time.sleep(0.01)  
            return True
        else:
            time.sleep(0.01)  
            return False

    def no_movement(self):
        if self.start == 0:
            self.cap = cv2.VideoCapture(0+cv2.CAP_ANY)
            self.fgbg = cv2.createBackgroundSubtractorMOG2()
            self.start = 1
           
        else:
            ret, frame = self.cap.read()

            if not ret:
                return False
            else:
                fgmask = self.fgbg.apply(frame)
                percentage = (fgmask> 0).mean()

                if percentage > 0.01:
                    self.start = 1
                    return False
                else:
                    time_now = time.time()
                    if self.start == 1:
                        self.time_start = time.time()
                        self.start = 2

                    if (time_now-self.time_start)>5:
                        self.start = 0 
                        self.cap.release()
                        return True
                    return False

    def door_closed(self):
        reedswitch = Button(16)

        if reedswitch.is_active:
            time.sleep(0.01)  
            return True
           
        else:
            time.sleep(0.01)
            return False

    def door_open(self):
        reedswitch = Button(16)

        if reedswitch.is_active:
            return False
           
        else:
            return True     

    def clear(self):
        if self.cap != None:
            self.cap.release()
        mylcd.lcd_clear()
   
    def time_delay(self):
        time.sleep(1.5)

    def time_delay2(self):
        if self.start == 0:
            self.start_time = time.time()
            self.start = 1

        time_now = time.time()

        if (time_now - self.start_time) > 3:
            self.start = 0
            return True
        else:
            return False

    def no_desinfect_time(self):
        if scan_objects.desinfect_time == 0 and scan_objects.scanning == True:
            mylcd.lcd_display_string("no objects found", 1, 0)
            if self.start1 == 0:
                self.start_time = time.time()
                self.start1 = 1

            time_now = time.time()

            if (time_now - self.start_time) > 3:
                self.start1 = 0
                return True
            else:
                return False
        else:
            return False

    def desinfect_time(self):
        if self.start == 0:
            self.start_time = time.time()
            self.start = 1

        time_now = time.time()
        Model.time_left = scan_objects.desinfect_time - (time_now - self.start_time)
        Model.time_left = round(Model.time_left)
       
        if (time_now - self.start_time) > scan_objects.desinfect_time:
            scan_objects.desinfect_time = 0
            self.start = 0
            return True
        else:
            return False

states = ['idle' , 'start', 'scan_objects' , 'desinfect' , 'pause' , 'stop' , 'resume' , 'error', 'finish']

transitions = [{'trigger': 'loop', 'source': 'idle', 'dest': 'start', 'conditions': 'green_button', 'after': "clear"},
               {'trigger': 'loop', 'source': 'start', 'dest': 'scan_objects', 'conditions': 'door_closed', 'after': "clear"},
               {'trigger': 'loop', 'source': 'scan_objects', 'dest': 'idle', 'conditions': ['no_desinfect_time'], 'after': "clear"},
               {'trigger': 'loop', 'source': ['scan_objects', 'resume'], 'dest': 'desinfect', 'conditions': ['door_closed', 'no_movement'], 'after': "clear"},
               {'trigger': 'loop', 'source': 'desinfect', 'dest': 'pause', 'conditions': 'orange_button', 'after': ["clear", "time_delay"]},
               {'trigger': 'loop', 'source': 'pause', 'dest': 'resume', 'conditions': 'orange_button', 'after': "clear"},
               {'trigger': 'loop', 'source': ['desinfect', 'scan_objects'], 'dest': 'stop', 'conditions': 'red_button', 'after': "clear"},
               {'trigger': 'loop', 'source': 'stop', 'dest': 'idle', 'conditions': 'time_delay2', 'after': "clear"},
               {'trigger': 'loop', 'source': 'desinfect', 'dest': 'error', 'conditions': 'door_open', 'after': "clear"},
               {'trigger': 'loop', 'source': 'error', 'dest': 'idle', 'conditions': 'red_button', 'after': "clear"},
               {'trigger': 'loop', 'source': 'desinfect', 'dest': 'finish', 'conditions': 'desinfect_time', 'after': "clear"},
               {'trigger': 'loop', 'source': 'finish', 'dest': 'idle', 'conditions': 'time_delay2', 'after': "clear"}]
               

model = Model()
machine = Machine(model=model, states=states, transitions=transitions,
                  initial='idle', finalize_event='execute', show_conditions=True)
model.get_graph().draw('state_machine/uv-c_box.png', prog='dot')                

if __name__ == '__main__':
    try:
        while True:
            model.loop()
            if keyboard.is_pressed('q'):
                model.clear()
                colorWipe(strip, Color(0, 0, 0), (0,54), 10)          
    except KeyboardInterrupt:
        model.clear()
        colorWipe(strip, Color(0, 0, 0), (0,54), 10)
