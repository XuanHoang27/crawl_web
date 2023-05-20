from urllib.request import urlopen, urljoin
import requests
import re
from bs4 import BeautifulSoup as BS
import os
import csv
from urllib.request import urlopen, urljoin
import requests
import re
from bs4 import BeautifulSoup as BS
import os
import shutil
import pandas as pd
from nudenet import NudeClassifier

root_folder = "data2"


def remove_special_chars(input_string):
    pattern = r'[^a-zA-Z0-9\sđĐáÁàÀảẢãÃạẠăĂắẮằẰẳẲẵẴặẶâÂấẤầẦẩẨẫẪậẬéÉèÈẻẺẽẼẹẸêÊếẾềỀểỂễỄệỆíÍìÌỉỈĩĨịỊôÔốỐồỒổỔỗỖộỘơƠớỚờỜởỞỡỠợỢúÚùÙủỦũŨụỤưỨỨừỪửỬữỮựỰýÝỷỶỹỸ]'
    new_string = re.sub(pattern, '', input_string)
    return new_string



def get_articles_XAN(URL, filename):

    column = []
    temp=0
    try:
        df = pd.read_csv("static/data/Detail/AnhNong/"+filename + '/' + filename +  '.csv')
        column = list(set(df.doc_src.to_list()))
    except:
        pass
   
    if(len(column)>0):
        temp=1
    column = list(set(column))

    reqs = requests.get(URL)
    content = reqs.text
    soup = BS(content, 'html.parser')
    articles_link = []
    csv_data = []
    for find_articles in soup.findAll('div', {'class': 'entry-summary'}):
            for find_atags in find_articles.find('a'):
                try:
                    if 'href' in find_atags.parent.attrs:
                        url = find_atags.parent.attrs['href']
                        column.append(url)
                        if(len(column)==len(list(set(column)))):
                            articles_link.append(url)
                        column = list(set(column))
                except:
                    pass

    for urla in articles_link:
        try:
            images_locations = []
            reqs = requests.get(urla)
            content = reqs.text
            soup1 = BS(content, 'html.parser')
            title_detail = ""

            # get title
            if soup1.find('h1', {'class': 'entry-title'}):
                title_detail = soup1.find('h1', {'class': 'entry-title'}).string

          

            if soup1.find('div', {'class': 'entry-content'}):
                imgs = soup1.find('div', {'class': 'entry-content'})
                if imgs.find('img'):
                    count_img = 0
                    imgs1 = imgs.find_all('img')
                    for img in imgs1:
                        write_csv = []
                        file_name = ""
                        if img.get('src'):
                            if("jpg" in img.get('src')):
                                file_name = img.get('src').split(".jpg")[0].split("/")[-1]
                            if("png" in img.get('src')):
                                file_name = img.get('src').split(".png")[0].split("/")[-1]
                            if("gif" in img.get('src')):
                                file_name = img.get('src').split(".gif")[0].split("/")[-1]
                            images_locations.append(img.get('src'))

                            response = requests.get(img.get('src'))

                            file = open("static/data/Detail/AnhNong/" + filename + "/" +
                                        file_name + "_{}.png".format(count_img), "wb")
                            count_img = count_img + 1
                            file.write(response.content)
                            file.close()
                            
                            new_row={'img_name':[file_name], 'img_src':[img.get('src')], 'title':[title_detail], 'doc_src':[urla]}
                        
                        if temp==0:
                            df = pd.DataFrame(new_row)
                            temp=1
                            df.to_csv("static/data/Detail/AnhNong/"+filename + '/' + filename +  '.csv', mode='a', index=False, header=['img_name', 'img_src', 'title', 'doc_src'])
                        else:
                            df = pd.DataFrame(new_row)
                            df.to_csv("static/data/Detail/AnhNong/"+filename + '/' + filename +  '.csv', mode='a', index=False, header=False)
                else:
                    continue
            else:
                continue


        except:
            pass


