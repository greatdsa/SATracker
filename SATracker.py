import tobii_research as tr
import time
from numpy import mean
import threading
import math

# Global Variables
gaze_position = (0, 0)
timestamp = 0
#gaze_position_2D_tuple = (gaze_position,)
Sample_point_tuple = tuple()
interpolated_sample_point = ()

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
        #print('Left:',left_eye)
        #print('Right:',right_eye)
        gaze_position = (left_eye, right_eye)
        gaze_position = tuple(mean(gaze_position, axis=0))
        print('With mean:', gaze_position)
        timestamp = gaze_data['device_time_stamp']
        timestamp = timestamp/1000000


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
    gp = gaze_position
    time.sleep(1)
    while 1:
        time.sleep(0.01111111)
        if not (math.isnan(gaze_position[0]) and math.isnan(gaze_position[1])):
            Sample_point = (gaze_position[0], gaze_position[1], timestamp)
            Sample_point_tuple = Sample_point_tuple + (Sample_point,)
            print('Sample points:', Sample_point_tuple)
        while gaze_position == gp:
            time.sleep(0.01)
          #  print(len(Sample_point_tuple))
          #  sample_point_list = list(Sample_point_tuple)
          #  print(sample_point_list)
          #  list2 = sample_point_list[:]
          #  for item in sample_point_list:
          #      count += 1
          #      if item in list2:
         #           del sample_point_list[count]
           # Sample_point_list = tuple(Sample_point_tuple)
          #  print('Sample Points R:', sample_point_list)


# Gap Filling Function
def interpolation():
    global Sample_point_tuple
    global interpolated_sample_point
    time_parameter = 0.075
    timeout_limit = 1
    time.sleep(2)
    spt = Sample_point_tuple
    while 1:
        number_of_ts = len(Sample_point_tuple)
        if number_of_ts > 1:
            for i in range(0, number_of_ts):
                delta_ts = Sample_point_tuple[i][2] - Sample_point_tuple[i - 1][2]
                if delta_ts <= time_parameter:
                    interpolated_sample_point = interpolated_sample_point + (Sample_point_tuple[i],)
                    print('Interpolated Sample Points', interpolated_sample_point)
                    new_interpolated_list = list(interpolated_sample_point)
                    print('List of tuples:', new_interpolated_list)
                    # print(new_interpolated_list[1])
                    # print(time_parameter)
                elif delta_ts >= timeout_limit:
                    new_interpolated_list = list(interpolated_sample_point)
                    del new_interpolated_list[i-1]
                    print('List of tuples:', new_interpolated_list)
                else:
                    ts = int(delta_ts / time_parameter)
                    x = Sample_point_tuple[i][0] - Sample_point_tuple[i - 1][0]
                    x = x / 2
                    x = Sample_point_tuple[i - 1][0] + x
                    y = Sample_point_tuple[i][1] - Sample_point_tuple[i - 1][1]
                    y = y / 2
                    y = Sample_point_tuple[i][1] - Sample_point_tuple[i - 1][1]
                    new_interpolated_point = (x, y, ts)
                    interpolated_sample_point = interpolated_sample_point + (new_interpolated_point,)
                    print('Interpolated Sample Points', interpolated_sample_point)
                    new_interpolated_list = list(interpolated_sample_point)
                    print('List of tuples:', new_interpolated_list)
        while Sample_point_tuple == spt:
            print('Waiting spt')
            time.sleep(0.01)

        # print(len(interpolated_sample_point))
          #      loc_of_sp = i
           #     num_interpolation = int(delta_ts / time_parameter)
            #    a = len(i)
             #   for b in range(1,a)
              #      if num_interpolation == b:
               #         distance_of_ts[b] = delta_ts/(b+1)
                #        distance_of_second_ts = distance_of_first_ts * 2
                 #   elif num_interpolation == i+1:
                  #      distance_of_first_ts = delta_ts/
                   #     distance_of_second_ts = distance_of_first_ts * 2





# Multi-threading
def main():
    thread1 = threading.Thread(target=call_gaze)
    thread2 = threading.Thread(target=sp)
    thread3 = threading.Thread(target=interpolation)
    # Will execute both in parallel
    thread1.start()
    thread2.start()
    thread3.start()
 


if __name__ == "__main__":
        gaze_position_2D = ()
        # gaze_position_2D_tuple = (0,)
        main()
