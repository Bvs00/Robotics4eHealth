#!/usr/bin/env python

import rospy
from naoqi import ALProxy
from group3.srv import *
from motion_controller import *
from utility import *
from abc import abstractmethod
from detector import *

intro = "Ciao, io sono NAO. Oggi faremo un bel gioco insieme... Ti prego di avvicinarti"

# Classe astratta per il Pattern STATE
class State():
    @abstractmethod
    def handle(self, manager):
        pass

#Classe concreta per l'intro
class Intro(State):
    def handle(self, manager):
        print("\nSono Nello stato INTRO")
        if "ACK" != text_2_speech(intro):
            print("Speach failed: Fammi vedere")
        manager.state = manager.waiting_for_person
        

#Classe concreta per il Pattern STATE
class WaitingForPerson(State):
    def handle(self, manager):
        print("\nSono Nello stato WAITING A PERSON")
        while request_distance() > 1.0:
            print("Wait a child\n")
        manager.state = manager.speak_and_extend_arm
        

class SpeakAndExtendArm(State):
    def handle(self, manager):
        print("\nSono Nello stato SPEAK AND EXTEND ARM")
        if "ACK" != text_2_speech("Iniziamo..."):
            print("Speach failed: Fammi vedere")
        if "ACK" != send_movement_arm("up"):
            print("Movement UP arm failed")
        if "ACK" != text_2_speech("Fammi vedere cosa hai in mano, vediamo se indovino"):
            print("Speach failed: Fammi vedere")
        if "ACK" != send_movement_arm("down"):
            print("Movement DOWN arm failed")
        
        manager.state = manager.waiting_for_object

class WaitingForObject(State):
    def handle(self, manager):
        print("\nSono Nello stato WAITING FOR OBJECT")
        result = request_distance()
        if float(result) < 1.0:
            manager.timer = 0
            manager.iteration_count = 0
            manager.state = manager.detect_object_and_speak
        else: 
            if manager.timer < (2):
                manager.timer += 1
                print("MANAGER_Timer: ", str(manager.timer))
                rospy.sleep(1)
            else:
                print("FALLIMENTO in WAITING OBJECT")
                manager.timer = 0
                manager.state = manager.iteration_failed
    

class DetectObjectAndSpeak(State):
    def handle(self, manager):
        print("\nSono Nello stato DETECT OBJECT AND SPEAK")
        if "ACK" != send_movement_head("down"):
            print("Movement Head DOWN failed")
        # DETECTION NODE
        obj = ""
        obj = detector_obj()

        if (obj != "ACK"):
            if "ACK" != send_movement_head("up"):
                print("Movement Head UP failed")
            if "ACK" != text_2_speech("L'oggetto che mi hai mostrato si chiama: " + obj):
                print("Speach failed: name object")
            if "ACK" != text_2_speech("Molto bene"):
                print("Speach failed: Molto bene")
            manager.state = manager.waiting_for_person
        else:
            if "ACK" != send_movement_head("up"):
                print("Movement Head UP failed")
            if "ACK" != text_2_speech("Non ho riconosciuto nessun oggetto"):
                print("Speach failed: Molto bene")
            manager.state = manager.speak_and_extend_arm

class IterationFailed(State):
    def handle(self, manager):
        print("\nSono Nello stato ITERATION FAILED")
        manager.iteration_count += 1
        if manager.iteration_count < 3:
            print("iteration_count: ", str(manager.iteration_count))
            manager.state = manager.speak_and_extend_arm
        else:
            if "ACK" != text_2_speech("Test Fallito, riproviamo a giocare..."):
                print("Speach failed: Molto bene")
            manager.state = manager.waiting_for_person
            manager.iteration_count = 0

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
        
        self.state = self.intro
        self.iteration_count = 0
        self.timer = 0
        self.i = 0
        self.rate_value = 10
        self.ack = "ACK"
        self.result = 0

    def run(self):
        while True:
            self.state.handle(self)

if __name__ == '__main__':
    rospy.init_node("project_manager")
    manager = ManagerNode()
    manager.run()
