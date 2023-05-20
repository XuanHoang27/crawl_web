import os
import sys
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
        if pd.isna(item[0]):
            continue
        else: 
            for i in list_folder:
                try:
                    if(str(i).find(item[0]) != -1):
                        # print(str(i))
                        test = classifier.classify(pathname + "/" + str(i))
                        if(test[pathname + "/" + str(i)]['unsafe'] > 0.8):
                            shutil.move(pathname + "/" + str(i), pathname + "/UnSafe/")
                            list_unsafe.append(item)
                        else:
                            shutil.move(pathname + "/" + str(i), pathname + "/Safe/")
                            list_safe.append(item)
                except:
                    pass
        
    return list_safe, list_unsafe


def create_csv_for_safe_data(pathname, list_safe):
    column = []
    temp = 0
    try:
        df = pd.read_csv(pathname + '/Safe/safe.csv')
        column = list(set(df.doc_src.to_list()))
    except:
        pass
    if(len(column) > 0):
        temp = 1
    for i in list_safe:
        try:
            if len(i) > 4:
                new_row={'img_name':[i[0]], 'img_src':[i[1]], 'title':[i[2]], 'doc_src':[i[3]], 'date':[i[4]], 'author':[i[5]]}
                if temp == 0:
                    df = pd.DataFrame(new_row)
                    temp = 1
                    df.to_csv(pathname + '/Safe/safe.csv', mode='a', index=False,
                            header=['img_name', 'img_src', 'title', 'doc_src', 'date', 'author'])
                else:
                    df = pd.DataFrame(new_row)
                    df.to_csv(pathname + '/Safe/safe.csv',
                            mode='a', index=False, header=False)
            else: 
                new_row={'img_name':[i[0]], 'img_src':[i[1]], 'title':[i[2]], 'doc_src':[i[3]]}
                if temp == 0:
                    df = pd.DataFrame(new_row)
                    temp = 1
                    df.to_csv(pathname + '/Safe/safe.csv', mode='a', index=False,
                            header=['img_name', 'img_src', 'title', 'doc_src'])
                else:
                    df = pd.DataFrame(new_row)
                    df.to_csv(pathname + '/Safe/safe.csv',
                            mode='a', index=False, header=False)
            
        except:
            pass


def create_csv_for_unsafe_data(pathname, list_unsafe):
    column = []
    temp = 0
    try:
        df = pd.read_csv(pathname + '/UnSafe/unsafe.csv')
        column = list(set(df.doc_src.to_list()))
    except:
        pass
    if(len(column) > 0):
        temp = 1
    for i in list_unsafe:
        try:
            if len(i) > 4:
                new_row={'img_name':[i[0]], 'img_src':[i[1]], 'title':[i[2]], 'doc_src':[i[3]], 'date':[i[4]], 'author':[i[5]]}
                if temp == 0:
                    df = pd.DataFrame(new_row)
                    temp = 1
                    df.to_csv(pathname + '/UnSafe/unsafe.csv', mode='a', index=False,
                            header=['img_name', 'img_src', 'title', 'doc_src', 'date', 'author'])
                else:
                    df = pd.DataFrame(new_row)
                    df.to_csv(pathname + '/UnSafe/unsafe.csv',
                            mode='a', index=False, header=False)
            else:
                new_row={'img_name':[i[0]], 'img_src':[i[1]], 'title':[i[2]], 'doc_src':[i[3]]}
                if temp == 0:
                    df = pd.DataFrame(new_row)
                    temp = 1
                    df.to_csv(pathname + '/UnSafe/unsafe.csv', mode='a', index=False,
                            header=['img_name', 'img_src', 'title', 'doc_src'])
                else:
                    df = pd.DataFrame(new_row)
                    df.to_csv(pathname + '/UnSafe/unsafe.csv',
                            mode='a', index=False, header=False)                
        except:
            pass


def classify(path):

    dir_safe = path + "/Safe"
    dir_unsafe = path + "/UnSafe"

    if (os.path.exists(dir_safe) == False):
        os.makedirs(dir_safe)

    if (os.path.exists(dir_unsafe) == False):
        os.makedirs(dir_unsafe)

    list = check_image_in_folder(path)
    create_csv_for_safe_data(path, list[0])
    create_csv_for_unsafe_data(path, list[1])


def classify_Non_Detail(web):
    if "https://xemanhnong.asia" in web:
        path = "static/data/Non_Detail/AnhNong"
        classify(path)
    if "https://anhnude.info" in web:
        path = "static/data/Non_Detail/AnhNude"
        classify(path)
    if "https://vnexpress.net" in web:
        path = "static/data/Non_Detail/VnExpress"
        classify(path)
    if "https://ngoisao.vnexpress" in web:
        path = "static/data/Non_Detail/SaoStar"
        classify(path)
    if "https://thanhnien.vn" in web:
        path = "static/data/Non_Detail/ThanhNien"
        classify(path)