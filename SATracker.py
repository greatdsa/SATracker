import tobii_research as tr
import time
from numpy import mean
import threading

# Eye Tracker Initialization
found_eyetrackers = tr.find_all_eyetrackers()
my_eyetracker = found_eyetrackers[0]
print("Address: " + my_eyetracker.address)
print("Model: " + my_eyetracker.model)
print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
print("Serial number: " + my_eyetracker.serial_number)


# Getting Gaze Point
def gaze_data_callback(gaze_data):
        left_3d = gaze_data['left_gaze_point_in_user_coordinate_system']
        right_3d = gaze_data['right_gaze_point_in_user_coordinate_system']
        gaze_point = (left_3d, right_3d)
        gaze_point = tuple(mean(gaze_point,axis=0))
        print("3d gaze point:",gaze_point)


#Random Test Function
def test():
     while 1:
        for x in range(0, 10):
            print("We're on time %d" % (x))
        print('Waiting..')
        #time.sleep(5)

#Calling Gaze Function
def callgaze():
    my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
    while 1:
        time.sleep(0)


#Multithreading
def main():
    thread1 = threading.Thread(target=callgaze)
    thread2 = threading.Thread(target=test)
    # Will execute both in parallel
    thread1.start()
    thread2.start()
    # Joins threads back to the parent process, which is this program
    thread1.join()
    thread2.join()

if __name__ == "__main__":
        main()
