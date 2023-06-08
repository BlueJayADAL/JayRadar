import socket,cv2, pickle,struct
from boundingbox import draw_box_on_frame

# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '10.4.10.46' # paste your server ip address here
port = 9999
client_socket.connect((host_ip,port)) # a tuple
data = b""
payload_size = struct.calcsize("Q")

from networktables import NetworkTables

ip = '10.4.10.146'  #str(input('Enter the ip address'))

NetworkTables.initialize(server = ip)

nt = NetworkTables.getTable("JayRadar")


while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024) # 4K
        if not packet: break
        data+=packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q",packed_msg_size)[0]
    
    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size]
    data  = data[msg_size:]
    frame = pickle.loads(frame_data)
    
    objects_key = nt.getNumberArray('objects_key', [-1])
    print(objects_key)
    
    for index, key in enumerate(objects_key):
        name = 'object'+str(index)
        box_info = nt.getNumberArray(name, [-1])
        print(box_info)
        if box_info[0] == -1:
            break
        
        frame = draw_box_on_frame(frame.copy(), box_info)
    
    
    cv2.imshow("RECEIVING VIDEO",frame)
    key = cv2.waitKey(1) & 0xFF
    if key  == ord('q'):
        break
client_socket.close()
