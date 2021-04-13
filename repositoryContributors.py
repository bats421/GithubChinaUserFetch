import pandas as pd
from utils import FileWriter
import requests, config

class RepositoryContributors:
    def __init__(self, login, name):
        self.data = {}
        self.df = None
        self.login = login
        self.name = name

    def fetch(self, num = 10):
      url = "https://api.github.com/repos/%s/%s/contributors" % (self.login, self.name)
      header = {
            'Authorization': 'bearer %s' % config.config["token"]}
      r = requests.get(url, headers = header)
      r = r.json()
      if len(r) > num:
        self.data = r[0:num]

    def toDataFrame(self):
        self.df = pd.json_normalize(self.data)
        self.df = self.df[["login", "type", "site_admin", "contributions"]]
        self.df['repo_name'] = self.login+"/"+self.name
        print(self.df)

    def saveCSV(self, fileName, mode):
        print("Save data")
        FileWriter.writeFile(self.df, fileName, mode)
