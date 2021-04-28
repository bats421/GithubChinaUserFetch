import threading

import user, userRepository, userOrganization, repositoryTopic, userPR
from scrap import repositoryContributors
import pandas as pd


#  多线程来加快爬取速度
class myThread(threading.Thread):
    def __init__(self, name, index_range):
        threading.Thread.__init__(self)
        self.name = name
        self.index_range = index_range

    def run(self):
        print("Starting " + self.name)
        repos = pd.read_csv('../userRepository.csv')
        login_list = repos['login'].values
        name_list = repos['name'].values
        for i in range(self.index_range[0], self.index_range[1] + 1):
            topics = repositoryTopic.RepositoryTopic(name_list[i], login_list[i])
            flag = topics.fetch()
            if flag:
                topics.toDataFrame()
                topics.saveCSV("repositoryTopics.csv", 'a+')
            else:
                print("该仓库不存在topic")
        print("Exiting " + self.name)


if __name__ == '__main__':
    thread_list = []
    range_list = [(0, 10000), (10001, 20000), (20001, 30000), (30001, 40000), (40001, 50000), (50001, 60000),
                  (60001, 70000), (70001, 81182)]

    # 创建新线程
    for i in range(1, 9):
        thread = myThread("Thread-" + str(i), range_list[i - 1])
        thread.start()
        thread_list.append(thread)

    # 等待线程完成
    for thread in thread_list:
        thread.join()
