#!/usr/bin/python3
'''
2023-11-20 Дмитрий Кораблев
Скрипт нахождения изменений в архивах за текущий и прошлый дни
'''
import os
import datetime
import json
import fnmatch

#Константы

INI_FILE_NAME = f"/root/dk_scripts/{os.path.basename(__file__).replace('_','').replace('.py','.json')}"
#INI_FILE_NAME = f"./{os.path.basename(__file__).replace('_','').replace('.py','.json')}"
SETTINGS      = {}
UNPACKING_PATH= "/root/dk_scripts/tmp"
LOGFILES_PATH = "/root/dk_scripts/diffs"
REMOVE_DIRS   = {"log","reports","tmp","diffs"}
DIFF_DIR = f"{LOGFILES_PATH}/{str(datetime.date.today()).replace('-','')}"


#---- datetime_message() ----
def datetime_message():
  return f"{datetime.datetime.now().replace(microsecond=0)} [{os.path.basename(__file__)}]"

#---- remove_dirs()  ----
def remove_dirs():
  global REMOVE_DIRS
  for dir in REMOVE_DIRS:
    cmd = f"rm -R {UNPACKING_PATH}/1/{dir}"
    os.system(cmd)
    cmd = f"rm -R {UNPACKING_PATH}/2/{dir}"
    os.system(cmd)

#---- rename_files()  ----
def rename_files():
  for filename in os.listdir(f"{UNPACKING_PATH}/1"):
    new_filename = f"{UNPACKING_PATH}/1/{filename[9:len(filename)]}"
    old_filename = f"{UNPACKING_PATH}/1/{filename}"
    os.rename(old_filename,new_filename)

  for filename in os.listdir(f"{UNPACKING_PATH}/2"):
    new_filename = f"{UNPACKING_PATH}/2/{filename[9:len(filename)]}"
    old_filename = f"{UNPACKING_PATH}/2/{filename}"
    os.rename(old_filename,new_filename)

#---- parse_name(f_name1) ----
def parse_name(name):
  wd = datetime.date.today().isoweekday()
  s = name.find(f"{wd}_")
  e = name.find("_bac")
  ret_name = name[s+2:e]
  return ret_name

#---- unpack_files(f_name1, f_name2) ----
def unpack_files(f_name1, f_name2):
  global UNPACKING_PATH, DIFF_DIR

#  date_stamp = "{str(datetime.date.today()).replace('-','')}"
  arch_name = parse_name(f_name1)
  date_stamp = f"{str(datetime.date.today()).replace('-','')}" 
#  print(date_stamp)

  #Распаковываем архив 1
  cmd = f"tar -xvf {f_name1} -C {UNPACKING_PATH}/1 > /dev/null"
  os.system(cmd)
  #Распаковываем архив 2
  cmd = f"tar -xvf {f_name2} -C {UNPACKING_PATH}/2 > /dev/null"
  os.system(cmd)

  if arch_name == "switches":   rename_files()
  if arch_name == "dk_scripts": remove_dirs()
  
  #!!!Находим разницу в файлах!!!
  cmd = f"diff -r {UNPACKING_PATH}/2 {UNPACKING_PATH}/1 > {DIFF_DIR}/{arch_name}_{date_stamp}.diff"
  os.system(cmd)
  #Удаляем все из временных папок
  cmd = f"rm -R {UNPACKING_PATH}/1/* && rm -R {UNPACKING_PATH}/2/*"
  os.system(cmd)



#---- find_fiiles() ----
def find_fiiles(the_path):
  weekday_1 = datetime.date.today().isoweekday()
  f_name1 = ""
  f_name2 = ""
  if (weekday_1 == 1): weekday_2 = 7
  else: weekday_2 = weekday_1-1
  for root, dirs, files in os.walk(the_path):
    for file in files:
      if file in fnmatch.filter(files,f"{weekday_1}_*.tar"): f_name1 = f"{the_path}/{file}"
      if file in fnmatch.filter(files,f"{weekday_2}_*.tar"): f_name2 = f"{the_path}/{file}"

  if not f_name1:  print(f"{datetime_message()} Файл [{the_path}/{weekday_1}_*.tar] не найден")
  if not f_name2:  print(f"{datetime_message()} Файл [{the_path}/{weekday_2}_*.tar] не найден")

  if f_name1 and f_name2: unpack_files(f_name1, f_name2) 

#---- do_script() ----
def do_script():
  global SETTINGS, DIFF_DIR

  #Создаем папку для записи файлов
  if not os.path.exists(DIFF_DIR): 
    cmd = f"mkdir {LOGFILES_PATH}/{str(datetime.date.today()).replace('-','')}"
    os.system(cmd)
  for path in SETTINGS["dif_paths"]:
    find_fiiles(path)

#---- read_settings() ----
def read_settings():
  global INI_FILE_NAME, SETTINGS
  try:
    ini_file = open(INI_FILE_NAME)
    try:
      SETTINGS = json.load(ini_file)
      #print(SETTINGS)
    except:
      print(f"{datetime_message()} Ошибка: Не удалось прочитать файл настроек [{INI_FILE_NAME}]")
  except:
    print(f"{datetime_message()} Ошибка: Не удалось открыть файл настроек [{INI_FILE_NAME}]")

#---- run_script() ----
def run_script():
  read_settings()
  do_script()

#------ main --------
if __name__ == "__main__":
  print(f"{datetime_message()} start")
  run_script()
  print(f"{datetime_message()} stop")