def get_articles_AN(URL, filename):

    column = []
    temp=0
    try:
        df = pd.read_csv("static/data/Detail/AnhNude/"+filename + '/' + filename +  '.csv')
        column = list(set(df.doc_src.to_list()))
    except:
        pass
   
    if(len(column)>0):
        temp=1
    column = list(set(column))

    reqs = requests.get(URL)
    content = reqs.text
    soup = BS(content, 'html.parser')
    articles_link = []
    csv_data = []
    for find_articles in soup.findAll('div', {'class': 'entry-thumb'}):
        for find_atags in find_articles.find('a'):
            try:
                if 'href' in find_atags.parent.attrs:
                    url = find_atags.parent.attrs['href']
                    column.append(url)
                    if(len(column)==len(list(set(column)))):
                        articles_link.append(url)
                    column = list(set(column))
            except:
                pass

    for urla in articles_link:
        try:
            images_locations = []
            reqs = requests.get(urla)
            content = reqs.text
            soup1 = BS(content, 'html.parser')
            title_detail = ""

            # get title
            if soup1.find('h1', {'class': 'entry-title'}):
                title_detail = soup1.find('h1', {'class': 'entry-title'}).string

          

            if soup1.find('div', {'class': 'entry-content'}):
                imgs = soup1.find('div', {'class': 'entry-content'})
                if imgs.find('img'):
                    count_img = 0
                    imgs1 = imgs.find_all('img')
                    for img in imgs1:
                        write_csv = []
                        file_name = ""
                        if img.get('src'):
                            if("jpg" in img.get('src')):
                                file_name = img.get('src').split(".jpg")[0].split("/")[-1]
                            if("png" in img.get('src')):
                                file_name = img.get('src').split(".png")[0].split("/")[-1]
                            if("gif" in img.get('src')):
                                file_name = img.get('src').split(".gif")[0].split("/")[-1]
                            images_locations.append(img.get('src'))

                            response = requests.get(img.get('src'))

                            file = open("static/data/Detail/AnhNude/" + filename + "/" +
                                        file_name + "_{}.png".format(count_img), "wb")
                            count_img = count_img + 1
                            file.write(response.content)
                            file.close()
                            
                            new_row={'img_name':[file_name], 'img_src':[img.get('data-src')], 'title':[title_detail], 'doc_src':[urla]}
                        
                        if temp==0:
                            df = pd.DataFrame(new_row)
                            temp=1
                            df.to_csv("static/data/Detail/AnhNude/"+filename + '/' + filename +  '.csv', mode='a', index=False, header=['img_name', 'img_src', 'title', 'doc_src'])
                        else:
                            df = pd.DataFrame(new_row)
                            df.to_csv("static/data/Detail/AnhNude/"+filename + '/' + filename +  '.csv', mode='a', index=False, header=False)
                else:
                    continue
            else:
                continue


        except Exception:
            print(Exception)


