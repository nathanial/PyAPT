import serial
port = serial.Serial(raw_input("Port:"))
buffer = []

    # h = "%02X" % buffer[-1]
    # print h,

def unescape(buffer):
    return buffer
    i = 0
    new_buffer = []
    while i < len(buffer) - 2:
        if buffer[i] == 0x04 and buffer[i+1] == 0x04:
            new_buffer.append(0x04)
            i += 2
        else:
            new_buffer.append(buffer[i])
            i += 1
    new_buffer.append(buffer[-2])
    new_buffer.append(buffer[-1])
    return new_buffer

def print_data(buffer):
    buffer = unescape(buffer)
    print "DDD: %s" % (" ".join(["%02X" % x for x in buffer[1:-2]]),)

def print_from_buffer(): 
    global buffer
    if buffer[-1] == 0x04 and buffer[-2] == 0x06: 
        print "RAW: %s" % " ".join(["%02X" % x for x in buffer])
        if buffer[0] == 0x06:
            print_data(buffer)
        else:
            print ""
        buffer = []
        print ""


while True:
    c = ord(port.read())
    buffer.append(c)
    print_from_buffer()

