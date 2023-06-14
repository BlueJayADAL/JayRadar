import threading
from network import frontend, network_setup_event
from prints import print_tests

network_thread = threading.Thread(target=frontend)
network_thread.start()

network_setup_event.wait()

print_thread = threading.Thread(target=print_tests)
print_thread.start()

print_thread.join()
