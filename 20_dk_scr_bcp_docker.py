#!/usr/bin/python3

'''
Скрипт создания backup docker контейнеров
(c) Дмитрий Кораблев

   После отработки скрипта, в каталоге {DST_PATH}/{the_docker}/{file_name} содержится 
архив docker контейнера

2022.03.28 Дата создания 
2022.03.29 Исправлено - удаление всех файлов в архиве 
2022.09.21 Исправлено - переезд на новый сервер
2024.01.22 1.Добавлена функция datetime_message
           2.В сообщениях добавлено {datetime_message}
           3.Глобальные переменные переведены в UpperCase
'''

import datetime
import time, os
import sys
import json


# Константы
INI_FILE_NAME = f"/root/dk_scripts/{os.path.basename(__file__).replace('_','').replace('.py','.json')}"
#INI_FILE_NAME = f"./{os.path.basename(__file__).replace('_','').replace('.py','.json')}"
SETTINGS      = {}
SRC_PATH  = "/docker/" #общая папка с docker контейнерами
DST_PATH_CUR =""
DST_PATH  = "/docker/samba/data/public/backups/docker"
LIST_FILE = "/root/dk_scripts/list_docker_stacks"


now = datetime.datetime.now()

#---- datetime_message ----
def datetime_message():
  return f"{datetime.datetime.now().replace(microsecond=0)} [{os.path.basename(__file__)}]"

#---- backup ----
def backup(the_docker):
  global DST_PATH, now

  cur_file = f"{DST_PATH}/{the_docker}"
  if os.path.isdir(cur_file):
    dirs = os.listdir(cur_file)
    match_str = f"{str(datetime.date.today().isoweekday())}_{the_docker}"
    #Находим и удаляем файл
    for file in dirs:
      if file.find(match_str) > -1: 
        del_file = f"{DST_PATH}/{the_docker}/{file}"
        print(f"{datetime_message()} Удаляем файл: [{del_file}]")
        os.remove(del_file)
    file_name = f"{str(datetime.date.today().isoweekday())}_{the_docker}_backup_{str(datetime.date.today()).replace('-','')}.tar"
    cmd = f"cd {SRC_PATH}{the_docker}/ &&  tar czpf {DST_PATH}/{the_docker}/{file_name} ./"
    print(f"{datetime_message()} Архивируем    [{SRC_PATH}{the_docker} в {DST_PATH}/{the_docker}/{file_name}]")
    os.system(cmd)
  else: 
    print(f"{datetime_message()} Ошибка: Не найдена папка[{cur_file}]")

#---- backup_docker ----
def backup_docker():
  global SETTINGS
  for docker in SETTINGS["docker_stack"]:
    backup(docker)

#---- read_settings ----
def read_settings():
  global INI_FILE_NAME, SETTINGS
  ret = False
  try:
    ini_file = open(INI_FILE_NAME)
    try:
      SETTINGS = json.load(ini_file)
      print(f"{datetime_message()} Файл настроек [{INI_FILE_NAME}] прочитан")
      ret =  True
    except:
      print(f"{datetime_message()} Ошибка: не удалось прочитать Файл настроек [{INI_FILE_NAME}]")
    ini_file.close()
  except:
    print(f"{datetime_message()} Ошибка: не удалось открыть  Файл настроек [{INI_FILE_NAME}]")
  return ret

#---- run_script ----
def run_script(filename):
  if read_settings():
    backup_docker()

#----- main -----
if __name__ =="__main__":
  print(f"{datetime_message()} start")
  run_script(LIST_FILE)
  print(f"{datetime_message()} stop")
