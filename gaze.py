import tobii_research as tr
import time
import math
from numpy import mean
from fractions import Fraction as fr
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
    # Print gaze points of left and right eye
        #print("Left eye 3d gaze: ({gaze_left_eye3d}) \t Right eye 3d gaze: ({gaze_right_eye3d})".format(
         #   gaze_left_eye3d=gaze_data['left_gaze_point_in_user_coordinate_system'],
          #  gaze_right_eye3d=gaze_data['right_gaze_point_in_user_coordinate_system']))

        #print("Left eye origin: ({gaze_left_eyeorig}) \t Right eye origin: ({gaze_right_eyeorig})".format(
         #   gaze_left_eyeorig=gaze_data['left_gaze_origin_in_user_coordinate_system'],
          #  gaze_right_eyeorig=gaze_data['right_gaze_origin_in_user_coordinate_system']))

        left_3d = gaze_data['left_gaze_point_in_user_coordinate_system']
        right_3d = gaze_data['right_gaze_point_in_user_coordinate_system']
        print(left_3d)
        print(type(left_3d))

        x = (left_3d, right_3d)
        print(x)
        print(type(x))
        a = tuple(mean(x,axis=0))
        print("3d gaze:",a)
        print(type(a))
        left_origin = gaze_data['left_gaze_origin_in_user_coordinate_system']
        right_origin = gaze_data['right_gaze_origin_in_user_coordinate_system']

my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
#my_eyetracker.subscribe_to(tr.EYETRACKER_EYE_IMAGES,eye_image_callback, as_dictionary=True)
time.sleep(5)

my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
