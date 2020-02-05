import socket
import grpc
from concurrent import futures
import Constants as CONST
from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
from gRPC import TrimTabMessages_pb2 as tt
from gRPC import TrimTabMessages_pb2_grpc as tt_grpc
import signal

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((CONST.OWN_IP, 50000))
s.listen(1)
conn, addr = s.accept()

aw_data = None # Apparent wind from Teensy
ca_data = None # Control angle for Teensy

class TrimTabGetterServicer(ms_grpc.TrimTabGetterServicer):
    def GetTrimTabSetting(self, request, context):
        ca_data = request.control_angle
        apparentWind = tt.ApparentWind()
        apparentWind.apparent_wind = aw_data
        return apparentWind


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
ms_grpc.add_TrimTabGetterServicer_to_server(TrimTabGetterServicer, server)
server.add_insecure_port('localhost:50051')
server.start()

try:
    while True:
        receivedData = tt.ApparentWind()
        receivedData.ParseFromString(conn.recv(32)) # Receiving a single float
        aw_data = receivedData.apparent_wind
        print("Apparent Wind: " + str(aw_data))
        if not aw_data:
            pass
        sendData = tt.ControlAngle()
        sendData.control_angle = input("Control Angle: ")
        conn.sendall(sendData.SerializeToString())
except KeyboardInterrupt:    
    conn.close()