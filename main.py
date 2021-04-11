import user
import config

if __name__ == '__main__':
  data = user.User()
  data.fetch(20, 10)
  data.toDataFrame()
  data.saveCSV("test.csv", "w")