def get_articles_VNEX(URL,fn,fn1):

    column = []
    temp=0
    try:
        df = pd.read_csv("static/data/Detail/VnExpress/"+fn + '/' + fn1 + '/' + fn1 +  '.csv')
        column = list(set(df.doc_src.to_list()))
    except:
        pass
    # f = open("testvn/"+fn + '/' + fn1 + '/' + fn1 +  '.csv', 'w+', encoding='UTF8')
    # writer = csv.writer(f)
    # header_csv = ['img_name', 'img_src', 'title', 'doc_src', 'date', 'author', 'note']
    if(len(column)>0):
        temp=1
    column = list(set(column))
    reqs = requests.get(URL)
    content = reqs.text
    soup = BS(content, 'html.parser')
    articles_link=[]
    # print(soup.findAll('div',{'class':'thumb-art'}))
    for find_articles in  soup.findAll('div',{'class':'thumb-art'}):
        
            try:
                find_atags = find_articles.find('a')
                if 'href' in find_atags.attrs :
                    url = find_atags.get('href')
                    column.append(url)
                    if(len(column)==len(list(set(column)))):
                        articles_link.append(url)
                    column = list(set(column))
            except:
                pass
    # print(articles_link)
    for urla in articles_link:
        images_locations = []
        reqs = requests.get(urla)
        content = reqs.text
        soup1 = BS(content, 'html.parser')
        title_detail = ""
        author = ""
        date_time = ""
        #get title
        if soup1.find('h1', {'class':'title-detail'}):
          title_detail = soup1.find('h1', {'class':'title-detail'}).string
        #get auhor
        if soup1.find('p', {'class':'author_mail'}):
            soup2 = soup1.find('p', {'class':'author_mail'})
            if soup2.find('strong'):
                author = soup2.find('strong').string
        #get date_time
        if soup1.find('span', {'class':'date'}):
          date_time = soup1.find('span', {'class':'date'}).string

        
        if soup1.find('article', {'class':'fck_detail'}):
            imgs = soup1.find('article', {'class':'fck_detail'})
            if imgs.find('img'):
                count_img = 0
                imgs1 = imgs.find_all('img')
                for img in imgs1:
                    write_csv = []
                    file_name = ""
                    if img.get('data-src'):
                        if("jpg" in img.get('data-src')):
                                file_name = img.get('data-src').split(".jpg")[0].split("/")[-1]
                        if("png" in img.get('data-src')):
                            file_name = img.get('data-src').split(".png")[0].split("/")[-1]
                        if("gif" in img.get('data-src')):
                            file_name = img.get('data-src').split(".gif")[0].split("/")[-1]
                        images_locations.append(img.get('data-src'))
                        if img.get('href') == '': 
                            break
                        response = requests.get(img.get('data-src'))
                        file = open("static/data/Detail/VnExpress/"+fn+"/"+fn1 +"/" + file_name  + "_{}.png".format(count_img), "wb")
                        count_img = count_img + 1
                        file.write(response.content)
                        file.close()
                        new_row={'img_name':[file_name], 'img_src':[img.get('data-src')], 'title':[title_detail], 'doc_src':[urla], 'date':[date_time], 'author':[author]}
                        
                        if temp==0:
                            df = pd.DataFrame(new_row)
                            temp=1
                            df.to_csv("static/data/Detail/VnExpress/"+fn + '/' + fn1 + '/' + fn1 +  '.csv', mode='a', index=False, header=['img_name', 'img_src', 'title', 'doc_src', 'date', 'author'])
                        else:
                            df = pd.DataFrame(new_row)
                            df.to_csv("static/data/Detail/VnExpress/"+fn + '/' + fn1 + '/' + fn1 +  '.csv', mode='a', index=False, header=False)
            else:
                continue
        else:
            continue


