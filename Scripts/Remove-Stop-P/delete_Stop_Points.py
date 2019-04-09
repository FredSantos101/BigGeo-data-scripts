import glob
import pandas as pd
import datetime
from datetime import datetime, timedelta


read_files = glob.glob("*.txt")



cont = 0
with open("remove_Stop_Points.txt", "w") as outfile:
    for f in read_files:
        with open(f, "r") as infile:
            line = infile.readline()
            lineNext = infile.readline()
            
            longi3 = lati3 = 0.0
            taxi_id3=100000
            trajNum3 = 100000

            while (lineNext):
                if(lineNext == "\n"):
                    break
                
                
                #assign variables form each line

                taxi_id, date, longit ,latit, trajNum = line.split(",")
                    
                taxi_id2, date2, longit2 ,latit2, trajNum2 = lineNext.split(",")

                longi = float(longit)
                longi2 = float(longit2)

                lati = float(latit)
                lati2 = float(latit2)


                fmt = '%Y-%m-%d %H:%M:%S'
                tstamp = datetime.strptime(date,fmt) 
                tstamp2 = datetime.strptime(date2,fmt) 

                #if within threshold, place same track identifier
                
                if(taxi_id == taxi_id2 and trajNum == trajNum2 and longi == longi2 and lati == lati2):
                    
                    if(longi3!=longi or lati3 != lati):
                        outfile.write(line)
                        longi3=longi
                        lati3 = lati
                        taxi_id3 = taxi_id
                        trajNum3 = trajNum
                    else:
                        print(cont)
                        cont +=1
                else:
                    if(taxi_id == taxi_id3 and longi == longi3 and lati == lati3 and trajNum == trajNum3):
                        print(cont)
                        cont +=1
                    else:
                        outfile.write(line)
                        longi3 = longi
                        lati3 = lati
                        taxi_id3 = taxi_id
                        trajNum3 = trajNum
                line = lineNext
                lineNext = infile.readline()
                
            if not (taxi_id == taxi_id3 and longi == longi3 and lati == lati3 and trajNum == trajNum3):    
                outfile.write(line)
                

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
