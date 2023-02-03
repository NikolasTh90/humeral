# var ws = new WebSocket("ws://192.168.10.186/ws");
# ws.onopen = function() {
# console.log("Connected");
# };
# ws.onmessage = function(evt) {
# console.log(evt.data);
# };

import  websocket
import  threading
import numpy as np
from pyvqf import PyVQF
import pyrr
class IMU:

    def update_data(self, data):
        keys = ['id', 'accx', 'accy', 'accz', 'gyrx', 'gyry', 'gyrz', 'magx', 'magy', 'magz']
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
        if self.data['current'] is not None:
            self.data['previous'] = self.data['current']
        self.data['current'] =  data 



    # async def listen(self):
    #     async with websockets.connect('ws://127.0.0.1:1234') as conn:
    #         await conn.send('Hello, world')
            # message = await conn.recv()
            # print(message)
            # data = message
            # self.update_data(data)
            # print(self.data)
            # self.run_main_code()ß

    def listen_ws(self):
        self.ws.run_forever() 

    def on_message(self, ws, msg):
        # print("Message Arrived on "+ str(self.id) +":"  + msg)
        self.update_data(msg)
        gyr = np.array([self.data['current']['gyrx'], self.data['current']['gyry'], self.data['current']['gyrz']])
        acc = np.array([self.data['current']['accx'], self.data['current']['accy'], self.data['current']['accz']])
        mag = np.array([self.data['current']['magx'], self.data['current']['magy'], self.data['current']['magz']])
        self.vqf.update(gyr, acc, mag)
        # self.quat6D = self.vqf.getQuat6D()
        self.quat9D = self.vqf.getQuat9D()
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
        self.data = {'current': None, 'previous': None}
        self.frequenzy = hz
        self.frequency_time = 1/hz
        self.vqf = PyVQF(self.frequency_time)
        self.quat6D = None
        self.quat9D = None

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

