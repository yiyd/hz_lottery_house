import lottery_crawer
import pdf_util
import queue

def main():
    total_page_num = lottery_crawer.get_total_number()
    #
    # for i in range(1, total_page_num):
    #     print("正在获取第" + str(i) + "页\n")
    #     lottery_crawer.get_house_list(i)

    #pdf_util.pdf_to_csv('files/0abcb5d6ca314413a55590f921667d69/lottery_regist.pdf')

    # 利用lottery_crawer创建爬虫线程池 默认20
    # 线程池用队列
    # lottery_queue = queue.Queue()
    # for i in range(20):
    #     t1 = lottery_crawer.lottery_crawer(lottery_queue)
    #     t2 = pdf_util.pdf_util()
    #     t1.setDaemon(True)
    #     t2.setDaemon(True)
    #     t1.start()
    #     t2.start()
    #
    # for i in range(1, total_page_num):
    #     lottery_crawer.get_house_list(i, lottery_queue)
    #
    # lottery_queue.join()
    # pdf_util.queue_join()

    # pdf_util.pdf_to_csv('files/edaa041a95a547b0a95c9e4bf712a71e/lottery_regist.pdf')

if __name__ == '__main__':
    main()