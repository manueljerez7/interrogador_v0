import pyvisa
import logging

rm = pyvisa.ResourceManager('@py')
dmm = rm.open_resource('TCPIP::10.0.0.10::3500::SOCKET')
print(dmm)
dmm.timeout = 5000
dmm.read_termination = '\r'
msg = dmm.query(':IDEN?')
print(msg)
