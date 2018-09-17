import multiprocessing
import tobii_research as tr
import time
#from gaze import gaze_data_callback
import math

# Eye Tracker Initialization
found_eyetrackers = tr.find_all_eyetrackers()
my_eyetracker = found_eyetrackers[0]
print("Address: " + my_eyetracker.address)
print("Model: " + my_eyetracker.model)
print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
print("Serial number: " + my_eyetracker.serial_number)


    #from mean import gaze_data_callback
class eye(object):
    def __str__(self):
        def gaze_data_callback(gaze_data):
                left_3d = gaze_data['left_gaze_point_in_user_coordinate_system']
                right_3d = gaze_data['right_gaze_point_in_user_coordinate_system']
            #Get the gaze point of both eyes
                print('L3d:', left_3d)
                print('R3d:', right_3d)
                numbers = [0, 0, 0]
                numbers[0] = [left_3d[0], right_3d[0]]
                numbers[1] = [left_3d[1], right_3d[1]]
                numbers[2] = [left_3d[2], right_3d[2]]
                print(numbers)
                x = [0, 0, 0]
                x[0] = sum(numbers[0])
                x[1] = sum(numbers[1])
                x[2] = sum(numbers[2])
                x[0] = x[0]/2
                x[1] = x[1]/2
                x[2] = x[2]/2
                print(x)

                #gaze_point = ((left_3d), (right_3d))
                #gaze_point = tuple(np.mean(gaze_point, axis=0))
                #gaze_point = tuple(mean(gaze_point, axis=0))
                #print("3d gaze:",gaze_point)
                my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
                time.sleep(5)

                my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
        #Get the timestamp
                #timestamp = tr.get_system_time_stamp()
                #print(timestamp)
                return (x)
     
         #Working on 2D data
def test():
    #a=0
    while 1:
        #if 'gaze_point' in gaze_data_callback(gaze_data):
         #   data = gaze_data_callback['gaze_point']

          #  if s == 0:
           #     x = data[0] * 1920
            #    y = data[1] * 1080
             #   return [x, y]
        #a+=1
        for x in range(0, 10):
            print("We're on time %d" % (x))
        print('Waiting..')
        #time.sleep(5)

def datac():
    while 1:
        tmp = eye.__new__(eye)
        tmp.__init__()
        print(tmp)

#Multiprocessing
def main():

    p1 = multiprocessing.Process(name="p1", target=datac)
    p2 = multiprocessing.Process(name="p2", target=test)
    p1.start()
    p2.start()

if __name__ == "__main__":
   main()
