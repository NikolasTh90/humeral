from IMU import IMU
import time
imu_tag4 = IMU('127.0.0.1', 4, 'ws://127.0.0.1:1234')
imu_tag2 = IMU('127.0.0.1',  2,  'ws://127.0.0.1:1234')
time.sleep(5)
print(imu_tag4.data)
print(imu_tag2.data)