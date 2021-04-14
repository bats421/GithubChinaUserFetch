from utils import GraphQL, FileWriter
import pandas as pd
class UserPR:
    query = """
    query { 
  user(login: "%s") {
    contributionsCollection(from: "%s", to: "%s") {
      pullRequestContributions(first: %d, after: %s) {
          pageInfo {
        	hasNextPage
          hasPreviousPage
          startCursor
          endCursor
        }
        edges {
            cursor
          node {
            occurredAt
            pullRequest {
              repository {
                name
                owner {
                  login
                }
              }
              permalink
              bodyText
              createdAt
              closed
              merged
              mergedAt
            }
          }
        }
      }
    }
  }
}
"""
    def __init__(self, login, startTime, endTime):
        self.data = {}
        self.login = login
        self.startTime = startTime
        self.endTime = endTime
        self.endCursor = "null"
    def fetch(self, num=10, batch_size=10):
        times = int(num/batch_size)
        if times < 1:
            times = 1
        print("data numbers: %d" % num)
        print("batch_size: %d" % batch_size)
        # times = num
        rest = num % batch_size
        if rest > 0 and times != 1:
            times = times+1
        print("times: %d" % times)
        for i in range(times):
            # print(self.query % self.endCursor)
            print("Request #%d" % (i+1))
            # print(self.endCursor)
            if i == times-1 and rest > 0:
                query = self.query % (self.login, self.startTime, self.endTime, rest, self.endCursor)
            else:
                query = self.query % (self.login, self.startTime, self.endTime, batch_size, self.endCursor)
            data = GraphQL.execute(query)
            if self.data:
                self.data["user"]["contributionsCollection"]["pullRequestContributions"]["edges"] = self.data["user"]["contributionsCollection"]["pullRequestContributions"]["edges"] + data["user"]["contributionsCollection"]["pullRequestContributions"]["edges"]
                self.data["user"]["contributionsCollection"]["pullRequestContributions"]["pageInfo"] = data["user"]["contributionsCollection"]["pullRequestContributions"]["pageInfo"]
            else:
                self.data = data
            print("Finshed #%d" % (i+1))
            self.startCursor = "\"%s\"" % data["user"]["contributionsCollection"]["pullRequestContributions"]["pageInfo"]["startCursor"]
            if not self.data["user"]["contributionsCollection"]["pullRequestContributions"]["pageInfo"]["hasPreviousPage"]:
              print("No more data")
              break
    def preprocessing(self):
        print("Data preprocessing")
        # print(self.data)
        if self.data:
            self.reform = self.data["user"]["contributionsCollection"]["pullRequestContributions"]["edges"]
            cursors = list(map(lambda x: x["cursor"], self.reform))
            self.reform = list(map(lambda x: x["node"], self.reform))
            # pr = list(map(lambda x: x["pullRequest"], self.reform))
            # self.reform.update(pr)
            for (index, i) in enumerate(self.reform):
                self.reform[index]["owner"] = i["pullRequest"]["repository"]["owner"]["login"]
                self.reform[index]["name"] = i["pullRequest"]["repository"]["name"]
                self.reform[index]["permalink"] = i["pullRequest"]["permalink"]
                self.reform[index]["createdAt"] = i["pullRequest"]["createdAt"]
                self.reform[index]["closed"] = i["pullRequest"]["closed"]
                self.reform[index]["merged"] = i["pullRequest"]["merged"]
                self.reform[index]["mergedAt"] = i["pullRequest"]["mergedAt"]
                self.reform[index]["cursor"] = cursors[index]
                if i["pullRequest"]["bodyText"]:
                    self.reform[index]["bodyText"] = i["pullRequest"]["bodyText"].replace('\n', '').replace('\r', '')
                del i["pullRequest"]
    def toDataFrame(self):
        self.preprocessing()
        self.df = pd.json_normalize(self.reform)
        self.df["login"] = self.login
        print(self.df)
    def saveCSV(self, fileName, mode):
        print("Save data")
        FileWriter.writeFile(self.df, fileName, mode)