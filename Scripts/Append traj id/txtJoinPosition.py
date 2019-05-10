import glob
import pandas as pd


with open("final.txt", "w") as outfile:
        with open("Tracks-to-Trips-ft-BigGeo.txt", "r") as infile:
            line = infile.readline()
            trajID=-1
            taxi_idPrev = 1000000
            track_idPrev = 100000
            while line: 
                taxi_idSTR, longi ,lati, date, vel,track_idSTR, lngs,lats,lnge,late  = line.split(",")
                taxi_id = int(taxi_idSTR)    
                track_id = int(track_idSTR)    
                if(taxi_id == taxi_idPrev and track_id == track_idPrev):
                    outfile.write(taxi_idSTR + "," +  longi + "," + lati + "," +  date + "," +  vel + "," + track_idSTR + "," + lngs + "," + lats + "," + lnge + "," + late.strip() + "," + str(trajID)+"\n" )
               
                else:
                    print(taxi_idSTR + " " + track_idSTR + " and the other is: " + str(taxi_idPrev) + " " + str(track_idPrev))
                    taxi_idPrev = taxi_id
                    track_idPrev = track_id
                    trajID +=1
                    
                    outfile.write(taxi_idSTR + "," +  longi + "," + lati + "," +  date + "," +  vel + "," + track_idSTR + "," + lngs + "," + lats + "," + lnge + "," + late.strip() + "," + str(trajID)+"\n")
                    
                    
                line = infile.readline()
                
            
                

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
