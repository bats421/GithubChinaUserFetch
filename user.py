import pandas as pd
from utils import FileWriter, GraphQL


class User:
    count = 0
    query = """
   query {
  search(query: "location:China", type: USER, first:%d, after: %s) {
    userCount
    pageInfo {
      startCursor
      hasNextPage
      hasPreviousPage
      endCursor
    }
    edges {
      cursor
      node {
        ... on User {
          name
          login
          location
          url
          bio
          contributionsCollection {
            totalIssueContributions
            totalCommitContributions
            totalRepositoryContributions
            totalPullRequestContributions
            totalPullRequestReviewContributions
            totalRepositoriesWithContributedIssues
          }
          followers {
            totalCount
          }
          repositories {
            totalCount
          }
          organizations {
            totalCount
          }
          pullRequests {
            totalCount
          }
          starredRepositories {
            totalCount
          }
          status {
            message
          }
          company
          websiteUrl
        }
      }
    }
  }
}
"""
    endCursor = "null"

    def __init__(self):
        self.count = 0
        self.data = {}
        self.reform = []
        self.df = None

    def fetch(self, num=10, batch_size=10):
        times = int(num/batch_size)
        if times < 1:
            times = 1
        print("data numbers: %d" % num)
        print("batch_size: %d" % batch_size)
        # times = num
        rest = num % batch_size
        if rest > 0:
            times = times+1
        print("times: %d" % times)
        for i in range(times):
            # print(self.query % self.endCursor)
            print("Request #%d" % (i+1))
            # print(self.endCursor)
            if i == times-1 and rest > 0:
                query = self.query % (rest, self.endCursor)
            else:
                query = self.query % (batch_size, self.endCursor)
            data = GraphQL.execute(query)
            if self.data:
                self.data["search"]["edges"] = self.data["search"]["edges"] + data["search"]["edges"]
                self.data["search"]["pageInfo"] = self.data["search"]["pageInfo"]
            else:
                self.data = data
            self.endCursor = "\"%s\"" % data["search"]["pageInfo"]["endCursor"]
            print("Finshed #%d" % (i+1))
            # print(self.data)

    def preprocessing(self):
        print("Data preprocessing")
        if self.data:
            self.reform = self.data["search"]["edges"]
            cursors = list(map(lambda x: x["cursor"], self.reform))
            self.reform = list(map(lambda x: x["node"], self.reform))
            for (index, i) in enumerate(self.reform):
                self.reform[index]["starredRepositories"] = i["starredRepositories"]["totalCount"]
                self.reform[index]["followers"] = i["followers"]["totalCount"]
                self.reform[index]["pullRequests"] = i["pullRequests"]["totalCount"]
                self.reform[index]["organizations"] = i["organizations"]["totalCount"]
                self.reform[index]["repositories"] = i["repositories"]["totalCount"]
                self.reform[index]["cursor"] = cursors[index]
                if i["bio"]:
                    self.reform[index]["bio"] = i["bio"].replace('\n', '').replace('\r', '')

    def toDataFrame(self):
        self.preprocessing()
        self.df = pd.json_normalize(self.reform)
        print(self.df)

    def saveCSV(self, fileName, mode):
        print("Save data")
        FileWriter.writeFile(self.df, fileName, mode)
