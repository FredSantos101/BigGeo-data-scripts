import glob
import pandas as pd
from datetime import datetime, date, time, timedelta


read_files = glob.glob("*.txt")

timeThreshold = timedelta(minutes=1, seconds=0)
timeThreshold1 = timedelta(minutes=0, seconds=0)
print( timeThreshold)
contFile = 1
with open("separateTracksByTime.txt", "w") as outfile:
    for f in read_files:
        
        with open(f, "r") as infile:
            print(contFile)
            contFile += 1
            equalToPrev = False
            firstTime = True
            line = infile.readline()
            lineNext = infile.readline()
            track_Cont = 0
            numPointInTrack = 0
            
            while (lineNext):
                if(lineNext == "\n"):
                    break
                
                
                #assign variables form each line
                
                taxi_id, date, longi ,lati = line.split(",")
                    
                taxi_id2, date2, longi2 ,lati2 = lineNext.split(",")
            
                # decode dates

                tstamp1 = datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
                tstamp2 = datetime.strptime(date2,'%Y-%m-%d %H:%M:%S')
                
                
                if(firstTime):
                    firstTime = False
                    if(timeThreshold1 <= tstamp2-tstamp1 <= timeThreshold):
                        numPointInTrack +=1
                        equalToPrev = True
                        outfile.write(taxi_id + "," + date + "," + '{0:.5f}'.format(float(longi)) + "," + '{0:.5f}'.format(float(lati)) + "," + str(track_Cont)+"\n")
                
                #if within threshold, place same track identifier
                elif(timeThreshold1 <= tstamp2-tstamp1 <= timeThreshold):
                    equalToPrev = True
                    numPointInTrack +=1
                    outfile.write(taxi_id + "," + date + "," + '{0:.5f}'.format(float(longi)) + "," + '{0:.5f}'.format(float(lati)) + "," + str(track_Cont)+"\n")
                else:
                    if (equalToPrev):
                        outfile.write(taxi_id + "," + date + "," + '{0:.5f}'.format(float(longi)) + "," + '{0:.5f}'.format(float(lati)) + "," + str(track_Cont)+"\n")
                    equalToPrev = False
                    track_Cont += 1    
                    numPointInTrack = 0
                    
            
                line = lineNext
                lineNext = infile.readline()
            
                

'''
PATH_INPUT='tracks.csv'
PATH_OUTPUT='dataset_output.csv'

if __name__ == "__main__":
    df = pd.read_csv(PATH_INPUT)
    
    df['points'] = df[['taxi_id','data_time','longitude', 'latitude']].groupby(['points'])['data_time','longitude', 'latitude'].transform(lambda x: ','.join(x))
    df[['taxi_id','data_time','longigute','latitude']].drop_duplicates()
    df.groupby('taxi_id').agg(lambda col: ''.join(col))
    print("ola")
    df.to_csv(PATH_OUTPUT, encoding='utf-8')
    print("skr")'''
