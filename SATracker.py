import tobii_research as tr
import time
from numpy import mean
import numpy as np
import threading
import math

# Global Variables
gaze_position = (0, 0)
timestamp = 0
#gaze_position_2D_tuple = (gaze_position,)
Sample_point_tuple = tuple()
interpolated_sample_point = ()
running = True
new_interpolated_list = []
Median_Cal_x = tuple()
Median_Cal_y = tuple()
noise_reduced = tuple()
velocity = tuple()
fixation_points = tuple()
# Calculated Threshold
threshold = 0.001

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
        #print('With mean:', gaze_position)
        timestamp = gaze_data['device_time_stamp']
        timestamp = timestamp/1000000


# Calling Gaze Function with timestamp
def call_gaze():
    print('I am call gaze process')
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
    print('I am sample point process')
    global Sample_point_tuple
    global gaze_position
    global timestamp
    gp = gaze_position
    time.sleep(1)
    while len(Sample_point_tuple) <= 19:
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
    print('I am Interpolation')
    global Sample_point_tuple
    global interpolated_sample_point
    global new_interpolated_list
    time_parameter = 0.075
    time_parameters = tuple()
    time_parameters = time_parameters + (0.075, 0.150, 0.225, 0.3, 0.375, 0.45, 0.525, 0.6, 0.675, 0.75, 0.825, 0.9,
                                         0.975)
    timeout_limit = 1
    time.sleep(2)
    spt = Sample_point_tuple
    #while len(Sample_point_tuple) <= 3:
    number_of_ts = len(Sample_point_tuple)
    if (number_of_ts > 1 and number_of_ts < 21):
        for i in range(0, number_of_ts):
            delta_ts = Sample_point_tuple[i][2] - Sample_point_tuple[i - 1][2]
            if delta_ts <= time_parameters[0]:
                interpolated_sample_point = interpolated_sample_point + (Sample_point_tuple[i],)
                print('Interpolated Sample Points', interpolated_sample_point)
                new_interpolated_list = list(interpolated_sample_point)
                print('List of tuples:', new_interpolated_list)
            elif delta_ts <= time_parameters[1]:
                num_of_points = int(delta_ts / time_parameter)
                for n in range(0, num_of_points):
                    ts = Sample_point_tuple[i][2] - Sample_point_tuple[i - 1][2]
                    ts = ts / num_of_points
                    ts = Sample_point_tuple[i - 1][2] + ts
                    x = Sample_point_tuple[i][0] - Sample_point_tuple[i - 1][0]
                    x = x / num_of_points
                    x = Sample_point_tuple[i - 1][0] + x
                    y = Sample_point_tuple[i][1] - Sample_point_tuple[i - 1][1]
                    y = y / num_of_points
                    y = Sample_point_tuple[i][1] +y
                    new_interpolated_point = (x, y, ts)
                    interpolated_sample_point = interpolated_sample_point + (new_interpolated_point,)
                    print('Interpolated Sample Points', interpolated_sample_point)
                    new_interpolated_list = list(interpolated_sample_point)
                    print('List of tuples:1 point inserted:', new_interpolated_list)
            elif delta_ts <= time_parameters[2]:
                num_of_points = int(delta_ts / time_parameter)
                for n in range(0, num_of_points):
                    ts = Sample_point_tuple[i][2] - Sample_point_tuple[i - 1][2]
                    ts = ts / num_of_points
                    ts = Sample_point_tuple[i - 1][2] + ts
                    x = Sample_point_tuple[i][0] - Sample_point_tuple[i - 1][0]
                    x = x / num_of_points
                    x = Sample_point_tuple[i - 1][0] + x
                    y = Sample_point_tuple[i][1] - Sample_point_tuple[i - 1][1]
                    y = y / num_of_points
                    y = Sample_point_tuple[i][1] +y
                    new_interpolated_point = (x, y, ts)
                    interpolated_sample_point = interpolated_sample_point + (new_interpolated_point,)
                    print('Interpolated Sample Points', interpolated_sample_point)
                    new_interpolated_list = list(interpolated_sample_point)
                    print('List of tuples: 2 points inserted:', new_interpolated_list)
            elif delta_ts <= time_parameters[3]:
                num_of_points = int(delta_ts / time_parameter)
                for n in range(0, num_of_points):
                    ts = Sample_point_tuple[i][2] - Sample_point_tuple[i - 1][2]
                    ts = ts / num_of_points
                    ts = Sample_point_tuple[i - 1][2] + ts
                    x = Sample_point_tuple[i][0] - Sample_point_tuple[i - 1][0]
                    x = x / num_of_points
                    x = Sample_point_tuple[i - 1][0] + x
                    y = Sample_point_tuple[i][1] - Sample_point_tuple[i - 1][1]
                    y = y / num_of_points
                    y = Sample_point_tuple[i][1] +y
                    new_interpolated_point = (x, y, ts)
                    interpolated_sample_point = interpolated_sample_point + (new_interpolated_point,)
                    print('Interpolated Sample Points:', interpolated_sample_point)
                    new_interpolated_list = list(interpolated_sample_point)
                    print('List of tuples:3 points inserted:', new_interpolated_list)
            elif delta_ts <= time_parameters[4]:
                num_of_points = int(delta_ts / time_parameter)
                for n in range(0, num_of_points):
                    ts = Sample_point_tuple[i][2] - Sample_point_tuple[i - 1][2]
                    ts = ts / num_of_points
                    ts = Sample_point_tuple[i - 1][2] + ts
                    x = Sample_point_tuple[i][0] - Sample_point_tuple[i - 1][0]
                    x = x / num_of_points
                    x = Sample_point_tuple[i - 1][0] + x
                    y = Sample_point_tuple[i][1] - Sample_point_tuple[i - 1][1]
                    y = y / num_of_points
                    y = Sample_point_tuple[i][1] +y
                    new_interpolated_point = (x, y, ts)
                    interpolated_sample_point = interpolated_sample_point + (new_interpolated_point,)
                    print('Interpolated Sample Points:', interpolated_sample_point)
                    new_interpolated_list = list(interpolated_sample_point)
                    print('List of tuples:4 points inserted:', new_interpolated_list)
            elif delta_ts <= time_parameters[5]:
                num_of_points = int(delta_ts / time_parameter)
                for n in range(0, num_of_points):
                    ts = Sample_point_tuple[i][2] - Sample_point_tuple[i - 1][2]
                    ts = ts / num_of_points
                    ts = Sample_point_tuple[i - 1][2] + ts
                    x = Sample_point_tuple[i][0] - Sample_point_tuple[i - 1][0]
                    x = x / num_of_points
                    x = Sample_point_tuple[i - 1][0] + x
                    y = Sample_point_tuple[i][1] - Sample_point_tuple[i - 1][1]
                    y = y / num_of_points
                    y = Sample_point_tuple[i][1] +y
                    new_interpolated_point = (x, y, ts)
                    interpolated_sample_point = interpolated_sample_point + (new_interpolated_point,)
                    print('Interpolated Sample Points:', interpolated_sample_point)
                    new_interpolated_list = list(interpolated_sample_point)
                    print('List of tuples:5 points inserted:', new_interpolated_list)
            elif delta_ts <= time_parameters[6]:
                num_of_points = int(delta_ts / time_parameter)
                for n in range(0, num_of_points):
                    ts = Sample_point_tuple[i][2] - Sample_point_tuple[i - 1][2]
                    ts = ts / num_of_points
                    ts = Sample_point_tuple[i - 1][2] + ts
                    x = Sample_point_tuple[i][0] - Sample_point_tuple[i - 1][0]
                    x = x / num_of_points
                    x = Sample_point_tuple[i - 1][0] + x
                    y = Sample_point_tuple[i][1] - Sample_point_tuple[i - 1][1]
                    y = y / num_of_points
                    y = Sample_point_tuple[i][1] +y
                    new_interpolated_point = (x, y, ts)
                    interpolated_sample_point = interpolated_sample_point + (new_interpolated_point,)
                    print('Interpolated Sample Points:', interpolated_sample_point)
                    new_interpolated_list = list(interpolated_sample_point)
                    print('List of tuples:6 points inserted:', new_interpolated_list)
            elif delta_ts <= time_parameters[7]:
                num_of_points = int(delta_ts / time_parameter)
                for n in range(0, num_of_points):
                    ts = Sample_point_tuple[i][2] - Sample_point_tuple[i - 1][2]
                    ts = ts / num_of_points
                    ts = Sample_point_tuple[i - 1][2] + ts
                    x = Sample_point_tuple[i][0] - Sample_point_tuple[i - 1][0]
                    x = x / num_of_points
                    x = Sample_point_tuple[i - 1][0] + x
                    y = Sample_point_tuple[i][1] - Sample_point_tuple[i - 1][1]
                    y = y / num_of_points
                    y = Sample_point_tuple[i][1] +y
                    new_interpolated_point = (x, y, ts)
                    interpolated_sample_point = interpolated_sample_point + (new_interpolated_point,)
                    print('Interpolated Sample Points:', interpolated_sample_point)
                    new_interpolated_list = list(interpolated_sample_point)
                    print('List of tuples:7 points inserted:', new_interpolated_list)
            elif delta_ts <= time_parameters[8]:
                num_of_points = int(delta_ts / time_parameter)
                for n in range(0, num_of_points):
                    ts = Sample_point_tuple[i][2] - Sample_point_tuple[i - 1][2]
                    ts = ts / num_of_points
                    ts = Sample_point_tuple[i - 1][2] + ts
                    x = Sample_point_tuple[i][0] - Sample_point_tuple[i - 1][0]
                    x = x / num_of_points
                    x = Sample_point_tuple[i - 1][0] + x
                    y = Sample_point_tuple[i][1] - Sample_point_tuple[i - 1][1]
                    y = y / num_of_points
                    y = Sample_point_tuple[i][1] +y
                    new_interpolated_point = (x, y, ts)
                    interpolated_sample_point = interpolated_sample_point + (new_interpolated_point,)
                    print('Interpolated Sample Points:', interpolated_sample_point)
                    new_interpolated_list = list(interpolated_sample_point)
                    print('List of tuples:8 points inserted:', new_interpolated_list)
            elif delta_ts <= time_parameters[9]:
                num_of_points = int(delta_ts / time_parameter)
                for n in range(0, num_of_points):
                    ts = Sample_point_tuple[i][2] - Sample_point_tuple[i - 1][2]
                    ts = ts / num_of_points
                    ts = Sample_point_tuple[i - 1][2] + ts
                    x = Sample_point_tuple[i][0] - Sample_point_tuple[i - 1][0]
                    x = x / num_of_points
                    x = Sample_point_tuple[i - 1][0] + x
                    y = Sample_point_tuple[i][1] - Sample_point_tuple[i - 1][1]
                    y = y / num_of_points
                    y = Sample_point_tuple[i][1] +y
                    new_interpolated_point = (x, y, ts)
                    interpolated_sample_point = interpolated_sample_point + (new_interpolated_point,)
                    print('Interpolated Sample Points:', interpolated_sample_point)
                    new_interpolated_list = list(interpolated_sample_point)
                    print('List of tuples:9 points inserted:', new_interpolated_list)
            elif delta_ts <= time_parameters[10]:
                num_of_points = int(delta_ts / time_parameter)
                for n in range(0, num_of_points):
                    ts = Sample_point_tuple[i][2] - Sample_point_tuple[i - 1][2]
                    ts = ts / num_of_points
                    ts = Sample_point_tuple[i - 1][2] + ts
                    x = Sample_point_tuple[i][0] - Sample_point_tuple[i - 1][0]
                    x = x / num_of_points
                    x = Sample_point_tuple[i - 1][0] + x
                    y = Sample_point_tuple[i][1] - Sample_point_tuple[i - 1][1]
                    y = y / num_of_points
                    y = Sample_point_tuple[i][1] +y
                    new_interpolated_point = (x, y, ts)
                    interpolated_sample_point = interpolated_sample_point + (new_interpolated_point,)
                    print('Interpolated Sample Points:', interpolated_sample_point)
                    new_interpolated_list = list(interpolated_sample_point)
                    print('List of tuples:10 points inserted:', new_interpolated_list)
            elif delta_ts <= time_parameters[11]:
                num_of_points = int(delta_ts / time_parameter)
                for n in range(0, num_of_points):
                    ts = Sample_point_tuple[i][2] - Sample_point_tuple[i - 1][2]
                    ts = ts / num_of_points
                    ts = Sample_point_tuple[i - 1][2] + ts
                    x = Sample_point_tuple[i][0] - Sample_point_tuple[i - 1][0]
                    x = x / num_of_points
                    x = Sample_point_tuple[i - 1][0] + x
                    y = Sample_point_tuple[i][1] - Sample_point_tuple[i - 1][1]
                    y = y / num_of_points
                    y = Sample_point_tuple[i][1] +y
                    new_interpolated_point = (x, y, ts)
                    interpolated_sample_point = interpolated_sample_point + (new_interpolated_point,)
                    print('Interpolated Sample Points:', interpolated_sample_point)
                    new_interpolated_list = list(interpolated_sample_point)
                    print('List of tuples:11 points inserted:', new_interpolated_list)
            elif delta_ts <= time_parameters[12]:
                num_of_points = int(delta_ts / time_parameter)
                for n in range(0, num_of_points):
                    ts = Sample_point_tuple[i][2] - Sample_point_tuple[i - 1][2]
                    ts = ts / num_of_points
                    ts = Sample_point_tuple[i - 1][2] + ts
                    x = Sample_point_tuple[i][0] - Sample_point_tuple[i - 1][0]
                    x = x / num_of_points
                    x = Sample_point_tuple[i - 1][0] + x
                    y = Sample_point_tuple[i][1] - Sample_point_tuple[i - 1][1]
                    y = y / num_of_points
                    y = Sample_point_tuple[i][1] +y
                    new_interpolated_point = (x, y, ts)
                    interpolated_sample_point = interpolated_sample_point + (new_interpolated_point,)
                    print('Interpolated Sample Points:', interpolated_sample_point)
                    new_interpolated_list = list(interpolated_sample_point)
                    print('List of tuples:12 points inserted:', new_interpolated_list)
            elif delta_ts >= timeout_limit:
                new_interpolated_list = list(interpolated_sample_point)
                del new_interpolated_list[i-1]
                print('List of tuples: 1 point deleted:', new_interpolated_list)
            else:
                print('Invalid data')
        #while Sample_point_tuple == spt:
            #print('Waiting spt')
          #  time.sleep(0.01)
    noise_reduction()

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


