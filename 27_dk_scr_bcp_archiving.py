#!/usr/bin/python3
"""
 Скрипт архивирования папок из списка

 Типы источников архивирования:
 fsd  : File System with Directory
 rfs : RemoteFileSystem
 mega: Mega
 yd  : Yanfex Disk

 После отработки скрипта создаютя архивы папок из списка


 2023.09.15 Дата создания 
"""
import os
import datetime
import json
import shutil
import glob
import subprocess
import time

# Константы
INI_FILE_NAME = f"/root/dk_scripts/{os.path.basename(__file__).replace('_','').replace('.py','.json')}"
#INI_FILE_NAME = f"./{os.path.basename(__file__).replace('_','').replace('.py','.json')}"
SETTINGS = {} #Настройки
#MEGA_LOGIN = "dkorablev@toyota-ufa.ru"	#Логин для меги
#MEGA_PASS  = "nhbvbnbk"			#Пароль для меги

#---- datetime_message()  ----
def datetime_message():
  return f"{datetime.datetime.now().replace(microsecond=0)} [{os.path.basename(__file__)}]"


#----- get_dir(src_path) -----
def get_dir(src_path):
  #Ищем папку с самой ранней датой
  entry = max((e for e in os.scandir(src_path) if e.is_dir(follow_symlinks=False)),
            key=lambda e: getattr(e.stat(), 'st_birthtime', None) or e.stat().st_ctime)
  return entry.name


#----- del_file_in_dst_path(dst_path,filename) ---

def del_file_in_dst_path(dst_path,src_file):
  filename=glob.glob(f"{dst_path}/{src_file[0:5]}*.*",recursive=True)
  for name in filename:
    #print(f"start {datetime.datetime.now()} [{os.path.basename(__file__)}] Удален файл:          [{name}]")
    print(f"{datetime_message()} Удален файл:          [{name}]")
    os.remove(name)
#----- copy_rfs(src_path,dst_path) -----

def arch_rfs(src_path,dst_path,mnt_path):

  command = f'sshfs -o password_stdin {mnt_path}'
  subprocess.Popen(command, shell=True, executable='/bin/bash')
  time.sleep(1)
  src_dir  =  f"{src_path}"
  filename = f"{str(datetime.date.today().isoweekday())}_{os.path.basename(dst_path)}_backup_{str(datetime.date.today()).replace('-','')}.tar"
  del_file_in_dst_path(dst_path,filename)
  command  = f"cd {src_dir} && tar cf {dst_path}/{filename} * && cd {dst_path} && umount {src_path} && chmod -R 777 {dst_path}"
  subprocess.Popen(command, shell=True, executable='/bin/bash')
  #print(f"start {datetime.datetime.now()} [{os.path.basename(__file__)}] Создан архивный файл: [{dst_path}/{filename}]")
  print(f"{datetime_message()} Создан архивный файл: [{dst_path}/{filename}]")

#----- arch_fsd(src_path,dst_path) -----

def arch_fsd(src_path,dst_path):
  src_dir  =  f"{src_path}/{get_dir(src_path)}"
  filename = f"{str(datetime.date.today().isoweekday())}_{os.path.basename(dst_path)}_backup_{str(datetime.date.today()).replace('-','')}.tar"
  del_file_in_dst_path(dst_path,filename)
  command  = f"cd {src_dir} &&  tar cf {dst_path}/{filename} * && chmod -R 777 {dst_path}"
  #print(f"start {datetime.datetime.now()} [{os.path.basename(__file__)}] Создан архивный файл: [{dst_path}/{filename}]")
  os.system(command)
  print(f"{datetime_message()} Создан архивный файл: [{dst_path}/{filename}]")

#----- arch_fs(src_path,dst_path) -----

def arch_fs(src_path,dst_path):
  src_dir  =  f"{src_path}"
  filename = f"{str(datetime.date.today().isoweekday())}_{os.path.basename(dst_path)}_backup_{str(datetime.date.today()).replace('-','')}.tar"
  del_file_in_dst_path(dst_path,filename)
  command  = f"cd {src_dir} &&  tar cf {dst_path}/{filename} * && chmod -R 777 {dst_path}"
  #print(f"start {datetime.datetime.now()} [{os.path.basename(__file__)}] Создан архивный файл: [{dst_path}/{filename}]")
  #print(f"Создан архивный файл: [{dst_path}/{filename}]")
  os.system(command)
  print(f"{datetime_message()} Создан архивный файл: [{dst_path}/{filename}]")

#----- do_arch(path, copy_type) -----

def do_arch(item):
  if (item[2] == "fs")  : arch_fs (item[0],item[1])
  if (item[2] == "fsd") : arch_fsd(item[0],item[1])
  if (item[2] == "rfs") : arch_rfs(item[0],item[1],item[3])
#  if (path_item[2] == "mega"): copy_mega(path_item[0],path_item[1])
#  if (path_item[2] == "yd")  : copy_yd(path_item[0],path_item[1])


#----- archiving() -----
def archiving():
  global SETTINGS
  for item in SETTINGS["arch_paths"]:
    do_arch(item)

#----- read_settings -----
def read_settings():
  global INI_FILE_NAME, SETTINGS
  ini_file = open(INI_FILE_NAME)
  try:
    ini_file = open(INI_FILE_NAME)
    try:
      SETTINGS = json.load(ini_file)
      print(f"{datetime_message()} Прочитан файл настроек[INI_FILE_NAME]")
#      print(f"start {datetime.datetime.now()} [{os.path.basename(__file__)}] Прочитан файл настроек")
      return True

    except:
#      print(f"start {datetime.datetime.now()} [{os.path.basename(__file__)}] Ошибка: Не удалость прочитать файл настроек [{INI_FILE_NAME}]")
      print(f"{datetime_message()} Ошибка: Не удалость прочитать файл настроек [{INI_FILE_NAME}]")
      return False
    ini_file.close()
  except:
    print(f"{datetime_message()} Ошибка: Не удалость открыть файл настроек [{INI_FILE_NAME}]")
#    print(f"start {datetime.datetime.now()} [{os.path.basename(__file__)}] Ошибка: Не удалость открыть файл настроек [{INI_FILE_NAME}]")
    return False

#----- run_script -----

def run_script():
  if(read_settings()):
    archiving()

#----- main -----
print(f"{datetime_message()} start ")
#print(f"{datetime.datetime.now()} [{os.path.basename(__file__)}] start")
run_script()
print(f"{datetime_message()} stop")
#print(f"{datetime.datetime.now()} [{os.path.basename(__file__)}] stop")
