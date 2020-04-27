import schedule, time
import os

def train_model():
    cmd = "train_model.sh"
    os.system(cmd)
    print("scheduled job executed")

schedule.every().day.at('04:00').do(train_model)

while 1:
    schedule.run_pending()
    print("********************* job is scheduled **************************************")
    time.sleep(1)
