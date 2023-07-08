#!/usr/bin/env python

import rospy
from naoqi import ALProxy
from group3.srv import *
from motion_controller import *
from utility import *
from abc import abstractmethod
from detector import *

intro = "Hello, my name is NAO.  Today we're going to play a nice game together... Please come closer"

#Abstract class, Pattern STATE
class State():
    """
    Abstract class to initialize Pattern State
    """
    @abstractmethod
    def handle(self, manager):
        pass

#Concrete Class to Intro
class Intro(State):
    """
    Concrete Class to Intro, when NAO presents itself
    """
    def handle(self, manager):
        print("\nINTRO")
        if "ACK" != text_2_speech(intro):
            print("Speach failed: intro")
            manager.state = manager.error
        manager.state = manager.waiting_for_person
        
#Concrete Class to wait a person that come closer

class WaitingForPerson(State):
    """
    Concrete Class to wait a person that come closer
    """
    def handle(self, manager):
        print("\nWAITING A PERSON")
        while request_distance() > 1.0:
            print("Wait a child")
        manager.state = manager.speak_and_extend_arm
        

class SpeakAndExtendArm(State):
    """
    Concrete Class to speak and extend NAO's arm
    """
    def handle(self, manager):
        print("\nSPEAK AND EXTEND ARM")
        
        if "ACK" != text_2_speech("Let's start"):
            print("Speach failed: Let's start")
            manager.state = manager.error

        if "ACK" != send_movement_arm("up"):
            print("Movement UP arm failed")
            manager.state = manager.error

        if "ACK" != text_2_speech("If you show me what you have in your hand, I'll try to guess"):
            print("Speach failed: If you show me what you have in your hand, I'll try to guess")
            manager.state = manager.error

        if "ACK" != send_movement_arm("down"):
            print("Movement DOWN arm failed")
            manager.state = manager.error
        
        manager.state = manager.waiting_for_object

class WaitingForObject(State):
    """
    Concrete Class to wait an object that is close
    """
    def handle(self, manager):
        print("\nWAITING FOR OBJECT")
        result = request_distance()
        if float(result) < 1.0:
            manager.timer = 0
            manager.iteration_count = 0
            manager.state = manager.detect_object_and_speak
        else: 
            if manager.timer < (4):
                manager.timer += 1
                rospy.sleep(1)
            else:
                manager.timer = 0
                manager.state = manager.iteration_failed
    

class DetectObjectAndSpeak(State):
    """
    Concrete Class to detect an object and says what it is
    """
    def handle(self, manager):
        print("\nDETECT OBJECT AND SPEAK")
        if "ACK" != send_movement_head("down"):
            print("Movement Head DOWN failed")
            manager.state = manager.error
        
        obj = ""
        obj = detector_obj()

        if "ACK" != send_movement_head("up"):
            print("Movement Head UP failed")
            manager.state = manager.error

        if (obj != "ACK"):
            if "ACK" != text_2_speech("If I am not mistaken you are holding a................ " + obj):
                print("Speech failed: name object")
                manager.state = manager.error

            rospy.sleep(1)
            
            if "ACK" != text_2_speech("Very well, we are finished..."):
                print("Speech failed: Very well, we are finished")
                manager.state = manager.error

            manager.state = manager.waiting_for_person
        
        else:
            if "ACK" != text_2_speech("I'm sorry, I didn't able to understand what was the object"):
                print("Speach failed: I'm sorry, I didn't able to understand what was the object")
                manager.state = manager.error

            manager.state = manager.speak_and_extend_arm

class IterationFailed(State):
    def handle(self, manager):
        print("\nITERATION FAILED")
        manager.iteration_count += 1
        if manager.iteration_count < 3:
            manager.state = manager.speak_and_extend_arm
        else:
            if "ACK" != text_2_speech("I'm sorry, the game is failed, let's try again"):
                print("Speach failed: I'm sorry, the game is failed, let's try again")
                manager.state = manager.error

            manager.iteration_count = 0
            manager.state = manager.waiting_for_person

class Error(State):
    def handle(self, manager):
        print("\nTHERE IS AN ERROR, THE PROJECT'S WORKFLOW IS BREAK\n")
        return 1


class ManagerNode:
    def __init__(self):
        self.waiting_for_person = WaitingForPerson()
        self.speak_and_extend_arm = SpeakAndExtendArm()
        self.waiting_for_object = WaitingForObject()
        self.detect_object_and_speak = DetectObjectAndSpeak()
        self.iteration_failed = IterationFailed()
        self.intro = Intro()
        self.error = Error()
        
        self.state = self.intro
        self.iteration_count = 0
        self.timer = 0

    def run(self):
        while True:
            self.state.handle(self)

if __name__ == '__main__':
    rospy.init_node("project_manager")
    manager = ManagerNode()
    manager.run()
