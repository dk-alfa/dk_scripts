#!/usr/bin/python3

'''

Описание:

 Этот скрипт формирует Отчет о резервном копировании 
копировании докер контейнеров за паредыдущий день

Создан Дмитрием Кораблевым

Дата создания:2023.02.01

'''

import sys
import os
import datetime
import json

PREAMBLE =      "  Отчет о резервном копировании backup файлов"
INI_FILE_NAME = f"/root/dk_scripts/reports_scripts/{os.path.basename(__file__).replace('_','').replace('.py','.json')}"
#INI_FILE_NAME = f"./{os.path.basename(__file__).replace('_','').replace('.py','.json')}"
PRINT_PREFIX  = f"{datetime.datetime.now()} [{os.path.basename(__file__)}]" 
SETTINGS      = {}
REP_FILE      = 0
MEGA_LOGIN    = "dkorablev@toyota-ufa.ru"
MEGA_PASS     = "nhbvbnbk"


#--- check_mega(fname,match_fname) ---
def check_mega(fname,match_fname):
  os.system(f"mega-login {MEGA_LOGIN} {MEGA_PASS}")
  ret = os.system(f"mega-ls {fname}/{match_fname}")
  os.system(f"mega-logout")
  
  if (ret == 0 ): 
    log_str  = f"{PRINT_PREFIX} Файл /Mega{fname}/{match_fname} найден [PASS]"
    log_str1 = f"    -  Файл /Mega{fname}/{match_fname} найден [PASS]"
  else: 
    log_str  = f"{PRINT_PREFIX} Файл /Mega{fname}/{match_fname}] НЕ  найден [FAIL !!!]"
    log_str1 = f"    -  Файл /Mega{fname}/{match_fname}] НЕ найден [FAIL !!!]"

  print(log_str)
  REP_FILE.write(f"{log_str1}\r\n")

# --- check_rfs(fname,match_fname) ---
def check_rfs(fname,match_fname):
  global REP_FILE
  os.system(f"sudo mount -t cifs {fname}")
  mount_point = fname
  mount_point = mount_point[mount_point.find(" "):len(mount_point)].lstrip()
  mount_point = mount_point[0:mount_point.find(" ")]
  src_path = f"{fname[0:fname.find(' ')]}"

  if (os.path.exists(f"{mount_point}/{match_fname}")): 
    log_str  = f"{PRINT_PREFIX} Файл {src_path}/{match_fname} найден [PASS]"
    log_str1 = f"    -  Файл {src_path}/{match_fname} найден [PASS]"
  else: 
    log_str  = f"{PRINT_PREFIX} Файл {src_path}/{match_fname} НЕ  найден [FAIL !!!]"
    log_str1 = f"    -  Файл {src_path}/{match_fname} НЕ  найден [FAIL !!!]"

  print(log_str)
  REP_FILE.write(f"{log_str1}\r\n")
  os.system(f"umount {mount_point}")

#--- check_fs(fname,match_fname) ---
def check_fs(fname,match_fname):
  global REP_FILE
  if (os.path.exists(f"{fname}/{match_fname}")): 
    log_str  = f"{PRINT_PREFIX} Файл {fname}/{match_fname} найден [PASS]"
    log_str1 = f"    -  Файл {fname}/{match_fname} найден [PASS]"
  else: 
    log_str  = f"{PRINT_PREFIX} Файл {fname}/{match_fname} НЕ  найден [FAIL !!!]"
    log_str1 = f"    -  Файл {fname}/{match_fname} НЕ  найден [FAIL !!!]"
  print(log_str)
  REP_FILE.write(f"{log_str1}\r\n")

#--- do_check(item) ---
def do_check(item):
#  fname = f"{item[0]}/{str(datetime.date.today().isoweekday())}_{item[1]}_{str(datetime.date.today()).replace('-','')}.tar"
  fname = f"{str(datetime.date.today().isoweekday())}_{item[1]}_{str(datetime.date.today()).replace('-','')}.tar"
  if (item[2] == "fs") : check_fs (item[0],fname)
  if (item[2] == "rfs"): check_rfs(item[0],fname)
  if (item[2] == "mega"): check_mega(item[0],fname)
  

#--- checking_files() ---
def checking_files():
  global  SETTINGS
  for item in SETTINGS["checks"]:
    do_check(item)
  

#--- read_settings() ---
def read_settings():
  global INI_FILE_NAME, SETTINGS
  try:
    ini_file = open(INI_FILE_NAME)
    try:
      SETTINGS = json.load(ini_file)
      print(f"{PRINT_PREFIX} прочитан файл настрек ")
    except:
      print(f"{PRINT_PREFIX} ошибка: не удалось прочитать файл настрек ")
    ini_file.close()
    return True
  except:
    print(f"{PRINT_PREFIX} ошибка: не удалось открыть файл настрек ")

#--- make_report() ---
def make_report():
  if ( read_settings()):
    checking_files()

#--- do_script(file_name) ---
def do_script(file_name):
  global REP_FILE
  REP_FILE = open(file_name,"w+")
  REP_FILE.write(PREAMBLE + "\r\n\r\n")
  make_report()
  REP_FILE.write("\r\n")
  REP_FILE.close()


if __name__ == "__main__":
  print("------------------------------------------------------------")
  print(f"{PRINT_PREFIX} start ")
  print("------------------------------------------------------------")
  try:
    filename = sys.argv[1] +  os.path.basename(__file__)
    filename = filename.replace(".py",".rep")
    do_script(filename)
  except: print ("Ошибка создания файла")
  print("------------------------------------------------------------")
  print(f"{PRINT_PREFIX} end")



