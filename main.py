import serial, struct, crc16pure
port = serial.Serial("COM79")
buffer = []
print ""

    # h = "%02X" % buffer[-1]
    # print h,

def escape(buffer):
    return buffer
    i = 0
    nbuf = []
    while i < len(buffer) - 2:
        if buffer[i] == 0x04 and buffer[i+1] == 0x04:
            nbuf.append(0x04)
            i += 2
        else:
            nbuf.append(buffer[i])
            i += 1
    nbuf.append(buffer[-2])
    nbuf.append(buffer[-1])
    return nbuf

def print_data(buffer):
    print "DDD: %s" % (" ".join(["%02X" % x for x in buffer[1:-2]]),)

def crc_is_correct(packet):
    data = packet[1:-4] #trim off packet wrapper
    print "DAT: %s" % " ".join(["%02X" % x for x in data])
    s = crc16pure.crc16([chr(x) for x in data])
    print s
    crcBytes = packet[-4:-2]
    crcBytes.reverse()
    print " ".join(["%02X" % x for x in crcBytes])
    crcBytes = "".join([chr(x) for x in crcBytes])
    crc = struct.unpack('H', crcBytes)
    print crc
    print "checksum: expected %s, got %s" % (s, crc)
    return s == bytes

def print_from_buffer(): 
    global buffer
    escaped = escape(buffer)
    if len(escaped) <= 3: return
    if escaped[-1] == 0x04 and escaped[-2] == 0x06: 
        print "RAW: %s" % " ".join(["%02X" % x for x in buffer])
        if escaped[0] == 0x06:
            if crc_is_correct(escaped):
                print_data(escaped)
            else:
                print "ERR: Bad Checksum"
        else:
            print "ERR: Malformed Packet"
        buffer = []
        print ""


while True:
    c = ord(port.read())
    buffer.append(c)
    print_from_buffer()

