import os, sys
import pandas as pd
from nudenet import NudeClassifier
import csv
import shutil

def check_image_in_folder(pathname):
    list_folder = os.listdir(pathname)
    filename = ""
    for i in list_folder:
        if(str(i).find("csv") != -1):
            filename = pathname + "/" + str(i)

    headers = ['img_name', 'img_src', 'title',
               'doc_src', 'date', 'author', 'note']
    df = pd.read_csv(filename, header=0, encoding="utf-8")
    imgs_infor = df.values.tolist()

    classifier = NudeClassifier()

    list_safe = []
    list_unsafe = []
    for item in imgs_infor:
        for i in list_folder:
            if(str(i).find(item[0]) != -1):
                # print(str(i))
                test = classifier.classify(pathname + "/" + str(i))
                if(test[pathname + "/" + str(i)]['unsafe'] > 0.8):
                    shutil.move(pathname + "/" + str(i), pathname + "/UnSafe/")
                    list_unsafe.append(item)
                else:
                    shutil.move(pathname + "/" + str(i), pathname + "/Safe/")
                    list_safe.append(item)
    return list_safe, list_unsafe

def create_csv_for_safe_data(pathname, list_safe):
  f = open(pathname + '/Safe/safe.csv', 'w+', encoding='UTF8')
  writer = csv.writer(f)
  header_csv = ['img_name', 'img_src', 'title', 'doc_src', 'date', 'author', 'note']
  writer.writerow(header_csv)
  for i in list_safe:
    writer.writerow(i)
  f.close()

def create_csv_for_unsafe_data(pathname, list_unsafe):
  f = open(pathname + '/UnSafe/unsafe.csv', 'w+', encoding='UTF8')
  writer = csv.writer(f)
  header_csv = ['img_name', 'img_src', 'title', 'doc_src', 'date', 'author', 'note']
  writer.writerow(header_csv)
  for i in list_unsafe:
    writer.writerow(i)
  f.close()

def classify_detail_pure(path):
    list_sum_folder = os.listdir(path)
    for i in list_sum_folder:
        if(str(i).find(".")==-1):
            sub_list_sum_folder = os.listdir(path+ "/" +str(i))
            for j in sub_list_sum_folder:
                dir_safe = path+ "/" +str(i) + "/" + str(j) + "/Safe"
                dir_unsafe = path+ "/" +str(i) + "/" + str(j) + "/UnSafe"
                
                if (os.path.exists(dir_safe)==False):
                    os.makedirs(dir_safe)
                
                
                if (os.path.exists(dir_unsafe)==False):
                    os.makedirs(dir_unsafe)

                pathname = path+ "/" +str(i) + "/" + str(j)
                # print(pathname)
                list = check_image_in_folder(pathname)
                create_csv_for_safe_data(pathname, list[0])
                create_csv_for_unsafe_data(pathname, list[1])


def classify_detail_not_pure(path):
    list_sum_folder = os.listdir(path)
    for i in list_sum_folder:
        if(str(i).find(".")==-1):
            dir_safe = path+ "/" +str(i)  + "/Safe"
            dir_unsafe = path+ "/" +str(i) + "/UnSafe"
            
            if (os.path.exists(dir_safe)==False):
                    os.makedirs(dir_safe)
                
                
            if (os.path.exists(dir_unsafe)==False):
                os.makedirs(dir_unsafe)

            pathname = path+ "/" +str(i)
            # print(pathname)
            list = check_image_in_folder(pathname)
            create_csv_for_safe_data(pathname, list[0])
            create_csv_for_unsafe_data(pathname, list[1])


def classify_detail(web):
    if "https://xemanhnong.asia" in web:
        path = "static/data/Detail/AnhNong"
        classify_detail_not_pure(path)
    if "https://anhnude.info" in web:
        path = "static/data/Detail/AnhNude"
        classify_detail_not_pure(path)
    if "https://vnexpress.net" in web:
        path = "static/data/Detail/VnExpress"
        classify_detail_pure(path)
    if "https://ngoisao.vnexpress" in web:
        path = "static/data/Detail/SaoStar"
        classify_detail_pure(path)
    if "https://thanhnien.vn" in web:
        path = "static/data/Detail/ThanhNien"
        classify_detail_pure(path)
    
