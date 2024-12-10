#!/usr/bin/python3
import os
import datetime

#---- datetime_message()  ----
def datetime_message():
  return f"{datetime.datetime.now().replace(microsecond = 0)} [{os.path.basename(__file__)}]"

#------ main --------
if __name__ == "__main__":
  print(f"{datetime_message()} start")
  print(f"{datetime_message()} stop")