def get_articles_NSVNE(URL,fn,fn1):

    column = []
    temp=0
    try:
        df = pd.read_csv("static/data/Detail/SaoStar/"+fn + '/' + fn1 + '/' + fn1 +  '.csv')
        column = list(set(df.doc_src.to_list()))
    except:
        pass
    if(len(column)>0):
        temp=1
    column = list(set(column))

    reqs = requests.get(URL)
    content = reqs.text
    soup = BS(content, 'html.parser')
    articles_link=[]
    for find_articles in  soup.findAll('div',{'class':'thumb_art'}):
        for find_atags in find_articles.findAll('a'):
            try:
                if 'href' in find_atags.attrs :
                    url = find_atags.get('href')
                    column.append(url)
                    if(len(column)==len(list(set(column)))):
                        articles_link.append(url)
                    column = list(set(column))
            except:
                pass

    for urla in articles_link:
        images_locations = []
        reqs = requests.get(urla)
        content = reqs.text
        soup1 = BS(content, 'html.parser')
        title_detail = ""
        author = ""
        date_time = ""
        #get title
        if soup1.find('h1', {'class':'title-detail'}):
          title_detail = soup1.find('h1', {'class':'title-detail'}).string
        #get auhor
        if soup1.find('p', {'class':'author_top'}):
            soup2 = soup1.find('p', {'class':'author_top'})
            if soup2.find('strong'):
                author = soup2.find('strong').string
        #get date_time
        if soup1.find('span', {'class':'date'}):
          date_time = soup1.find('span', {'class':'date'}).text

        # print(title_detail, date_time, author)
        if soup1.find('div', {'class':'sidebar-1'}):
            imgs = soup1.find('div', {'class':'sidebar-1'})
            if imgs.find('img'):
                count_img = 0
                imgs1 = imgs.find_all('img')
                for img in imgs1:
                    # write_csv = []
                    file_name = ""
                    if img.get('data-src'):
                        if("jpg" in img.get('data-src')):
                                file_name = img.get('data-src').split(".jpg")[0].split("/")[-1]
                        if("png" in img.get('data-src')):
                            file_name = img.get('data-src').split(".png")[0].split("/")[-1]
                        if("gif" in img.get('data-src')):
                            file_name = img.get('data-src').split(".gif")[0].split("/")[-1]
                        images_locations.append(img.get('data-src'))
                        if img.get('href') == '': 
                            break
                        response = requests.get(img.get('data-src'))
                        file = open('static/data/Detail/SaoStar/' +fn+"/"+fn1 +"/" + file_name  + "_{}.png".format(count_img), "wb")
                        count_img = count_img + 1
                        file.write(response.content)
                        file.close()
                        # write_csv.append(file_name)
                        # write_csv.append(img.get('data-src'))
                        # write_csv.append(title_detail)
                        # write_csv.append(urla)
                        # write_csv.append(date_time)
                        # write_csv.append(author)
                        # writer.writerow(write_csv)
                        new_row={'img_name':[file_name], 'img_src':[img.get('data-src')], 'title':[title_detail], 'doc_src':[urla], 'date':[date_time], 'author':[author]}
                        
                        if temp==0:
                            df = pd.DataFrame(new_row)
                            temp=1
                            df.to_csv("static/data/Detail/SaoStar/"+fn + '/' + fn1 + '/' + fn1 +  '.csv', mode='a', index=False, header=['img_name', 'img_src', 'title', 'doc_src', 'date', 'author'])
                        else:
                            df = pd.DataFrame(new_row)
                            df.to_csv("static/data/Detail/SaoStar/"+fn + '/' + fn1 + '/' + fn1 +  '.csv', mode='a', index=False, header=False)
            else:
                continue
        else:
            continue
   



