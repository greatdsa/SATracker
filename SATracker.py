import tobii_research as tr
import time
from numpy import mean
import threading

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
        print(type(gaze_data))


        left_3d = gaze_data['left_gaze_point_in_user_coordinate_system']
        right_3d = gaze_data['right_gaze_point_in_user_coordinate_system']
        gaze = {'left': left_3d , 'right': right_3d}
        #print(gaze)
        print(type(gaze))
        gaze_point = (left_3d, right_3d)
        gaze_point = tuple(mean(gaze_point,axis=0))
        print("3d gaze point:",gaze_point)
        time.sleep(3)
        return gaze


# Calling Gaze Function with timestamp
def call_gaze():
    my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
    print(a)
    while 1:
        print(tr.get_system_time_stamp())
        time.sleep(2)


# Random Test Function with the Timestamp
def test():
     while 1:
        for x in range(0, 10):
            print("We're on time %d" % (x))
            time.sleep(2)
        print('Waiting..')
        print(tr.get_system_time_stamp())
        #time.sleep(5)


# Multithreading
def main():
    thread1 = threading.Thread(target=call_gaze)
    thread2 = threading.Thread(target=test)
    # Will execute both in parallel
    thread1.start()
    thread2.start()
    # Joins threads back to the parent process, which is this program
    thread1.join()
    thread2.join()


if __name__ == "__main__":
        gaze_point_2d = []
        gaze_point_2D_list = []
        main()
