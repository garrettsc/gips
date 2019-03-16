import serial.tools.list_ports


x = serial.tools.list_ports.comports()

print(x[0].device)