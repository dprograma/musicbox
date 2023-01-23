from datetime import date, datetime
import os


def tolog(val):
    val = str(val)
    file_path = os.path.abspath(__file__)
    print(file_path)
    logtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    opened_file = open("log.txt", "a")
    opened_file.write("\n")
    opened_file.write(logtime)
    opened_file.write("\n")
    opened_file.write(file_path)
    opened_file.write("\n")
    opened_file.write(val)
    opened_file.close()


    


