from utils import GraphQL, FileWriter
import pandas as pd

from utils.DataProcess import get_data


class RepositoryTopic:
    query = """
    query { 
  repository(name: "%s", owner: "%s") {
    repositoryTopics(first: 20, after: %s) {
      pageInfo {
        endCursor
        hasNextPage
        hasPreviousPage
        startCursor
      }
      edges {
        cursor
        node {
          topic {
            name
          }
        }
      }
    }
  }
}
"""

    def __init__(self, name, owner):
        self.data = {}
        self.name = name
        self.owner = owner
        self.endCursor = "null"
        self.count = 0

    def fetch(self):
        while (True):
            print("Request #%d" % (self.count + 1))
            query = self.query % (self.name, self.owner, self.endCursor)
            data = GraphQL.execute(query)
            # print(data['repository']['repositoryTopics']['pageInfo']['startCursor'])
            if get_data(data, "repository", "repositoryTopics", "pageInfo", "startCursor") is None:
                return False
            self.count = self.count + 1
            if get_data(data, "repository", "repositoryTopics", "pageInfo", "hasNextPage") is not None:
                self.hasNextPage = get_data(data, "repository", "repositoryTopics", "pageInfo", "hasNextPage")
            if get_data(data, "repository", "repositoryTopics", "pageInfo", "endCursor") is not None:
                self.endCursor = "\"%s\"" % get_data(data, "repository", "repositoryTopics", "pageInfo", "endCursor")
            if (self.data):
                if get_data(data, "repository", "repositoryTopics", "edges") is not None:
                    self.data["repository"]["repositoryTopics"]["edges"] = self.data["repository"]["repositoryTopics"][
                                                                               "edges"] + get_data(data, "repository",
                                                                                                   "repositoryTopics",
                                                                                                   "edges")
                if get_data(data, "repository", "repositoryTopics", "pageInfo") is not None:
                    self.data["repository"]["repositoryTopics"]["pageInfo"] = get_data(data, "repository",
                                                                                       "repositoryTopics", "pageInfo")
            else:
                self.data = data
            print("Finshed #%d" % (self.count + 1))
            if (self.hasNextPage == False):
                print("No more data")
                return True

    def preprocessing(self):
        print("Data preprocessing")
        if self.data:
            self.reform = self.data["repository"]["repositoryTopics"]["edges"]
            cursors = list(map(lambda x: x["cursor"], self.reform))
            self.reform = list(map(lambda x: x["node"], self.reform))
            for (index, i) in enumerate(self.reform):
                self.reform[index]["cursor"] = cursors[index]
                self.reform[index]["topic"] = i["topic"]["name"]

    def toDataFrame(self):
        self.preprocessing()
        self.df = pd.json_normalize(self.reform)
        self.df["owner"] = self.owner
        self.df["name"] = self.name
        print(self.df)

    def saveCSV(self, fileName, mode):
        print("Save data")
        FileWriter.writeFile(self.df, fileName, mode)
