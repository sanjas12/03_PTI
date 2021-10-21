from modbus.client import client
import time

c = client(host='localhost')
data = [0]
while True:
    time.sleep(1)

    r = c.read(FC=4, ADD=1000, LEN=1)
    # w = c.write(FC=16, ADD=2000, DAT=data)
    # data[0] = data[0] + 3
    print(r)
