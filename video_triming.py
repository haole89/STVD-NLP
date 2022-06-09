from genericpath import exists
import os
from datetime import timedelta,datetime
import pandas as pd
from common import check_file, map_channel

# Global variables
# ------------------------------------------------
def runBash(command):
	os.system(command)
# ------------------------------------------------
def crop(start, end, input, output):
	str = "ffmpeg -i " + input + " -ss  " + start + " -to " + end + " -c copy " + output
	# print(str)
	runBash(str)
# ------------------------------------------------    
def resize_video(input, output):
    # ffmpeg -i movie.mp4 -vf scale=64:48 movie_360p.mp4
	str = "ffmpeg -i " + input + " -vf scale=64:48  "  + output
	# print(str)
	runBash(str)
# ------------------------------------------------
def str2datetime(str_timestamp):
    year_start = int(str_timestamp[:4])
    month_start = int(str_timestamp[4:6])
    day_start = int(str_timestamp[6:8])
    hour_start = int(str_timestamp[8:10])
    min_start = int(str_timestamp[10:12])
    second_start = int(str_timestamp[12:14])
    time_element = datetime(year=year_start, month=month_start, day=day_start, hour=hour_start, minute=min_start, second=second_start)
    return time_element
def main():
    print("--------Start program----------")
    # The video name format: c[0-7]_yyyymmdd_[video-audio].mp4
    # channel_list = ["c111", "c445", "c119", "c192", "c4", "c80", "c47", "c118"] 

    
    df = pd.read_csv("meta_data.csv")
    # The location of the original video (captured videos)
    video_path = r"E:\Fact_Checking\video_2"
    # Left padding in minutes
    # Right padding in minutes
    before_delta = 8
    after_delta = 12
    repeated_list = []
    # output path
    output_path = r"E:\trimming_02\\"
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    for row in df.itertuples():
        
        channel_code = str(row.Channel_Code)
        hashcode = str(row.Hashcode)
        timestamp = str(row.Start)
        time_element = str2datetime(timestamp)

        time_start = time_element - timedelta(minutes=before_delta)
        time_end = time_element + timedelta(minutes=after_delta)

        before_day = time_element - timedelta(days=1)

        time_start_hour = time_start.hour
        time_end_hour = time_end.hour
        time_start_min = time_start.minute
        time_end_min = time_end.minute

        if(time_start_hour == 23 and time_end_hour ==0):
            video_date = timestamp[:8]
            time_start_hour = time_start_hour - 6
            time_end_hour = time_end_hour + 18
        elif(time_start.hour >= 0 and time_start.hour <= 2):
            video_date = before_day.strftime("%Y%m%d")
            time_start_hour = time_start_hour + 18
            time_end_hour = time_end_hour + 18
        else:
            video_date = timestamp[:8]
            time_start_hour = time_start_hour - 6
            time_end_hour = time_end_hour - 6

        start_duration = str(time_start_hour) + ":" + str(time_start_min) + ":00"
        end_duration = str(time_end_hour) + ":" + str(time_end_min) + ":00"

        channel_c = map_channel(channel_code)
        output_filename = channel_c + "_" + timestamp + "_video.mp4"

        input_file = video_path + "\\" + channel_c + "_" + video_date + "_video.mp4"


        output_file = output_path + output_filename

        file_check = channel_c + "_" + video_date + "_video.mp4"
        # print(file_check,"------", video_path)
        if(check_file(file_check, video_path) == True):
            # trim video
            # crop(start_duration, end_duration, input_file, output_file)
            case = ({
                'Hashcode': hashcode,
                'Video_name': output_filename
            })
            repeated_list.append(case)

        # print("Timestamp: ", time_element, "Start: ", time_start, " End: ", time_end)


    df = pd.DataFrame(repeated_list)
    df.to_csv("segment.csv", index = False, header=True, encoding="utf-8-sig")

    print("---------End program----------")

if __name__ == "__main__":
    main()