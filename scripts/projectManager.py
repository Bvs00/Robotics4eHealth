import time
import subprocess


def main():
    status = subprocess.run(['python', 'arm_controller_service_client_up.py'] + ['up'], capture_output=True).stdout.strip().decode()

    if (status == "ACK"):
        print("Il braccio si è alzato correttamente")
    else:
        return 1

    time.sleep(5)
    status = subprocess.run(['python', 'arm_controller_service_client_up.py'] + ['down'], capture_output=True).stdout.strip().decode()

    if (status == "ACK"):
        print("Il braccio si è abbassato correttamente")
    else:
        return 1
    


if __name__ == "__main__":
    main()