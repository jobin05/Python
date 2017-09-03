import sys
import telnetlib

HOST = "localhost"
tn = telnetlib.Telnet(HOST,3001)
tn.write("test\n")
tn.write("exit\n")
tn.sock.close()
tn.close()
