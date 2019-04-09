import glob
import pandas as pd
import datetime
from datetime import datetime, timedelta


read_files = glob.glob("*.txt")



cont = 0
with open("remove_Same_Time_Points.txt", "w") as outfile:
    for f in read_files:
        with open(f, "r") as infile:
            line = infile.readline()
            lineNext = infile.readline()
            fmt = '%Y-%m-%d %H:%M:%S'
            taxi_id3=100000
            taxi_id = 1000000
            trajNum3 = 100000
            
            tstamp3 = datetime.strptime("2001-01-01 00:00:01",fmt) 

            while (lineNext):
                if(lineNext == "\n"):
                    break
                
                
                #assign variables form each line

                taxi_id_Str, date, longit ,latit, trajNum = line.split(",")
                taxi_id = int(taxi_id_Str)    
                taxi_id2_Str, date2, longit2 ,latit2, trajNum2 = lineNext.split(",")
                taxi_id2 = int(taxi_id2_Str) 


                
                tstamp = datetime.strptime(date,fmt) 
                tstamp2 = datetime.strptime(date2,fmt) 

                #if within threshold, place same track identifier
                
                if(taxi_id == taxi_id2 and trajNum == trajNum2 and tstamp == tstamp2):
                    
                    if(tstamp!=tstamp3):
                        outfile.write(line)
                        taxi_id3 = taxi_id
                        trajNum3 = trajNum
                        tstamp3 = tstamp
                    else:
                        print(cont)
                        cont +=1
                        
                else:
                    if(taxi_id == taxi_id3 and trajNum == trajNum3 and tstamp == tstamp3):
                        print(cont)
                        cont +=1
                    else:
                        outfile.write(line)
                        taxi_id3 = taxi_id
                        trajNum3 = trajNum
                        tstamp3 = tstamp
                line = lineNext
                lineNext = infile.readline()
                
            if not (taxi_id == taxi_id3 and trajNum == trajNum3 and tstamp == tstamp3):    
                outfile.write(line)
 
