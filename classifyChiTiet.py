import os, sys
import pandas as pd
from nudenet import NudeClassifier
import csv
import shutil

def check_image_in_folder(pathname):
  list_folder = os.listdir(pathname)
  filename=""
  for i in list_folder:
    if(str(i).find("csv")!=-1):
        try:
            filename = pathname + "/" + str(i)

            headers = ['img_name', 'img_src', 'title', 'doc_src', 'date', 'author', 'note']
            df = pd.read_csv(filename, header=0, encoding = "utf-8")
            imgs_infor = df.values.tolist()

            classifier = NudeClassifier()

            list_safe = []
            list_unsafe = []
            for item in imgs_infor:
                for i in list_folder:
                    try:
                        if(str(i).find(item[0])!=-1):
                        # print(str(i))
                            test = classifier.classify(pathname + "/" + str(i))
                            if(test[pathname + "/" + str(i)]['unsafe']>0.8):
                                shutil.move(pathname + "/" + str(i), pathname + "/UnSafe/")
                                list_unsafe.append(item)
                            else:
                                shutil.move(pathname + "/" + str(i), pathname + "/Safe/")
                                list_safe.append(item)
                    except:
                        pass
            return list_safe, list_unsafe
        except:
            pass

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
        except:
            pass



def classify_pure(path):
    list_sum_folder = os.listdir(path)
    for i in list_sum_folder:
            if(str(i).find(".")==-1):
                sub_list_sum_folder = os.listdir(path+ "/" +str(i))
                for j in sub_list_sum_folder:
                    if(os.path.exists(path+ "/" +str(i) + "/" + str(j) + "/" + "{}.csv".format(j))):
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
                    else: continue


def classify_not_pure(path):
    list_sum_folder = os.listdir(path)
    for i in list_sum_folder:
        if(str(path+ "/" +str(i)).find(".")==-1):

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
        classify_not_pure(path)
    if "https://anhnude.info" in web:
        path = "static/data/Detail/AnhNude"
        classify_not_pure(path)
    if "https://vnexpress.net" in web:
        path = "static/data/Detail/VnExpress"
        classify_pure(path)
    if "https://ngoisao.vnexpress" in web:
        path = "static/data/Detail/SaoStar"
        classify_pure(path)
    if "https://thanhnien.vn" in web:
        path = "static/data/Detail/ThanhNien"
        classify_pure(path)
    