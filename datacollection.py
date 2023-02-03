# import libraries
import serial
import numpy
import time
import datetime
import os
import serial.tools.list_ports
import sys

# this function will obtain the current ports
def get_ports():
  ports = serial.tools.list_ports.comports()
  return ports

# this function will iterate through each port and check if it is the arduino port
# --> this is decided based on the string 'usbserial' (appears in arduino ports)
# --> this string is then cleaned up so that it can be used in a subsequent function
def findArduino(portsFound):
  varr=0; # create variable to determine if finding port is complete
  commPort = 'None' # predetermined value for the port string
  n = len(portsFound) # find number of ports
  for i in range(0,n): # iterate throughout each port and check if it is connected

    # the following is a trimming of each port name
    port = portsFound[i]
    strPort = str(port)
    splitPort = strPort.split(' ')
    commPort = (splitPort[0])

    ser = serial.Serial(commPort, 115200) # connect to the current port
    ser.timeout = 1 # set timeout value
    
    timestart = time.perf_counter() # collect current run time
    state = 0; # variable that determines while loop status
    while state==0:
      i = "W" # create signal to send to the arduino
      ser.write(i.encode()) # write encoded string to serial port
      time.sleep(0.5) # wait
      string = ser.readline(1).decode('utf-8') # read decoded string back from serial port
      timeend = time.perf_counter() # collect current run time

      # if the received string from arduino is "A", then we know that it is in fact
      # connected and we can return the name of the port
      if string == "A":
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("     Connection established!     ")
        print("             Port: ", "      " + commPort, sep="\n")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        varr = 1 # set varriable value to 1 to signal that a port was in fact found
        return commPort # function returns name of the connected port

      # Per port, it takes roughly 2 seconds of reading and writing to the serial port
      # to establish a connection in these cases. Therefore, we wait roughly 2.5 seconds
      # per port to make sure that if the port is in fact correct we are actually
      # connecting to it.
      elif (timeend - timestart) < 2.5: # take difference of timestamps to get run time
        continue # continue with the while loop
      state=1 # end the while loop

  if varr == 0: # varr stays at 0 if no port connects
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Connection not established.", " --> Make sure that the USB is connected to the port and try again.",sep="\n")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    sys.exit() # exits the program

print("Processing...")
foundPorts = get_ports() # call the function to find the list of current ports
port = findArduino(foundPorts) # call the function using list of ports to obtain connected port name

arduinoData = serial.Serial(port, 115200) # connect to the viable port
time.sleep(2) # wait
arduinoData.write("W".encode()) # send "W" string back to arduino to start void loop (see arduino) code)

timenow = datetime.datetime.now() # gather date and time for file naming purposes
filename=timenow.strftime("%Y%m%d_%H%M") # name file based on time and date

# check if the output folder exists
currentpath = os.getcwd()
path = os.path.join(currentpath,"output_folder")
if os.path.isdir(path) == False:
  os.mkdir(path) # if the folder does not exist, then create the folder
foldername = "output_folder"
Filename = '' # placeholder for the file name

# this section of code prompts the user to input their desired file name for the data collection
# >> user is prompted to input a custom file name or use default naming system
# >> user is prompted to select a different name if their custom one is already taken
# >> a sub-folder is created in the output folder to hold the data in addition to future files based off of said txt file
check = 0
while check == 0:
  print(" ","What would you like to name the data file?",
      " --> Note: Empty input (press enter) receives default naming.",sep="\n")
  response = input("Filename: ")
  print("")

  # if the response is nothing (press enter), then file/folder are created based off of default name
  if (response == '') or (response == ' ') or (response == '  ') or (response == '   '): # if the response is a non-answer (spaces), keep default file name
    Filename = foldername+"/"+filename+"/"+filename+".txt" # create the default file name
    check = 1
    new = os.path.join(path,filename)
    os.mkdir(new)

  # if response is input, file/folder are created based off of default name
  else:
    response = response.replace(' ', '_').lower() # replace spaces with underscores for valid file name syntax
    Filename = foldername+"/"+response+"/"+response+".txt" # if response is typed, replace default file name with new one
    new = os.path.join(path,response)
    if os.path.exists(new) == True: # if the name already exists, then prompt user to input new name  
      print("This name is already taken, please choose another.")
    else:
      check = 1
      os.mkdir(new)

File = open(Filename,"a") # open file for input of data
File.write("Time Stamp(millisSeconds),pressure(PSI) \n") # create a header for the data

cnt = 0 # create variable for while loop status
print("Ready for measurements") # alert user that the code is ready to take measurements (data)
try:
    while(cnt==0):
        while(arduinoData.inWaiting()==0): # wait here until there is data
            pass # do nothing
        arduinoString = arduinoData.readline() # read line from serial port
        arduinoString = arduinoString.decode('utf-8') # decode data from bytes into string

        # the following if statements are used to notify the user when the end of an trial has occured
        if '*1' in arduinoString:
            print("Event 1")
        if '*2' in arduinoString:
            print("Event 2")
        if '*3' in arduinoString:
            print("Event 3")
        if '*4' in arduinoString:
            print("Event 4")
        if '*5' in arduinoString:
            print("Event 5")
        if '*6' in arduinoString:
            print("Event 6")
            cnt=1

        # 'A' that is sent from arduino further back is not read in this case 
        if 'A' not in arduinoString: # subject to change (for speed)
            File.write(arduinoString) # write the data to the file if there is not an 'A'
            #print(arduinoString) # last add
     
except KeyboardInterrupt:
    print('\nReceived Keyboard Interrupt')
finally:
    data="Number of Events = 6" # the number of events that occured
    File.write(data) # write the number of events
    File.close() # close the file that was open when writing the data to it
    print('Program finished')
  
  
