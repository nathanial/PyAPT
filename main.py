import serial, struct, crc16pure
port = serial.Serial("COM79")
buffer = []
print ""

def crc_is_correct(packet):
    data = packet[1:-4] #trim off packet wrapper
    print "DAT: %s" % " ".join(["%02X" % x for x in data])
    s = crc16pure.crc16([chr(x) for x in data])
    crcBytes = packet[-4:-2]
    crcBytes = "".join([chr(x) for x in crcBytes])
    crc = struct.unpack('h', crcBytes)
    print "checksum: expected %s, got %s" % (s, crc)
    return s == bytes

def top_end_unit_data(buffer):
    data = struct.unpack('bbHHHHhhhHhH',"".join([chr(x) for x in buffer]))
    return { 'TSUSTAT' : data[0],
             'AVG' : data[1],
             'REFROLL' : data[2],
             'MAGDEV' : data[3],
             'TOPVOLT' : data[4],
             'CURRENT' : data[5],
             'ROLL' : data[6],
             'MAGROLL' : data[7],
             'PITCH' : data[8],
             'TOTMAG' : data[9],
             'HEAD' : data[10],
             'TOTGRAV' : data[11] }

def heading_sensor_data(buffer):
    data = struct.unpack('bhhhhhhhh', "".join([chr(x) for x in buffer]))
    return { 'HEADSTATUS' : data[0],
             'MAGX' : data[1],
             'ACCX' : data[2],
             'MAGY' : data[3],
             'ACCY' : data[4],
             'MAGZ' : data[5],
             'ACCZ' : data[6],
             'TEMP' : data[7],
             'VOLT' : data[8] }

def escape(buffer):
    i = 0
    nbuf = []
    while i < len(buffer) - 2:
        if buffer[i] == 0x06 and buffer[i+1] == 0x06:
            nbuf.append(0x04)
            i += 2
        else:
            nbuf.append(buffer[i])
            i += 1
    nbuf.append(buffer[-2])
    nbuf.append(buffer[-1])
    return nbuf

def print_heading_sensor_data(buffer):
    print "<HEADING SENSOR DATA>"
    data = heading_sensor_data(buffer)
    for key in data.keys():
        print "    %s : %s" % (key, data[key])
    print "<HEADING SENSOR DATA>"

def print_top_end_unit_data(buffer):
    print "<TOP END UNIT DATA>"
    data = top_end_unit_data(buffer)
    for key in data.keys():
        print "    %s : %s" % (key, data[key])
    print "<TOP END UNIT DATA>"

def print_parsed_data(buffer):
    if buffer[0] == 0x01:
        print_heading_sensor_data(buffer)
    elif buffer[0] == 0x03:
        print_top_end_unit_data(buffer[1:])
    else:
        print "PPP: Not Supported"
        

def print_data(buffer):
    print "DDD: XX",
    print " ".join(["%02X" % x for x in buffer[1:-4]]),
    print "XXXXX",
    print "XXXXX"
    print_parsed_data(buffer[1:-4])


def print_from_buffer(): 
    global buffer
    if len(buffer) <= 3: return
    escaped = escape(buffer)
    if escaped[-1] == 0x04 and escaped[-2] == 0x06: 
        print "RAW: %s" % " ".join(["%02X" % x for x in buffer])
        if escaped[0] == 0x06:
            print_data(escaped)
        else:
            print "ERR: Malformed Packet"
        buffer = []
        print ""


while True:
    c = ord(port.read())
    buffer.append(c)
    print_from_buffer()

