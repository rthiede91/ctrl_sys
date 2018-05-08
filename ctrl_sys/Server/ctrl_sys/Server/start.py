import threading, sys, time
import init as init

class ServicesThread(threading.Thread):

    def __init__(self, cmd):
        threading.Thread.__init__(self)
        print ("New Service: ", cmd)
        
    def run(self):
        if cmd == 'server stop': 
            server(0)
        if cmd == 'ctrl start':
            server(1)
        if cmd == 'user start':
            server(2)
        if cmd == 'ctrl list': 
            server(3)
        if cmd == 'user list': 
            server(4)
        

def server(arg):
    if arg == 0:
        init.stop()
    if arg == 1:
        init.start_server_ctrl()
    if arg == 2:
        init.start_server_user()
    if arg == 3:
        init.list_ctrl()
    if arg == 4:
        init.list_user()

while True:
    time.sleep(1)
    try: 
        cmd = raw_input("CMD: ")
        newThread = ServicesThread(cmd)
        newThread.start()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