# Noise Reduction Function
def noise_reduction():
    print('I am Noise Reduction')
    global new_interpolated_list
    global Median_Cal_x
    global Median_Cal_y
    global noise_reduced
    i = len(new_interpolated_list)

    for k in range(0, i-2):
        # print('I am i:length of new interpoalted:',i)
        # add X-coordinate of 3 sequential gaze positions into the special list (median calculation for X)
        Median_Cal_x = Median_Cal_x + (new_interpolated_list[i - 3][0],)
        Median_Cal_x = Median_Cal_x + (new_interpolated_list[i - 2][0],)
        Median_Cal_x = Median_Cal_x + (new_interpolated_list[i - 1][0],)

        # add Y-coordinate of 3 sequential gaze positions into the special list (median calculation for Y)
        Median_Cal_y = Median_Cal_y + (new_interpolated_list[i - 3][1],)
        Median_Cal_y = Median_Cal_y + (new_interpolated_list[i - 2][1],)
        Median_Cal_y = Median_Cal_y + (new_interpolated_list[i - 1][1],)

        # calculate the median of 3 gaze points
        median_x = np.median(Median_Cal_x)
       # print('Median of x:',median_x)
        median_y = np.median(Median_Cal_y)
       # print('Median of y:', median_y)

        # empties the tuple
        del Median_Cal_x, Median_Cal_y
        Median_Cal_x = tuple()
        Median_Cal_y = tuple()

        # create tuple for the median position (x,y,t)
        median_tuple = (median_x, median_y, new_interpolated_list[i - 2][2],)
        noise_reduced = noise_reduced + (median_tuple,)
        print('Noise Reduced:', noise_reduced)
        gaze_last = new_interpolated_list[i - 1]

        # delete the last two gaze points from the gaze point list
        del new_interpolated_list[i-1], new_interpolated_list[i - 2]

       #  new_interpolated_list = tuple(new_interpolated_list)
        print('New Interpolated List:',new_interpolated_list)
        new_interpolated_list.append(median_tuple)
        #print(new_interpolated_list)
        #print('Before:',i)
        i = len(new_interpolated_list)
        #i = i - 1
        #print('After:',i)
        # add the median point into the gaze point list
        # print(type(new_interpolated_list))
        # print(new_interpolated_list)
        # new_interpolated_list.append(gaze_point_2d)
        # print(new_interpolated_list)

        # add the original last gaze point
        # new_interpolated_list.append(gaze_last)
        # new_interpolated_list = tuple(new_interpolated_list)
        # print(new_interpolated_list)
        # new_interpolated_list = tuple(mean(new_interpolated_list, axis=0))
        # print('Noise Reduced:', new_interpolated_list)

        # Call Velocity Calculator
    velocity_calculator()


