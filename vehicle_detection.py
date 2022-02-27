import cv2
from darkflow.net.build import  TFNet
import matplotlib.pyplot as plt 
import os
import sys
import time


options={
   'model':'./cfg/yolo.cfg',        #specifying the path of model
   'load':'./bin/yolov2.weights',   #weights
   'threshold':0.3                  #minimum confidence factor to create a box, greater than 0.3 good
}


tfnet=TFNet(options)
inputPath = os.getcwd() + "/test_images/"
outputPath = os.getcwd() + "/output_images/"


def countdown(delay,count):
  print("{} green".format(count))
  while delay:
    mins, secs = divmod(delay, 60)
    timer = '{:02d}:{:02d}'.format(mins, secs)
    print(timer, end="\r")
    time.sleep(1)
    delay -= 1
    if delay == 0:
      print("{} yellow".format(count))
      time.sleep(5)
      print("{} red".format(count))


      
def detection(filename,tfnet):
   global  inputPath, outputPath
   count_of_car=0
   count_of_bus=0
   count_of_bike=0
   count_of_truck=0
   count_of_rickshaw=0
   img=cv2.imread(inputPath+filename,cv2.IMREAD_COLOR)
   img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
   result=tfnet.return_predict(img)
   #print(result)
   for vehicle in result:
      label=vehicle['label']   #extracting label
      if(label=="car" or label=="bus" or label=="bike" or label=="truck" or label=="rickshaw"):    #drawing box and writing label
         top_left=(vehicle['topleft']['x'],vehicle['topleft']['y'])
         bottom_right=(vehicle['bottomright']['x'],vehicle['bottomright']['y'])
         img=cv2.rectangle(img,top_left,bottom_right,(0,255,0),3)    #green box of width 5
         img=cv2.putText(img,label,top_left,cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,0),1)   #image, label, position, font, font scale, colour: black, line width      
         if(label=="car"):
            count_of_car = count_of_car + 1
         elif(label=="bike"):
            count_of_bike = count_of_bike + 1
         elif(label=="bus"):
            count_of_bus = count_of_bus + 1
         elif(label=="truck"):
            count_of_truck =  count_of_truck + 1
         elif(label=="rickshaw"):
           count_of_rickshaw = count_of_rickshaw + 1
         total_vehicles_count = count_of_car + count_of_bike + count_of_bus + count_of_truck + count_of_rickshaw
   
   print("\n\n_________________________________________________")
   print("Output of file {}".format(filename))
   print("_________________________________________________")
   print("count of car : {}".format(count_of_car))
   print("count of bike : {}".format(count_of_bike))
   print("count of bus : {}".format(count_of_bus))
   print("count of truck : {}".format(count_of_truck))
   print("count of rickshaw : {}".format(count_of_rickshaw))
   print("Count of total vehiclies in {} : {}".format(filename,total_vehicles_count))
   print("_________________________________________________")
         
         
   outputFilename = outputPath + "output_" +filename
   cv2.imwrite(outputFilename,img)
   #plt.imshow(img)
   #plt.show()
   #return result
   return total_vehicles_count
 
def generate_signal():
  highest_total_vehicles=0
  list_of_total_vehicles = dict()
  for filename in os.listdir(inputPath):
    if(filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg")):
      count = detection(filename,tfnet)
      list_of_total_vehicles["Lane {}".format(str(filename))] = count
      if(highest_total_vehicles < count):
          highest_total_vehicles = count
          image = filename

  print(list_of_total_vehicles)
  print("_________________________________________________\n\n")
  print("image with highest traffic is {} and the count is {}".format(image,highest_total_vehicles))  
  print("_________________________________________________\n\n")
  print("Traffic signal timer") 
  for count in list_of_total_vehicles:
    print(list_of_total_vehicles[count])
    delay = list_of_total_vehicles[count] + 5
    countdown(delay,count)
    print("_________________________________________________\n\n")
    
generate_signal()