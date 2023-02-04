from IMU import IMU
import time
import pyrr
import math
from pyvqf import PyVQF
import numpy as np
imu_tag0 = IMU('192.168.0.101', 0)
imu_tag4 = IMU('192.168.0.102',  4)
while True:
    if imu_tag0.quat9D is not None and imu_tag4.quat9D is not None:
        # change between quat9D and quat6D
        q1 = imu_tag0.quat9D 
        q2 = imu_tag4.quat9D
        
        # q_mul = pyrr.quaternion.dot(q1, pyrr.quaternion.inverse(q2))
        q_mul = PyVQF.quatMultiply(q1, PyVQF.quatConj(q2))
        print(q_mul)
        norm = np.linalg.norm(q_mul[:3],1)
        print(norm)
        try:
            theta = 2*math.asin(norm)
            print(math.degrees(theta))
        except:
            print("beyond limits")    
        
        # uncomment the line below to see the calculation of each message
        # print(time.time() - imu_tag0.start_time)
        # exit()
        #comment this line out when calculating times
        time.sleep(0.1)