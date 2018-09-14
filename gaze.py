import tobii_research as tr
import time
import math
from statistics import mean
found_eyetrackers = tr.find_all_eyetrackers()

my_eyetracker = found_eyetrackers[0]
print("Address: " + my_eyetracker.address)
print("Model: " + my_eyetracker.model)
print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
print("Serial number: " + my_eyetracker.serial_number)


#def gaze_data_callback(gaze_data):
    # Print gaze points of left and right eye
 #   print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
  #      gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
   #     gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))

def gaze_data_callback(gaze_data):
     #Print gaze points of left and right eye
        #print("Left eye 3d gaze: ({gaze_left_eye3d}) \t Right eye 3d gaze: ({gaze_right_eye3d})".format(
         #   gaze_left_eye3d=gaze_data['left_gaze_point_in_user_coordinate_system'],
          #  gaze_right_eye3d=gaze_data['right_gaze_point_in_user_coordinate_system']))
   while 1:
        #print("Left eye origin: ({gaze_left_eyeorig}) \t Right eye origin: ({gaze_right_eyeorig})".format(
         #   gaze_left_eyeorig=gaze_data['left_gaze_origin_in_user_coordinate_system'],
          # gaze_right_eyeorig=gaze_data['right_gaze_origin_in_user_coordinate_system']))

        left_3d = gaze_data['left_gaze_point_in_user_coordinate_system']
        #print('L3d:', left_3d)
        right_3d = gaze_data['right_gaze_point_in_user_coordinate_system']
        #print('R3d:', right_3d)
        numbers = [0, 0,0]
        numbers[0] = [left_3d[0], right_3d[0]]
        numbers[1] = [left_3d[1], right_3d[1]]
        numbers[2] = [left_3d[2], right_3d[2]]
        #print(numbers)
        x = [0, 0, 0]
        x[0] = sum(numbers[0])
        x[1] = sum(numbers[1])
        x[2] = sum(numbers[2])
        x[0] = x[0]/2
        x[1] = x[1]/2
        x[2] = x[2]/2
        print(x)
        return x

   my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

#my_eyetracker.subscribe_to(tr.EYETRACKER_EYE_IMAGES,eye_image_callback, as_dictionary=True)
