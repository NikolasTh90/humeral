from matplotlib import pyplot as plt
import pickle
with open('imu_tag_4_data.pickle', 'rb') as file:
    data_list = pickle.load(file)
    accx_list = list()
    for data in data_list:
        accx_list.append(data['accx'])
    plt.plot(accx_list)
    plt.show()