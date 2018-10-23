import os
import tabula
import queue
from urllib import request
import threading

download_queue = queue.Queue()

class pdf_util(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = download_queue

    def run(self):
        while True:
            # 从下载queue取出地址进行下载
            pdf_info = self.queue.get()
            self.save_pdf(pdf_info[0], pdf_info[1], pdf_info[2])

            self.queue.task_done()

    def save_pdf(self, pdf_url, file_name, file_path):
        try:
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            file_name = '{}{}{}'.format(file_path, os.sep, file_name)
            request.urlretrieve(pdf_url, file_name)
        except IOError as e:
            print('File Failed', e)

        except Exception as e:
            print('error', e)

# 接收下载地址，并放入队列，吊起线程下载
def get_pdf_url(pdf_url, file_name, file_path):
    temp = [pdf_url, file_name, file_path]
    download_queue.put(temp)

def queue_join():
    download_queue.join()

# 解析PDF
def pdf_to_csv(filepath):
    prefix = filepath.split('.')[0]
    # tabula.convert_into(filepath, prefix + '.csv',output_format='csv',java_options="-Dfile.encoding=UTF8")
    df = tabula.read_pdf(filepath, encoding='gbk', pages='all')

    print(df)

    for indexs in df.index:
        print(df.loc[indexs].values[1].strip())
