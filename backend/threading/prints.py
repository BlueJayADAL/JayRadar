from network import nt_lock, config
import time

def print_tests():
    while True:
        time.sleep(1)
        with nt_lock:
            print("Print_Thread acquired lock")
            conf = config['conf']
            print("Print_Thread released lock")
        print(f'conf: {conf}')
    