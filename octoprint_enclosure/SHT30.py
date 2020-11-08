import smbus
import time
import sys



if len(sys.argv) == 2 or len(sys.argv) == 3:
    address = int(sys.argv[1],16)
    if len(sys.argv) == 3:
        busNum = int(sys.argv[2],16)
    else:
        busNum = 1
else:
    print('-1 | -1')
    sys.exit(1)

# Get I2C bus
bus = smbus.SMBus(busNum)

#Write the read sensor command
bus.write_i2c_block_data(address, 0x2C, [0x06])
time.sleep(0.05) #This is so the sensor has tme to preform the mesurement and write its registers before you read it

# SHT30 address, 0x44(68)
# Read data back from 0x00(00), 6 bytes
# cTemp MSB, cTemp LSB, cTemp CRC, Humididty MSB, Humidity LSB, Humidity CRC
data = bus.read_i2c_block_data(address, 0x00, 6)

# Convert the data
cTemp = ((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45
fTemp = cTemp * 1.8 + 32
humidity = 100 * (data[3] * 256 + data[4]) / 65535.0


print('{0:0.1f} | {1:0.1f}'.format(cTemp, humidity))
