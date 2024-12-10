#!/usr/bin/python3

'''
Скрипт создания backup конфигураций коммутаторов 
(c) Дмитрий Кораблев

    После отработки скрипта, в каталоге  BASE_TFTP_DIR/BACKUP_DIR содержатся файлы конфигурации
коммутаторов из списка

2024.01.11 Исправлено: корректное удаление каталога предидущего дня недели, замена на f стринги
2024.01.12 Исправлено: замена файла настроек на .json, перевод названия глобальных переменных в UpperCase

'''

import pexpect
import sys
import re
import datetime
import os
import fnmatch
import shutil
import json

INI_FILE_NAME = f"/root/dk_scripts/{os.path.basename(__file__).replace('_','').replace('.py','.json')}"
#INI_FILE_NAME = f"./{os.path.basename(__file__).replace('_','').replace('py','json')}"
SETTINGS = {} #Настройки

USERNAME       = "root"
PASSWORD       = "7e7acdee8A"
TFTP_SERVER_IP = "172.16.1.78"
BASE_TFTP_DIR  = "/docker/samba/data/public/backups/"
BACKUP_DIR     = "switches/"
CUR_DATE       = datetime.date.today()
CUR_DIR_NAME   = BASE_TFTP_DIR+BACKUP_DIR+"/"+str(datetime.date.today().isoweekday())+"_"


#---- datetime_message() ----
def datetime_message():
  return f"{datetime.datetime.now().replace(microsecond=0)} [{os.path.basename(__file__)}]"

#---- expect_sw(sw_ip_address) ----
def expect_sw(sw_ip_address):
  global CUR_DATE

  telnet = pexpect.spawn(f"telnet "+ sw_ip_address, timeout=20, encoding="utf-8")
  telnet.logfile = sys.stdout
  telnet.expect(":")
  telnet.sendline(USERNAME)
  telnet.expect(":")
  telnet.sendline(PASSWORD)
  telnet.expect("#")
  telnet.sendline()
  telnet.expect("#")
  s = telnet.before
  sw_name = re.sub(r'[^a-zA-Z0-9-]', '', s)[1:len(s)-1]
  CUR_DATE = str(CUR_DATE).replace('-','')
  copy_path = f"/{BACKUP_DIR}{str(datetime.date.today().isoweekday())}_{CUR_DATE}/{CUR_DATE}_{sw_name}_{sw_ip_address}.conf"
  cmd = "copy running-config tftp://"+TFTP_SERVER_IP+copy_path
  telnet.sendline(cmd)
  telnet.expect("#")
  telnet.sendline("exit")

#---- do_backups() ----
def do_backups():
  global SETTINGS
  for item in SETTINGS["switches_ip"]:
    expect_sw(item)

#--- create_dir() -----
def create_dir():
  global BASE_TFTP_DIR, BACKUP_DIR, CUR_DIR_NAME, CUR_DATE
 
  the_base_dir = BASE_TFTP_DIR+BACKUP_DIR
  dirs = os.listdir(BASE_TFTP_DIR+BACKUP_DIR)
  match = str(datetime.date.today().isoweekday())+"_*"

  for file in dirs:
    if fnmatch.fnmatch(file,match ) and os.path.isdir(the_base_dir+file):
      try:
        shutil.rmtree(the_base_dir+file)
      except OSError as e:
        print (f"{datetime_message()} Ошибка: {the_base_dir+file} {e.strerror} ")
  try:
    CUR_DIR_NAME = CUR_DIR_NAME+str(CUR_DATE).replace("-","")
    os.mkdir(CUR_DIR_NAME)
    os.chmod(CUR_DIR_NAME, 0o0777)
    return True
  except OSError:
    print (f"{datetime_message()} Ошибка: Создать директорию [{CUR_DIR_NAME}] не удалось")
    return False

#---- backup_configs() -----
def backup_configs():
   if create_dir():
     do_backups()

#---- read_settings() ----
def read_settings():
  global INI_FILE_NAME, SETTINGS
  try:
    ini_file = open (INI_FILE_NAME)
    try:
      SETTINGS = json.load(ini_file)
      print(f"{datetime_message()} Файл настроек [{INI_FILE_NAME}] прочитан ")
      return True
    except:
      print(f"{datetime_message()} Ошибка: Не удалось прочитать файл настроек [{INI_FILE_NAME}]")
    ini_file.close()
  except:
    print(f"{datetime_message()} Ошибка: Не удалось открыть файл настроек [{INI_FILE_NAME}]")
    return False
  
  
#---- run_script -----
def run_script():
  if(read_settings()):
    backup_configs()
#------- main ---------
if __name__ == "__main__":
  print(f"{datetime_message()} start")
  run_script()
  print(f"{datetime_message()} stop")
