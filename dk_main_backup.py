#!/usr/bin/python3
"""
 Скрипт запуска скриптов из  директории WORK_DIR, 
 содержащих в имени файла MATCH_STR

 2023.09.25 refactoring:  Убраны подсветки в начальных сообщениях, константы названы UpperCase шрифтом
 2023.11.22 1. refactoring: Изменена функция получения списка скриптов
            2. добавлена функция datetime_message()
 2024.01.22 refactoring: Оптимизирован код, добавлен try except при выполнении скриптов
"""
import os
import datetime

WORK_DIR   = "/root/dk_scripts/"
MATCH_STR  = "dk_scr"
START_TIME = ""

#---- datetime_message() ----
def datetime_message():
  return f"{datetime.datetime.now().replace(microsecond=0)} [{os.path.basename(__file__)}]"

#---- file_number(file_name) ----
def file_number(file_name):
  return int(file_name[0:file_name.find("_")])

#---- run_script() ----
def run_script():
  scripts_list = []
  #Записываем в files все, что находится в WORK_DIR
  files = os.listdir(WORK_DIR)
  #Записываем все нужные файлы в scripts_list
  for filename in files:
    if os.path.isfile(f"{WORK_DIR}{filename}") and MATCH_STR in filename:
      scripts_list.append(filename)
  #Сортируем список по номеру
  scripts_list.sort(key = file_number)
  #Выполняем скрипты, согласно их номерам
  for i in range(len(scripts_list)):

#    print(f"{datetime_message().replace(microsecond=0)} Запуск скрипта [{WORK_DIR+scripts_list[i]}]")
    print(f"{datetime_message()} Запуск скрипта [{scripts_list[i]}]")
    print("------------------------------------------------------------")
    cmd = f"{WORK_DIR}{scripts_list[i]}"
    try:
      os.system(cmd)
      print("------------------------------------------------------------")
#      print (f"{datetime_message()} Cкрипт [{cmd}] успешно выполнен.[PASS]")
      print (f"{datetime_message()} Cкрипт         [{scripts_list[i]}] успешно выполнен.[PASS]")
    except:
      print("------------------------------------------------------------")
#      print (f"{datetime_message()} Ошибка: не удалось выполнить скрипт [{cmd}] [FAIL!!!]")
      print (f"{datetime_message()} Ошибка: не удалось выполнить скрипт [{scripts_list[i]}] [FAIL!!!]")

#------- main ---------
if __name__ == "__main__":
  START_TIME = datetime.datetime.now().replace(microsecond=0)
  print(f"{datetime_message()} start")
  run_script()
  print(f"{datetime_message()} stop")
  print()
  print(f"==== Скрипт выполнялся с [{START_TIME}] по [{datetime.datetime.now().replace(microsecond=0)}] ====")
