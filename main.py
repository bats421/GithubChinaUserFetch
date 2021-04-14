import user, userRepository, repositoryContributors, userOrganization, repositoryTopic, userPR
import config
from datetime import datetime, timezone, timedelta

if __name__ == '__main__':
  # data = user.User()
  # data.fetch(20, 10)
  # data.toDataFrame()
  # data.saveCSV("test.csv", "w")
  # repo = userRepository.UserRepository("yyx990803")
  # repo.fetch(20, 10)
  # repo.toDataFrame()
  # repo.saveCSV("userRepository.csv", "w")
  # contributors = repositoryContributors.RepositoryContributors("vitejs", "vite")
  # contributors.fetch(10)
  # contributors.toDataFrame()
  # contributors.saveCSV("repoContributors.csv", 'w')
  # orgs = userOrganization.UserOrganization("skyzh")
  # orgs.fetch()
  # orgs.toDataFrame()
  # orgs.saveCSV("userOrgs.csv", 'a')
  # topics = repositoryTopic.RepositoryTopic("vite", "vitejs")
  # topics.fetch()
  # topics.toDataFrame()
  # topics.saveCSV("repositoryTopics.csv", 'a')
  endTime = datetime.now()
  startTime = endTime-timedelta(days=365)
  userPRs = userPR.UserPR("yyx990803", startTime.isoformat(), endTime.isoformat())
  userPRs.fetch(10, 10)
  userPRs.toDataFrame()
  userPRs.saveCSV("userPr.csv", 'a')
  