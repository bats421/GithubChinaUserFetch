import matplotlib
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
from sklearn import preprocessing
from sklearn.cluster import KMeans, DBSCAN, SpectralClustering
from sklearn.decomposition import PCA
import pandas as pd

pd.set_option('display.max_columns', 1000)

pd.set_option('display.width', 1000)

pd.set_option('display.max_colwidth', 1000)

data = pd.read_csv("../userRepository.csv", header=0)
fColumns = [
    'commitComments',
    'forkCount',
    'stargazerCount', 'issues', 'diskUsage', 'pullRequests', 'watchers'
]

# scatter_matrix(
#     data[fColumns],
#     figsize=(10, 10), diagonal="hist")

# dCorr = data[fColumns].corr()
# print(dCorr)

# # 降维
# pca_2 = PCA(n_components=2)
# data_pca_2 = pd.DataFrame(
#     pca_2.fit_transform(data[fColumns]))
#
# plt.scatter(
#     data_pca_2[0],
#     data_pca_2[1])
#
# plt.show()

newColumns = ['commitComments', 'forkCount', 'stargazerCount', 'issues', 'watchers']
# kmModel = KMeans(n_clusters=2)
# kmModel = kmModel.fit(data[newColumns])
# 对图像进行分类
# pTarget = kmModel.predict(data[newColumns])

minmax = preprocessing.MinMaxScaler()
my_data = minmax.fit_transform(data[newColumns])
dbsModel = SpectralClustering().fit_predict(my_data)

pca = PCA(2)
pData = pca.fit_transform(my_data)


plt.scatter(
    pData[:, 0],
    pData[:, 1],
    c=dbsModel
)
plt.show()

# # 设置聚类数量
# n_clusters = 5
#
# # 建立聚类模型对象
# kmeans = KMeans(n_clusters=n_clusters, random_state=2018)
