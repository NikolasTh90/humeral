# This is a class that represents each IMU
# Make an instance of this class using the constructor IMU(ip, id), example: IMU('192.168.0.100',4)
# The default websocket url is 'ws://<ip>/ws' with the default port 80. The default frequency is 10
# Optionally you can set a custom url for the websocket connection or change the default frequency, example: IMU('192.168.0.100,4,url=http://192.168.0.100, hz=15)
import  websocket
import  threading
import numpy as np
from pyvqf import PyVQF
import pyrr, time
import pickle
class IMU:

    def save_data(self, filename=None):
        if not filename:
            filename = 'imu_tag_'+str(self.id)+'_data.pickle'             
        with open(filename, 'wb+') as file:
            pickle.dump(self.data_list, file)
        


# Updates the data dictionary of the IMU instance.
# in : data (the string from the websocket connection the IMU sends)
    def update_data(self, data):
        # create a new dictionary with appropriate tags
        keys = ['id', 'accx', 'accy', 'accz', 'gyrx', 'gyry', 'gyrz', 'magx', 'magy', 'magz']
        # split the string on ',' and put the values to the dictionary
        data = dict(zip(keys, data.split(',')))
        
        data['id'] = int(data['id'])
        data['accx'] = float(data['accx'])
        data['accy'] = float(data['accy'])
        data['accz'] = float(data['accz'])
        data['gyrx'] = float(data['gyrx'])
        data['gyry'] = float(data['gyry'])
        data['gyrz'] = float(data['gyrz'])
        data['magx'] = float(data['magx'])
        data['magy'] = float(data['magy'])
        data['magz'] = float(data['magz'])

        if self.id != int(data['id']):
            return
        self.data =  data 
        self.data_list.append(self.data)

    def listen_ws(self):
        self.ws.run_forever() 

    def on_message(self, ws, msg):
        # print("Message Arrived on "+ str(self.id) +":"  + msg)
        self.start_time = time.time()
        self.update_data(msg)
        self.save_data()
        # gyr = np.array([self.data['current']['gyrx'], self.data['current']['gyry'], self.data['current']['gyrz']])
        # acc = np.array([self.data['current']['accx'], self.data['current']['accy'], self.data['current']['accz']])
        # mag = np.array([self.data['current']['magx'], self.data['current']['magy'], self.data['current']['magz']])
        # self.vqf.update(gyr, acc, mag)
        # self.quat6D = self.vqf.getQuat6D()
        # self.quat9D = self.vqf.getQuat9D()
        # print(self.quat6D)
        



        # self.calculate_quaternion()

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("Connection Closed")

    # def on_open(ws):
    #     # ws.send("Hello!")
    #     pass

    def __init__(self, ip, id, url=None, hz = 10):
        self.ip = ip
        self.id = id
        self.url = url
        self.data = {}
        self.frequenzy = hz
        self.frequency_time = 1/hz
        self.vqf = PyVQF(self.frequency_time)
        self.quat6D = None
        self.quat9D = None
        self.start_time = 0
        self.data_list = []

        if not url:
            self.url = 'ws://' + self.ip + '/ws'
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp(self.url,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        # asyncio.get_event_loop().run_until_complete(self.listen())
        imu_data_thread = threading.Thread(target=self.listen_ws)
        imu_data_thread.start()                                   
        
        # asyncio.get_event_loop().run_forever()