def get_articles_TN(URL,fn,fn1):
    column = []
    temp=0
    try:
        df = pd.read_csv("static/data/Detail/ThanhNien/"+fn + '/' + fn1 + '/' + fn1 +  '.csv')
        column = list(set(df.doc_src.to_list()))
    except:
        pass
    # print(column)
    if(len(column)>0):
        temp=1
    column = list(set(column))

    reqs = requests.get(URL)
    content = reqs.text
    soup = BS(content, 'html.parser')
    articles_link=[]
    # print(soup.findAll('div',{'class':'thumb-art'}))
    for find_articles in  soup.findAll('div', {'class':'box-category-item'}):
        for find_atags in find_articles.findAll('a'):
            try:
    
                if 'href' in find_atags.attrs :
                    url = 'https://thanhnien.vn'+ find_atags.get('href')
                    column.append(url)
                    if(len(column)==len(list(set(column)))):
                        articles_link.append(url)
                    column = list(set(column))
            except:
                pass
    # print(articles_link)
    for urla in articles_link:
        try:
            images_locations = []
            reqs = requests.get(urla)
            content = reqs.text
            soup1 = BS(content, 'html.parser')
            title_detail = ""
            author = ""
            date_time = ""
            #get title
            if soup1.find('h1', {'class':'detail-title'}):
                title_detail_temp = soup1.find('h1', {'class':'detail-title'})
                if title_detail_temp.find('span'):
                    title_detail = title_detail_temp.find('span').string
            #get auhor
            if soup1.find('div', {'class':'detail-author'}):
                soup2 = soup1.find('div', {'class':'detail-author'})
                if soup2.find('a', {'class':'name'}):
                    author = soup2.find('a').get('title')
                    
            #get date_time
            if soup1.find('div', {'class':'detail-time'}):
                date_time_temp = soup1.find('div', {'class':'detail-time'})
                if date_time_temp.find('div'):
                    date_time = date_time_temp.find('div').text
            
            if soup1.find('div', {'class':'detail__main'}):
                imgs = soup1.find('div', {'class':'detail__main'})
                if imgs.find('img'):
                    count_img = 0
                    imgs1 = imgs.find_all('img')
                    for img in imgs1:
                        write_csv = []
                        file_name = ""
                        if img.get('data-original'):
                            if("jpg" in img.get('data-original')):
                                file_name = img.get('data-original').split(".jpg")[0].split("/")[-1]
                            if("png" in img.get('data-original')):
                                file_name = img.get('data-original').split(".png")[0].split("/")[-1]
                            if("gif" in img.get('data-original')):
                                file_name = img.get('data-original').split(".gif")[0].split("/")[-1]
                            images_locations.append(img.get('data-original'))
                            if img.get('href') == '': 
                                break
                            response = requests.get(img.get('data-original'))
                            file = open("static/data/Detail/ThanhNien/"+fn+"/"+fn1 +"/" + file_name  + "_{}.png".format(count_img), "wb")
                            count_img = count_img + 1
                            file.write(response.content)
                            file.close()
                            new_row={'img_name':[file_name], 'img_src':[img.get('data-src')], 'title':[title_detail], 'doc_src':[urla], 'date':[date_time], 'author':[author]}
                        
                            if temp==0:
                                df = pd.DataFrame(new_row)
                                temp=1
                                df.to_csv("static/data/Detail/ThanhNien/"+fn + '/' + fn1 + '/' + fn1 +  '.csv', mode='a', index=False, header=['img_name', 'img_src', 'title', 'doc_src', 'date', 'author'])
                            else:
                                df = pd.DataFrame(new_row)
                                df.to_csv("static/data/Detail/ThanhNien/"+fn + '/' + fn1 + '/' + fn1 +  '.csv', mode='a', index=False, header=False)
                else:
                    continue
            else:
                continue
        except:
            pass
   


        
def crawl_detail_TN():
    URL = 'https://thanhnien.vn'

    reqs = requests.get(URL)
    content = reqs.text
    soup = BS(content, 'html.parser').find('ul',{'class':'menu-nav'})
    for item in soup.find_all('li'):
        try:
            
                link = item.find('a')
                file_name = link.get('title')
                if(os.path.exists("static/data/Detail/ThanhNien/"+file_name)==False):
                    os.makedirs("static/data/Detail/ThanhNien/"+file_name)
                reqs = requests.get(URL+link.get('href'))
                content = reqs.text
                soup = BS(content, 'html.parser').find('div', {'class':'swiper-wrapper'})
                for item1 in soup.findAll('a', {'class':'swiper-slide'}):
                    try:
                        link = item1
                        sub_file_name = link.get('title')
                        if(os.path.exists("static/data/Detail/ThanhNien/"+file_name + "/" + sub_file_name)==False):
                            os.makedirs("static/data/Detail/ThanhNien/"+file_name + "/" + sub_file_name)
                        get_articles_TN('https://thanhnien.vn' + link.get('href'), file_name, sub_file_name)
                    except:
                        pass
        except:
            pass



