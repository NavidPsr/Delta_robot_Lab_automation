import socket
import threading
import math

def server_thread():
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
    global state
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
        ss.bind((HOST, PORT))
        ss.listen()
        conn, addr = ss.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
                if(data == b"BreakBreak"):
                    os._exit(0)
                    
            zip()
                

def capture():
    global s 
    result = False
    try:
        s.settimeout(10000)  
#        s.connect((HOST, PORT))
        s.sendall(b"Home")
        data = s.recv(1024)
        if data==b"Done":
                s.sendall(b"Capture")
                data = s.recv(1024)
                if data==b"Done":
                    print("Done")
                    return True
                else:
                    return False
        else:
            return False
                    
     
    except Exception as e: 
        print("capture " + str(e))
        return False
    
def get_position():
    global s 
    try:
#        s.settimeout(10000)
#        s.connect((HOST, PORT))
        s.sendall(b"Get_Position")
        data = s.recv(1024).decode("utf-8")
        data = str(data)        
        data = data.split(",")
        return data
    except Exception as e:
        print(str(e) + " get_position")
        return False
    
def go_to(x,y,z):
    global s 
    try:
#        s.settimeout(20000)
#        s.connect((HOST, PORT))
        x_pre,y_pre,z_pre = list(map(float,get_position()))
        print(x_pre,y_pre,z_pre,"get position")
        distance1= math.sqrt((x_pre-x)**2+(y_pre-y)**2+(z_pre+350)**2)
        # print("distance " , distance1)
        if distance1 < 5.0:
            return True
                    
        string = f"Movej={x_pre:.2f},{y_pre:.2f},-350"
        # print(string)
        s.sendall(string.encode("utf-8"))
        data = s.recv(1024)
        if data==b"Done":
            print('Done') 
            string = f"Movej={x:.2f},{y:.2f},-350"
            # print(string)
            s.sendall(string.encode("utf-8"))
            data = s.recv(1024)
            if data==b"Done":
                print('Done') 
                string = f"Movej={x:.2f},{y:.2f},{z:.2f}"#{int(list_height[index]):.2f}
                s.sendall(string.encode("utf-8"))
                data = s.recv(1024)
                if data==b"Done":
                        print('Done') 
                        return True
        else:
            return False
    except Exception as e:
        print("go to " + str(e))
        return False

def move_to(x,y,z):
    global s 
    try:
        string = f"Movej={x:.2f},{y:.2f},{z:.2f}"
        s.sendall(string.encode("utf-8"))
        data = s.recv(1024)
        if(data == b"Done"):
            return True
        else:
            return False
    except Exception as e:
        print(e)
        #print('Error')
        return False
HOST = "192.168.0.150"  # The server's hostname or IP address
# HOST = "127.0.0.1"  # The server's hostname or IP address  change it************************************************
PORT = 810  # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("connected to controller")