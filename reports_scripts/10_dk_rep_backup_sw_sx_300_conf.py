#!/usr/bin/python3

'''

Описание:

 Этот скрипт формирует Отчет о резервном копировании 
конфигурационных файлов коммутаторов коммутаторов за паредыдущий день.
Скрипт запускается с аргументом - папка с файлами отчетов [/root/dk_scripts/reports/2024-01-15]

Создан Дмитрием Кораблевым

Дата создания:2023.02.01
2024.01.15 Добавлено: datetime_message(), настроена работа с json файлом настройки

'''

import sys
import os
import datetime
import re
import json

PREAMBLE           = "  Отчет о резервном копировании конфигурационных файлов коммутаторов:"
INI_FILE_NAME      = "/root/dk_scripts/10dkscrbcpswsx300conf.json"
#LIST_SWITCHES_FILE = "/root/dk_scripts/list_sw_sx300" 
BACKUP_PATH        = "/docker/samba/data/public/backups/switches/"
SETTINGS = {}

#---- read_settings - ---
def read_settings(ini_file):
  global SETTINGS
  SETTINGS = json.load(ini_file)

#--- datetime_message() ---
def datetime_message():
  return f"{datetime.datetime.now()} [{os.path.basename(__file__)}]"

#---- do_script(file_name) ----
def do_script(file_name):
  global SETTINGS

  switch_count = 0
  try:
    ini_file = open(INI_FILE_NAME)
    try: 
      read_settings(ini_file)

      #Записываем количество коммутаторов в файле списка коммутаторов в expected_switch_count
      expected_switch_count = len(SETTINGS["switches_ip"])

      #Записываем количество файлов конфигурации коммутаторов в real_switch_count
      path = f"{BACKUP_PATH}{str(datetime.date.today().isoweekday())}_{str(datetime.date.today()).replace('-','')}"
#      path = BACKUP_PATH + str(datetime.date.today().isoweekday())+'_'+str(datetime.date.today()).replace("-","")
      real_switch_count = len([f for f in os.listdir(path)
                        if os.path.isfile(os.path.join(path, f))])
      # формируем отчет
      rep_file = open(file_name,"w+")
      rep_file.write(PREAMBLE + "\r\n")
      message = f"   -  Сохранено {real_switch_count} конфигураций из {expected_switch_count} "
      if real_switch_count == expected_switch_count:
        message +=  "[PASS]"
      else:
        message += "[FAIL!!!]"
      message += "\r\n"
      message += f"   -  Расположение архива:\r\n      {path}\r\n\r\n"
      rep_file.write(message)
      rep_file.close()
    except: print(f"{datetime_message()} Ошибка: не удалось прочитать файл настроек [{INI_FILE_NAME}]")
    ini_file.close()
  except:
    print(f"{datetime_message()} Ошибка: не удалось открыть файл настроек [{INI_FILE_NAME}]")

#---- main ----
if __name__ == "__main__":

  print (f"{datetime_message()} start")
  filename = ""
  try:
    filename = f"{sys.argv[1]}/{os.path.basename(__file__)}"
    filename = filename.replace(".py",".rep")
    try:
      do_script(filename)
    except: pass
  except:
    print (f"{datetime_message()} Ошибка: скрипт должен запускаться с аргументом [/root/dk_scripts/reports/2024-01-15]")
  print (f"{datetime_message()} stop")
