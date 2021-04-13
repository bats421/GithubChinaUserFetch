import pandas as pd
from utils import FileWriter, GraphQL

class UserOrganization:
    count = 0
    query = """
   {
  user(login: "%s") {
    organizations(first: 10, after: %s) {
      pageInfo {
        hasNextPage
        startCursor
        endCursor
      }
      edges {
        cursor
        node {
          name
          description
          login
          location
          url
          websiteUrl
          membersWithRole {
            totalCount
          }
        }
      }
    }
  }
}
"""
    endCursor = "null"

    def __init__(self, login):
        self.data = {}
        self.reform = []
        self.df = None
        self.login = login
        self.hasNextPage = False

    def fetch(self):
        while(True):
          print("Request #%d" % (self.count+1))
          query = self.query % (self.login, self.endCursor)
          data = GraphQL.execute(query)
          self.count = self.count+1
          self.hasNextPage = data["user"]["organizations"]["pageInfo"]["hasNextPage"]
          self.endCursor = "\"%s\"" % data["user"]["organizations"]["pageInfo"]["endCursor"]
          if(self.data):
            self.data["user"]["organizations"]["edges"] = self.data["user"]["organizations"]["edges"]+data["user"]["organizations"]["edges"]
            self.data["user"]["organizations"]["pageInfo"] = data["user"]["organizations"]["pageInfo"]
          else:
            self.data = data
          print("Finshed #%d" % (self.count+1))
          if(self.hasNextPage == False):
            break
    pass
    def preprocessing(self):
      print("Data preprocessing")
      if self.data:
          self.reform = self.data["user"]["organizations"]["edges"]
          cursors = list(map(lambda x: x["cursor"], self.reform))
          self.reform = list(map(lambda x: x["node"], self.reform))
          for (index, i) in enumerate(self.reform):
            self.reform[index]["cursor"] = cursors[index]
            self.reform[index]["membersWithRole"] = i["membersWithRole"]["totalCount"]
            if i["description"]:
              self.reform[index]["description"] = i["description"].replace('\n', '').replace('\r', '')
    def toDataFrame(self):
        self.preprocessing()
        self.df = pd.json_normalize(self.reform)
        self.df["login"] = self.login
        print(self.df)

    def saveCSV(self, fileName, mode):
        print("Save data")
        FileWriter.writeFile(self.df, fileName, mode)
