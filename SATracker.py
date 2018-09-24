import tobii_research as tr
import time
from numpy import mean
import threading

gaze_position = (0, 0)
timestamp = 0
gaze_position_2D_tuple = (gaze_position,)

# Eye Tracker Initialization
found_eyetrackers = tr.find_all_eyetrackers()
system_time_stamp = tr.get_system_time_stamp()
print("The system time stamp in microseconds is {0}.".format(system_time_stamp))
print(tr.EYETRACKER_GAZE_DATA)
my_eyetracker = found_eyetrackers[0]
print("Address: " + my_eyetracker.address)
print("Model: " + my_eyetracker.model)
print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
print("Serial number: " + my_eyetracker.serial_number)


# Getting Gaze Point
def gaze_data_callback(gaze_data):
        global gaze_position
        global timestamp
        left_eye = gaze_data['left_gaze_point_on_display_area']
        right_eye = gaze_data['right_gaze_point_on_display_area']
        gaze_position = (left_eye,right_eye)
        print('Without mean:', gaze_position)
        gaze_position = tuple(mean(gaze_position,axis=0))
        timestamp = gaze_data['device_time_stamp']
        timestamp = timestamp/1000000
        time.sleep(3)


# Calling Gaze Function with timestamp
def call_gaze():
    global gaze_position_2D_tuple
    my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

    while 1:
        print(gaze_position)
        gaze_position_2D_tuple = gaze_position_2D_tuple + (gaze_position,)
        print(gaze_position_2D_tuple)
        print(timestamp)
        ts = tr.get_system_time_stamp()/1000000
        print(ts)
        time.sleep(2)


# Random Test Function with the Timestamp
def test():
    while 1:
        for x in range(0, 10):
            print("We're on time %d" % (x))
            time.sleep(2)
        print('Waiting..')
        print(timestamp)
        ts = tr.get_system_time_stamp()/1000000
        print(ts)
        #time.sleep(5)


# Multi-threading
def main():
    thread1 = threading.Thread(target=call_gaze)
    thread2 = threading.Thread(target=test)
    # Will execute both in parallel
    thread1.start()
    thread2.start()

if __name__ == "__main__":
        gaze_position_2D = ()
        # gaze_position_2D_tuple = (0,)
        main()