# Velocity Calculator Function
def velocity_calculator():
    global noise_reduced
    global threshold
    noise_reduced_temp = noise_reduced
    i = len(noise_reduced_temp)
    global velocity
    for k in range (0, i-2):
        # Calculating the distance
        distance = math.sqrt((noise_reduced_temp[i-1][0] - noise_reduced_temp[i-2][0])**2 +
                (noise_reduced_temp[i-1][1] - noise_reduced_temp[i-2][1])**2)
        # Calculating the time
        time = float(noise_reduced_temp[i-1][2] - noise_reduced_temp[i-2][2])

        # Converting noise reduced tuple to list in order to delete the last point
        noise_reduced_temp = list(noise_reduced_temp)

        del noise_reduced_temp[i-1]
        i = len(noise_reduced_temp)
        # adding the calculated velocity to the tuple of velocity
        velocity = velocity + (abs(distance / time),)
    velocity = list(velocity)
    velocity = tuple(velocity)
    print('Velocity:',velocity)
    fixation()


def fixation():
    global threshold
    global velocity
    global noise_reduced
    global fixation_points
    i = len(velocity)
    j = len(noise_reduced)
    noise_reduced = list(noise_reduced)
    velocity = list(velocity)
    for k in range(0, i-1):
        if velocity[i-1] > threshold:
            del velocity[i-1]
            del noise_reduced[i]
            i = len(velocity)
        else:
            fixation_points = fixation_points + (noise_reduced[i],)
            del velocity[i-1]
            del noise_reduced[i]
            i = len(velocity)
            print('Fixation Point:',fixation_points)




# Multi-threading
def main():
    thread1 = threading.Thread(target=call_gaze)
    thread2 = threading.Thread(target=sp)
    thread3 = threading.Thread(target=interpolation)
    #thread4 = threading.Thread(target=noise_reduction)
    # Will execute both in parallel
    thread1.start()
    thread2.start()
    thread3.start()
    #thread4.start()


if __name__ == "__main__":
        gaze_position_2D = ()
        # gaze_position_2D_tuple = (0,)
        main()
