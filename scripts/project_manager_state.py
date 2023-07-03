from abc import ABC, abstractmethod



def send_movement(argomento):
    return "ACK"

def request_distance():
    return 0.9  

def send_head_movement(argomento):
    return "ACK"

def text_2_speach(argomento):
    return "ACK"

def detector():
    return "cellulare"

# Classe astratta per il Pattern STATE
class State(ABC):
    @abstractmethod
    def handle(self, manager):
        pass

#Classe concreta per il Pattern STATE
class WaitingForPerson(State):
    def handle(self, manager):
        print("\nSono Nello stato 0")
        result = request_distance()
        if float(result) < 1.0:
            manager.state = manager.speak_and_extend_arm


class SpeakAndExtendArm(State):
    def handle(self, manager):
        print("\nSono Nello stato 1")
        if "ACK" != send_movement("up"):
            print("Movement UP failed")
        if "ACK" != text_2_speach("Fammi vedere"):
            print("Speach failed: Fammi vedere")
        if "ACK" != send_movement("down"):
            print("Movement DOWN failed")
        manager.state = manager.waiting_for_object

class WaitingForObject(State):
    def handle(self, manager):
        print("\nSono Nello stato 2")
        result = request_distance()
        if float(result) < 1.0:
            manager.timer = 0
            manager.state = manager.detect_object_and_speak
        else: 
            if manager.timer < (20 * manager.rate_value):
                manager.timer += 1
            else:
                manager.timer = 0
                manager.state = manager.iteration_failed

class DetectObjectAndSpeak(State):
    def handle(self, manager):
        print("\nSono Nello stato 3")
        if "ACK" != send_head_movement("down"):
            print("Movement Head DOWN failed")
        object_name = detector()
        if "ACK" != send_head_movement("up"):
            print("Movement Head UP failed")
        if "ACK" != text_2_speach(object_name):
            print("Speach failed: name object")
        if "ACK" != text_2_speach("Molto bene"):
            print("Speach failed: Molto bene")
        manager.state = manager.waiting_for_person

class IterationFailed(State):
    def handle(self, manager):
        print("\nSono Nello stato 4")
        manager.iteration_count += 1
        if manager.iteration_count <= 3:
            manager.state = manager.speak_and_extend_arm
        else:
            if "ACK" != text_2_speach("Fallimento"):
                print("Speach failed: fallimento")
            manager.state = manager.waiting_for_person
            manager.iteration_count = 0

class ManagerNode:
    def __init__(self):
        self.waiting_for_person = WaitingForPerson()
        self.speak_and_extend_arm = SpeakAndExtendArm()
        self.waiting_for_object = WaitingForObject()
        self.detect_object_and_speak = DetectObjectAndSpeak()
        self.iteration_failed = IterationFailed()
        
        self.state = self.waiting_for_person
        self.iteration_count = 0
        self.timer = 0
        self.i = 0
        self.rate_value = 10
        self.ack = "ACK"
        self.result = 0

    def run(self):
        while self.i < 5:
            self.i += 1
            self.state.handle(self)

if __name__ == '__main__':
    manager = ManagerNode()
    manager.run()