def crawl_detail_NSVNE():
    URL = 'https://ngoisao.vnexpress.net'
    reqs = requests.get(URL)
    content = reqs.text
    soup = BS(content, 'html.parser').find('ul',{'class':'nav'})

    for item in soup.find_all('li', {'class':''}):
        try:
            link = item.find('a')
            file_name = link.get('title')
            if(os.path.exists("static/data/Detail/SaoStar/"+file_name)==False):
                os.makedirs("static/data/Detail/SaoStar/"+file_name)
            reqs = requests.get(URL+item.find('a').get('href'))
            content = reqs.text
            if BS(content, 'html.parser').find('div',{'class':'head-folder'}):
                soup1 = BS(content, 'html.parser').find('div',{'class':'cate'})
                sub_a = soup1.find_all('a')
                for sub_link in sub_a:
                    try:
                        a = sub_link.get('href')
                        sub_file_name = sub_link.text
                        if(os.path.exists("static/data/Detail/SaoStar/"+file_name + "/" + sub_file_name)==False):
                            os.makedirs("static/data/Detail/SaoStar/"+file_name + "/" + sub_file_name)
                        get_articles_NSVNE(a, file_name, sub_file_name)
                    except:
                        pass
        except:
            pass



    
def crawl_detail_VNE():
    URL = 'https://vnexpress.net'

    reqs = requests.get(URL)
    content = reqs.text
    soup = BS(content, 'html.parser').find('ul',{'class':'parent'})
    hrefs = []
    count = 0
    count_img = 0
    for item in soup.find_all('li'):
        try:
            if 'data-id' in item.attrs:
                link = item.find('a')
                file_name = link.get('title')
                if(os.path.exists("static/data/Detail/VnExpress/"+file_name)==False):
                    os.makedirs("static/data/Detail/VnExpress/"+file_name)
                reqs = requests.get(URL+link.get('href'))
                content = reqs.text
                soup = BS(content, 'html.parser').find('ul', {'class':'ul-nav-folder'})
                for item1 in soup.find_all('li'):
                    try:
                        link = item1.find('a')
                        sub_file_name = link.get('title')
                        if(os.path.exists("static/data/Detail/VnExpress/"+file_name + "/" + sub_file_name)==False):
                            os.makedirs("static/data/Detail/VnExpress/"+file_name + "/" + sub_file_name)
                        if 'data-medium' in link.attrs:
                            # print('https://vnexpress.net' + link.get('href'))
                            get_articles_VNEX('https://vnexpress.net' + link.get('href'), file_name, sub_file_name)
                    except:
                        pass
        except:
            pass



def crawl_detail_ANI():
    URL = 'https://anhnude.info/'
    reqs = requests.get(URL)
    content = reqs.text
    soup = BS(content, 'html.parser').find('ul', {'id': 'primary-navigation'})

    for item in soup.find_all('li'):
        try:
            link = item.find('a')
            file_name = remove_special_chars(link.text)
            if(os.path.exists("static/data/Detail/AnhNude/" + file_name)==False):
                os.makedirs("static/data/Detail/AnhNude/" + file_name)
            
            if link.attrs['href'] != "/":
                get_articles_AN(link.attrs['href'], file_name)
            else:
                get_articles_AN(URL, file_name)
        except:
            pass


def crawl_detail_XAN():
    URL = 'https://xemanhnong.asia/'
    reqs = requests.get(URL)
    content = reqs.text
    soup = BS(content, 'html.parser').find('ul', {'id': 'primary-menu'})

    for item in soup.find_all('li'):
        try:
            link = item.find('a')
            file_name = remove_special_chars(link.text)
            if(os.path.exists("static/data/Detail/AnhNong/" + file_name)==False):
                os.makedirs("static/data/Detail/AnhNong/" + file_name)
            
            if link.attrs['href'] != "/":
                get_articles_XAN(link.attrs['href'], file_name)
            else:
                get_articles_XAN(URL, file_name)
        except:
            pass

