import tobii_research as tr
import time
from numpy import mean
import numpy as np
import threading
import math
import csv

# Global Variables
gaze_position = (0, 0)
timestamp = 0
Sample_point_tuple = tuple()
interpolated_sample_point = ()
running = True
new_interpolated_list = []
Median_Cal_x = tuple()
Median_Cal_y = tuple()
noise_reduced = tuple()
velocity = tuple()
fixation_points = tuple()
# Screen size
screen_x = 31
screen_y = 17.5
# Calculated Threshold
threshold = 35

Max_Distance_Between_Fixation = 0.5
Max_Fixation_Duration = 1
Max_Time_Between_Fixation = 0.075
Min_Fixation_Duration = 0.1
FIXATION_POINTS = tuple()

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
        gaze_position = (gaze_position[0]*screen_x, gaze_position[1]*screen_y)
        #print('With mean:', gaze_position)
        timestamp = gaze_data['device_time_stamp']
        timestamp = timestamp/1000000


# Calling Gaze Function with timestamp
def call_gaze():
    print('I am call gaze process')
    #global gaze_position_2D_tuple
    global timestamp
    my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)


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
        median_y = np.median(Median_Cal_y)


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
        print('New Interpolated List:',new_interpolated_list)
        new_interpolated_list.append(median_tuple)
        i = len(new_interpolated_list)


        # Call Velocity Calculator
    velocity_calculator()


# Velocity Calculator Function
def velocity_calculator():
    global noise_reduced
    global threshold
    noise_reduced_temp = noise_reduced
    i = len(noise_reduced_temp)
    global velocity
    for k in range(0, i-2):
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
    print('Velocity:',velocity)
    fixation()


# Fixation Group Function
def fixation():
    global threshold
    global velocity
    global noise_reduced
    global fixation_points
    global Max_Distance_Between_Fixation
    global Max_Fixation_Duration
    global Max_Time_Between_Fixation
    global Min_Fixation_Duration
    global FIXATION_POINTS
    fixation_count = 0
    i = len(velocity)
    velocity = list(velocity)

    # Reading CSV File to find out the number of strokes
    with open(r"C:\Users\Admin\Desktop\Gestenkatalog.csv") as f:
        reader = csv.reader(f)
        data = ()
        for row in reader:
            data = data + tuple(row)
        separated = data[0].split(';')
        number_of_strokes = (len(separated) - 1)
    for k in range(0, i-1):
        # Checks if the velocity between two points is greater than the threshold velocity
        if velocity[i-1] > threshold:
            del velocity[i-1]
            #noise_reduced = list(noise_reduced)
            del noise_reduced[i]
           # noise_reduced = tuple(noise_reduced)
            i = len(velocity)
        else:
            length = len(fixation_points)
            # If the group is empty
            if len(fixation_points) == 0:
                fixation_points = fixation_points + (noise_reduced[i],)
                del velocity[i-1]
                noise_reduced = list(noise_reduced)
                del noise_reduced[i]
                noise_reduced = tuple(noise_reduced)
                i = len(velocity)
            else:
                del velocity[i-1]
                # time interval between the current being checked gaze point and
                # the last fixation point in the fixation list
                time_interval = (noise_reduced[i][2] - fixation_points[length - 1][2])
                # time interval between the current being checked gaze point and
                # the first fixation point in the fixation list
                time_sum = noise_reduced[i][2] - fixation_points[0][2]

                distance = math.sqrt((fixation_points[length - 1][0] - fixation_points[length - 2][0]) ** 2 +
                                     (fixation_points[length - 1][1] - fixation_points[length - 2][1]) ** 2)

                # If all 3 conditions satisfied, then we will add the point as fixation point
                if distance < Max_Distance_Between_Fixation and time_interval < Max_Time_Between_Fixation:
                        # If it's not the last fixation point
                    if (fixation_count < (number_of_strokes - 1)) and (time_sum < Max_Fixation_Duration):
                            fixation_points = fixation_points + (noise_reduced,)
                else:

                    # if the fixation group is long enough (enough fixation points) to be an eligible fixation group
                    if (fixation_points[length - 1][2] - fixation_points[0][2]) > Min_Fixation_Duration:
                        fixation_count = fixation_count + 1
                        # calculate the midpoint of the fixation group
                        x_average = 0
                        y_average = 0
                        for N in range(0, length - 1):
                            x_average = x_average + fixation_points[N][0]
                            y_average = y_average + fixation_points[N][1]
                        x_average = x_average / length
                        y_average = y_average / length
                        fixation_center_point = (x_average, y_average)

                        # save the midpoint of this fixation group into the special list (fixation center point list)
                        FIXATION_POINTS = FIXATION_POINTS + (fixation_center_point,)

                        # delete the list of current fixation points
                        del fixation_points
                        fixation_points = tuple()
                        # the current fixation point as the first fixation point of the next fixation group
                        fixation_points = fixation_points + (noise_reduced[i],)

                    # if there is not enough fixation points in the fixation group
                    else:
                        # this fixation group is invalid
                        del fixation_points
                        fixation_points = tuple()
                        # the current fixation point as the first fixation point of the next fixation group
                        fixation_points = fixation_points + (noise_reduced[i],)
            i = len(velocity)
        print('Fixation Points:', fixation_points)
        print('Mid-points:', FIXATION_POINTS)


# Multi-threading
def main():
    thread1 = threading.Thread(target=call_gaze)
    thread2 = threading.Thread(target=sp)
    thread3 = threading.Thread(target=interpolation)
    # Will execute them in parallel
    thread1.start()
    thread2.start()
    thread3.start()


if __name__ == "__main__":
        main()
