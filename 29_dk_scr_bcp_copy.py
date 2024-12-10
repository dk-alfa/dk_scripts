#!/usr/bin/python3
"""
 Скрипт копирования backup файлов
 Типы копирования:
 fs  : FileSystem
 rfs : RemoteFileSystem
 mega: Mega
 yd  : Yanfex Disk


 2023.09.07 Дата создания 
"""
import os
import datetime
import json
import shutil
import glob

# Константы
INI_FILE_NAME = f"/root/dk_scripts/{os.path.basename(__file__).replace('_','').replace('.py','.json')}"
#INI_FILE_NAME = f"./{os.path.basename(__file__).replace('_','').replace('.py','.json')}"
SETTINGS = {} #Настройки
MEGA_LOGIN = "dkorablev@toyota-ufa.ru"	#Логин для меги
MEGA_PASS  = "nhbvbnbk"			#Пароль для меги


#---- datetime_message() ----
def datetime_message():
  return f"{datetime.datetime.now().replace(microsecond=0)} [{os.path.basename(__file__)}]"


#----- del_file_in_dst_path(dst_path) -----
def del_file_in_dst_path(dst_path,src_file):
  filename = glob.glob( f"{dst_path}/{src_file[0:5]}*.*", recursive=True)
  for name in filename:
    print(f"{datetime_message()} Удаляется : [{name}]")
#    print(f"{datetime.datetime.now()} [{os.path.basename(__file__)}] Удаляется : [{name}]")
    os.remove(name)

#----- get_last_file(src_path) -----

def get_last_file(src_path):

  files = os.listdir(src_path)
  files = [os.path.join(src_path, file) for file in files]
  files = [file for file in files if os.path.isfile(file)]
  ret = os.path.basename(max(files, key=os.path.getmtime))
  return ret

#----- copy_rfs(src_path,dst_path) -----

def copy_rfs(src_path,dst_path,mnt_path):
  os.system(f"sudo mount -t cifs {mnt_path}")
  copy_fs(src_path,dst_path)
  os.system(f"sudo umount {dst_path}")

#----- copy_fs(src_path,dst_path) -----

def copy_fs(src_path,dst_path):
  src_file =  get_last_file(src_path)
  del_file_in_dst_path(dst_path,src_file)
  print(f"{datetime_message()} Удаляется : [Копируется: [{src_path}/{src_file} {dst_path}/]]")
  #print (f"{datetime.datetime.now()} [{os.path.basename(__file__)}] Копируется: [{src_path}/{src_file} {dst_path}/]")
  shutil.copy2(f"{src_path}/{src_file}", f"{dst_path}/{src_file}")

#----- copy_mega(path) -----

def copy_mega(src_path,dst_path):
  src_file =  get_last_file(src_path)
  os.system(f"mega-login {MEGA_LOGIN} {MEGA_PASS}")
  os.system(f"mega-rm {dst_path}/{src_file[0:7]}*.*")
  os.system(f"mega-put {src_path}/{src_file} {dst_path}/{src_file}")
  os.system("mega-logout")

#----- copy_yd(path) -----

def copy_yd(src_path,dst_path):
  pass
#  print(f"copy {src_path} to {dst_path}"

#----- do_copy(path, copy_type) -----

def do_copy(path_item):
  pass
  if (path_item[2] == "fs")  : copy_fs(path_item[0],path_item[1])
  if (path_item[2] == "rfs") : copy_rfs(path_item[0],path_item[1],path_item[3])
  if (path_item[2] == "mega"): copy_mega(path_item[0],path_item[1])
#  if (path_item[2] == "yd")  : copy_yd(path_item[0],path_item[1])


#----- copy_bacup() -----

def copy_bacup():
  global SETTINGS
  for path_item in SETTINGS["bcp_paths"]:
    do_copy(path_item)

#----- read_settings -----

def read_settings():
  global INI_FILE_NAME, SETTINGS
  ini_file = open(INI_FILE_NAME)
  try:
    ini_file = open(INI_FILE_NAME)
    try:
      SETTINGS = json.load(ini_file)
    except:
      print(f"{datetime_message()} Ошибка: Не удалость прочитать файл настроек [{INI_FILE_NAME}]")
      #print(f"{datetime.datetime.now()} [{os.path.basename(__file__)}] Ошибка: Не удалость прочитать файл настроек [{INI_FILE_NAME}]")
    ini_file.close()
  except:
    print(f"{datetime_message()} Ошибка: Не удалость открыть файл настроек [{INI_FILE_NAME}]")

#----- run_script -----
def run_script():
    read_settings()
    copy_bacup()

#----- main -----
if __name__ == "__main__":
  print(f"{datetime_message()} start")
  run_script()
  print(f"{datetime_message()} stop")
