import tobii_research as tr
import time
from numpy import mean
import threading
import math

gaze_position = (0, 0)
timestamp = 0
#gaze_position_2D_tuple = (gaze_position,)
Sample_point_tuple = tuple()

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
        print('Left:',left_eye)
        print('Right:',right_eye)
        gaze_position = (left_eye, right_eye)
        gaze_position = tuple(mean(gaze_position, axis=0))
        print('With mean:', gaze_position)
        timestamp = gaze_data['device_time_stamp']
        timestamp = timestamp/1000


# Calling Gaze Function with timestamp
def call_gaze():
    #global gaze_position_2D_tuple
    global timestamp
    my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

    #while 1:
       # print('Gaze Position:',gaze_position)
        #gaze_position_2D_tuple = gaze_position_2D_tuple + (gaze_position,)
        #print(gaze_position_2D_tuple)
        #print(timestamp)

        # ts = tr.get_system_time_stamp()/1000000
        # print(ts)
       # time.sleep(2)


# Creating the tuple for sample points
def sp():
    global Sample_point_tuple
    global gaze_position
    global timestamp
    count = -1
    time.sleep(5)
    while 1:
        # time.sleep(1)
        if not (math.isnan(gaze_position[0]) and math.isnan(gaze_position[1])):
            Sample_point = (gaze_position[0],gaze_position[1], timestamp)
            Sample_point_tuple = Sample_point_tuple + (Sample_point,)
            print('Sample points:', Sample_point_tuple)

          #  sample_point_list = list(Sample_point_tuple)
          #  print(sample_point_list)


          #  list2 = sample_point_list[:]


          #  for item in sample_point_list:
          #      count += 1
          #      if item in list2:
         #           del sample_point_list[count]
           # Sample_point_list = tuple(Sample_point_tuple)
          #  print('Sample Points R:', sample_point_list)



# Random Test Function with the Timestamp
def test():
    while 1:
        for x in range(0, 10):
            print("We're on time %d" % (x))
            time.sleep(2)
        print('Waiting..')
        print(timestamp)
        # ts = tr.get_system_time_stamp()/1000000
       # print(ts)
      # time.sleep(5)


# Multi-threading
def main():
    thread1 = threading.Thread(target=call_gaze)
    thread2 = threading.Thread(target=test)
    thread3 = threading.Thread(target=sp)
    # Will execute both in parallel
    thread1.start()
    thread2.start()
    thread3.start()


if __name__ == "__main__":
        gaze_position_2D = ()
        # gaze_position_2D_tuple = (0,)
        main()
