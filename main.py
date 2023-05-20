from crawl_chitiet import *
from crawl_tongquat import *

def main(web, mode):

    if web == 'https://xemanhnong.asia/':
        if mode == 'detail':
            crawl_detail_XAN()
        else:
            crawl_img_only_XAN()
            
    if web == 'https://anhnude.info':
        if mode == 'detail':
            crawl_detail_ANI()
        else:
            crawl_img_only_AN()  

    if web == 'https://vnexpress.net':
        if mode == 'detail':
            crawl_detail_VNE()
        else:
            crawl_img_only_VNE()        

    if web == 'https://ngoisao.vnexpress.net':
        if mode == 'detail':
            crawl_detail_NSVNE()
        else:
            crawl_img_only_NSVNE()        

    if web == 'https://thanhnien.vn':
        if mode == 'detail':
            crawl_detail_TN()
        else:
            crawl_img_only_TN()        