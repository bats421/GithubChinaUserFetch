import logging
import socket
import time

import pandas as pd
import urllib3

from utils import FileWriter
import requests, config


class RepositoryContributors:
    def __init__(self, login, name):
        self.data = {}
        self.df = None
        self.login = login
        self.name = name

    def fetch(self, num=10):
        url = "https://api.github.com/repos/%s/%s/contributors" % (self.login, self.name)
        header = {
            'Authorization': 'bearer %s' % config.config["token"]}
        try:
            r = requests.get(url, headers=header, timeout=(3, 15))
            print(r.status_code)
            logging.basicConfig(level=logging.WARNING,
                                filename='log.txt',
                                filemode='a+',
                                format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

            if r.status_code == 204 or r.status_code == 404:
                print("不存在该资源，跳过")
                # use logging
                logging.warning("记录个数-404")
                return False
            elif r.status_code == 403:
                time.sleep(60)
                print("流量限制，停止1分钟")
                print(r)
                self.fetch(10)
            else:
                print(url)
                # use logging
                logging.warning("记录个数-200")
                r = r.json()
                print(r)
                if len(r) > num:
                    self.data = r[0:num]
                return True
        except:
            time.sleep(3)
            print("请求超时，从新请求")
            self.fetch(10)

    def toDataFrame(self):
        self.df = pd.json_normalize(self.data)
        # print(self.data)
        if bool(self.data):
            self.df = self.df[["login", "type", "site_admin", "contributions"]]
            self.df['owner'] = self.login
            self.df["name"] = self.name
            print(self.df)
            return True
        else:
            return False

    def saveCSV(self, fileName, mode):
        print("Save data")
        FileWriter.writeFile(self.df, fileName, mode)
