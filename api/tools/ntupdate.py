from networktables import NetworkTables

ip = '10.1.32.27'  #str(input('Enter the ip address'))

NetworkTables.initialize(server = ip)

nt = NetworkTables.getTable("JayRadar")

while True:
    key = input('Enter a key: ')
    value = input('Enter a value: ')
    nt.putValue(key, value)