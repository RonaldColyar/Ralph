import time
import threading
class TimeData:
	def __init__():
		self.running = True
		self.start_time = time.time()

class TimeTracker:
	def __init__(self):
		self.connection_one_clock = None
        self.connection_two_clock = None
    def check_elasped_time(self , clock,client):
        current_time = time.time()
        elasped_time = int(current_time -clock.start_time)
        #only can be connected to the proxy
        #without stating who you are for 20 seconds!
        while clock.running == True:
            if elasped_time >20 :
                client.close()
    def stop_timer(self ,num):
            if num == 1:
                self.connection_one_clock.running = False
            else:
                self.connection_two_clock.running = False
    def start_timer(self , client,num):
        thread = threading.Thread(target = self.monitor_timeout , args = (client,num))
        thread.start()

    def monitor_timeout(self, client , num):
        if num == 1:
            self.connection_one_clock == TimeData()
            self.check_elasped_time(self.connection_one_clock,client)
        else:
            self.connection_two_clock == TimeData()
            self.check_elasped_time(self.connection_two_clock, client)