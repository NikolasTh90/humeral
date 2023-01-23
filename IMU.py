# var ws = new WebSocket("ws://192.168.10.186/ws");
# ws.onopen = function() {
# console.log("Connected");
# };
# ws.onmessage = function(evt) {
# console.log(evt.data);
# };

import websockets, websocket, json
import asyncio, threading
class IMU:

    def update_data(self, data):
        keys = ['id', 'accx', 'accy', 'accz', 'gyrx', 'gyry', 'gyrz', 'magx', 'magy', 'magz']
        data = dict(zip(keys, data.split(',')))
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
            # self.run_main_code()

    def listen_ws(self):
        self.ws.run_forever() 

    def on_message(self, ws, msg):
        print("Message Arrived:" + msg)
        self.update_data(msg)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("Connection Closed")

    # def on_open(ws):
    #     # ws.send("Hello!")
    #     pass

    def __init__(self, ip, id, url=None):
        self.ip = ip
        self.id = id
        self.url = url
        self.data = {'current': None, 'previous': None}
        if not url:
            self.url = 'ws://' + self.ip + '/ws'
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(self.url,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        # asyncio.get_event_loop().run_until_complete(self.listen())
        imu_data_thread = threading.Thread(target=self.listen_ws)
        imu_data_thread.start()                                   
        
        # asyncio.get_event_loop().run_forever()

