import glob
import pandas as pd
import datetime


read_files = glob.glob("*.txt")

timeThreshold = datetime.timedelta(minutes=7, seconds=0)
print( timeThreshold)
cont = 0
with open("delete1Point.txt", "w") as outfile:
    for f in read_files:
        with open(f, "r") as infile:

            line = infile.readline()
            lineNext = infile.readline()
            
            numPointInTrack = 0
            lastID = 15000
            lastTrajNum = 100000
            lastEqual = False
            while (lineNext):
                if(lineNext == "\n"):
                    break
                
                
                #assign variables form each line

                taxi_id, date, longi ,lati, trajNum = line.split(",")
                    
                taxi_id2, date2, longi2 ,lati2, trajNum2 = lineNext.split(",")

                
                #if same id and track num
                if(taxi_id == taxi_id2 and trajNum == trajNum2):
                    numPointInTrack +=1
                    outfile.write(line)
                    lastEqual= True


                else:
                    if(lastEqual):
                        lastEqual = False
                        numPointInTrack +=1
                        outfile.write(line)
                    else:
                        lastEqual = False
                        cont += 1
                        print(cont)
                   
                    
            
                line = lineNext
                lineNext = infile.readline()
            if(lastEqual):
                outfile.write(line)



                
                
                
                
