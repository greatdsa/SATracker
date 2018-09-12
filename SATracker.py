import multiprocessing
import tobii_research as tr
import time
import math
from numpy import mean
import threading

#Eye Tracker Initialization
found_eyetrackers = tr.find_all_eyetrackers()
my_eyetracker = found_eyetrackers[0]
print("Address: " + my_eyetracker.address)
print("Model: " + my_eyetracker.model)
print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
print("Serial number: " + my_eyetracker.serial_number)


def gaze_data_callback(gaze_data):
        left_3d = gaze_data['left_gaze_point_in_user_coordinate_system']
        right_3d = gaze_data['right_gaze_point_in_user_coordinate_system']
#Get the gaze point of both eyes
        gaze_point = ((left_3d), (right_3d))
        gaze_point = tuple(mean(gaze_point, axis=0))
        print("3d gaze:",gaze_point)

#Get the timestamp
        timestamp = tr.get_system_time_stamp()
        return [gaze_point]

 #Working on 2D data
def data_collection():
    while running:
        if 'gaze_point' in gaze_data_callback():
            data = gaze_data_callback['gaze_point']

            if s == 0:
                x = data[0] * 1920
                y = data[1] * 1080
                return [x, y]


#Multiprocessing
if __name__ == "__main__":
    p1 = multiprocessing.Process(name="p1", target=gaze_data_callback)
    p2 = multiprocessing.Process(name="p2", target=data_collection)
    p1.start()
    p2.start()
