import threading

import user, userRepository, repositoryContributors, userOrganization, repositoryTopic, userPR
import pandas as pd


#  多线程来加快爬取速度
class myThread(threading.Thread):
    def __init__(self, name, index_range):
        threading.Thread.__init__(self)
        self.name = name
        self.index_range = index_range

    def run(self):
        print("Starting " + self.name)
        repos = pd.read_csv('userRepository.csv')
        login_list = repos['login'].values
        name_list = repos['name'].values
        for i in range(self.index_range[0], self.index_range[1] + 1):
            contributors = repositoryContributors.RepositoryContributors(login_list[i], name_list[i])
            is_url = contributors.fetch(10)
            if is_url:
                flag = contributors.toDataFrame()
                if flag:
                    contributors.saveCSV("repoContributors.csv", 'a+')
        print("Exiting " + self.name)


if __name__ == '__main__':
    thread_list = []
    range_list = [(0, 1000), (1001, 2000), (2001, 3000), (3001, 4000)]

    # 创建新线程
    for i in range(1, 5):
        thread = myThread("Thread-" + str(i), range_list[i - 1])
        thread.start()
        thread_list.append(thread)

    # 等待线程完成
    for thread in thread_list:
        thread.join()
