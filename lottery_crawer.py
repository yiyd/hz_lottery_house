from bs4 import BeautifulSoup
from urllib import request
import os
import threading
import queue
import mongo_util
import pdf_util

# url 前缀
index_page_pre = "https://www.hz-notary.com/lottery/index?page.pageNum="
detail_page_pre = "https://www.hz-notary.com/lottery/detail?lottery.id="
content_page_pre = "https://www.hz-notary.com/lottery/detail_content?lotteryContent.id="

class lottery_crawer(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        # 根据队列中的house_id创建线程抓取
        while True:
            index_id = self.queue.get()
            #self.get_house_list(index_id)
            self.get_house_detail(index_id)

            self.queue.task_done()

    # 解析具体楼盘页
    def get_house_detail(self, house_id):
        detail_url = detail_page_pre + house_id
        lottery_soup = BeautifulSoup(request.urlopen(detail_url), 'lxml')
        detail_ul = lottery_soup.find_all(name='ul')[1]
        for li in detail_ul.find_all(name='li'):
            temp = li.a.string
            if ('意向登记' in temp):
                lottery_regist_id = li.a.attrs['href'].split("=")[1]
                print('开始获取意向登记表' + lottery_regist_id)
                self.get_house_conetnt(house_id, lottery_regist_id, 'lottery_regist')

            if ('摇号结果' in temp):
                lottery_result_id = li.a.attrs['href'].split('=')[1]
                print('开始获取摇号结果' + lottery_result_id)
                self.get_house_conetnt(house_id, lottery_result_id, 'lottery_result')

    # 解析文件链接
    def get_house_conetnt(slef, house_id, content_id, pdf_type):
        content_url = content_page_pre + content_id
        lottery_soup = BeautifulSoup(request.urlopen(content_url), 'lxml')
        detail_content = lottery_soup.select('.detail_content')[0].find_all(name='p')

        for p_li in detail_content:
            if p_li.a:
                pdf_url = p_li.a.attrs['href']
                # judge url
                if ('ueditor' in pdf_url):
                    pdf_url = 'https://www.hz-notary.com' + pdf_url

                # get pdf and store in local files
                pdf_util.get_pdf_url(pdf_url, pdf_type + '.pdf', 'files/' + house_id)
                # print(pdf_url)

# 获得总页数
def get_total_number():
    first_url= 'https://www.hz-notary.com/lottery/index?page.pageNum=1'

    # get page number
    lottery_soup = BeautifulSoup(request.urlopen(first_url), 'lxml')
    form_html = lottery_soup.find_all(name='ul')[2]
    span_html = form_html.find_all(name='li')[0]
    num_string = span_html.span.string
    return int(num_string.split('/')[1].split("页")[0])

# 解析目录页(目录页数较少，可以不用开多线程)
def get_house_list(index, queue):
    index_url = index_page_pre + str(index)
    lottery_soup = BeautifulSoup(request.urlopen(index_url), 'lxml')
    house_ul = lottery_soup.find_all(name='ul')[1]
    for li in house_ul.find_all(name='li'):
        house_id = li.div.a.attrs['href'].split("=")[1]
        house_name = str.strip(li.div.a.string)
        house_time = str.strip(li.div.p.string)

        # insert into mongodb
        db = mongo_util.get_db(mongo_util.get_conn())
        house_collection = db['house_test']
        house = {
            'house_id': house_id,
            'house_name': house_name,
            'create_time': house_time
        }
        house_collection.insert_one(house)

        # mkdir house_id
        os.makedirs('files/' + house_id)
        print("开始获取楼盘文件： " + house_name)
        # slef.get_house_detail(house_id)
        queue.put(house_id)
        print(str(index) + ' ' + house_id + ' ' + house_name)
