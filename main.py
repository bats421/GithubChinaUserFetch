import user, userRepository, repositoryContributors, userOrganization, repositoryTopic, userPR
import config
import pandas as pd
from datetime import datetime, timezone, timedelta

if __name__ == '__main__':
    # data = user.User()
    # data.fetch(1000, 10)
    # data.toDataFrame()
    # data.saveCSV("users.csv", "w")

    # users = pd.read_csv('users.csv')
    # user_list = users['login'].values
    # for user in user_list:
    #   print(user)
    #   repo = userRepository.UserRepository(user)
    #   repo.fetch(1000, 10)
    #   repo.toDataFrame()
    #   repo.saveCSV("userRepository.csv", "a+")
    # a = {}
    # a["a"] = {}
    # a["a"]["a"] = 0
    # print(userRepository.get_data(a, "a", "a"))
    # print(userRepository.get_data(a, "a", "a", "a"))

    repos = pd.read_csv('userRepository.csv')
    login_list = repos['login'].values
    name_list = repos['name'].values
    for (login, name) in zip(login_list, name_list):
        contributors = repositoryContributors.RepositoryContributors(login, name)
        is_url = contributors.fetch(10)
        if is_url:
            flag = contributors.toDataFrame()
            if flag:
                contributors.saveCSV("repoContributors.csv", 'a+')
    # orgs = userOrganization.UserOrganization("skyzh")
    # orgs.fetch()
    # orgs.toDataFrame()
    # orgs.saveCSV("userOrgs.csv", 'a')
    # topics = repositoryTopic.RepositoryTopic("vite", "vitejs")
    # topics.fetch()
    # topics.toDataFrame()
    # topics.saveCSV("repositoryTopics.csv", 'a')
    # endTime = datetime.now()
    # startTime = endTime-timedelta(days=365)
    # userPRs = userPR.UserPR("yyx990803", startTime.isoformat(), endTime.isoformat())
    # userPRs.fetch(10, 10)
    # userPRs.toDataFrame()
    # userPRs.saveCSV("userPr.csv", 'a')
