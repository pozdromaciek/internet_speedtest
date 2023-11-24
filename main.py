import speedtest
from datetime import datetime
import time
import csv
import matplotlib.pyplot as plt
import os
from os import system
import pandas as pd
system("title " + "Automatic SpeedTest Tool")

#Convert bytes to megabytes
def bytes2megabytes(bytes):
    KB = 1024
    MB = KB *1024
    return(bytes/MB)

#Welcome message
print("Welcome to Automatic Internet Speed Test")
interval = input("Set interval between tests (in sec): ")
print("Testing started, to stop testing and draw graph press CTRL + C")
#Open csv file
try:
    filename = "speedtest.csv"

    if os.path.exists(filename):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not

    output = open(filename, append_write, encoding='utf-8-sig', newline='')
    csv_writer = csv.writer(output, dialect='excel')
    try: 
        while True:
            time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            speed_test = speedtest.Speedtest(secure=True)
            download_speed = speed_test.download()
            upload_speed = speed_test.upload()
            test_output = [time_stamp, round(bytes2megabytes(download_speed), 2), round(bytes2megabytes(upload_speed),2)]
            csv_writer.writerow(test_output)
            print(str(time_stamp) + " " + str(round(bytes2megabytes(download_speed), 2)) + " " + str(round(bytes2megabytes(upload_speed),2)))
            time.sleep(int(interval))
    except KeyboardInterrupt:
        pass
    output.close()
    # Import data for the graph
    data = []
    timestamps = []  # New list to store only timestamps
    with open('speedtest.csv') as graph_input:
        data_reader = csv.reader(graph_input, delimiter=',')    
        # Skip the header
        next(data_reader)    
        # Add the remaining rows
        for row in data_reader:
            data.append(row)
            timestamps.append(row[0])  # Add timestamp to the new list

    # Drawing the graph
    data_frame = pd.DataFrame(data, columns=["Timestamp", "Download", "Upload"])
    data_frame["Timestamp"] = pd.to_datetime(data_frame["Timestamp"], format="%Y-%m-%d %H:%M:%S")
    data_frame["Download"] = pd.to_numeric(data_frame["Download"], errors='coerce')
    data_frame["Upload"] = pd.to_numeric(data_frame["Upload"], errors='coerce')

    # Draw a line plot
    plt.plot(data_frame["Timestamp"], data_frame["Download"], label="Download", marker='o')
    plt.plot(data_frame["Timestamp"], data_frame["Upload"], label="Upload", marker='o')

    # Uncomment this section if you prefer more detailed labels.
    # # Add labels with point values
    # for i, txt in enumerate(data_frame["Download"]):
    #     plt.annotate(txt, (data_frame["Timestamp"].iloc[i], data_frame["Download"].iloc[i]), ha='right', va='bottom')

    # for i, txt in enumerate(data_frame["Upload"]):
    #     plt.annotate(txt, (data_frame["Timestamp"].iloc[i], data_frame["Upload"].iloc[i]), ha='right', va='bottom')

    # # Set X-axis labels only to the values from the data
    # plt.xticks(data_frame["Timestamp"], rotation=45, ha='right')

    # Add labels and legend
    plt.xlabel("Timestamp")
    plt.ylabel("Speed")
    plt.legend()

    # Show the plot
    plt.show()
    output.close()  
except Exception as e:
    print(e)
    input("Press any key to exit")


