import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
# 生成数据样本
X,y = make_blobs(n_samples=1000,n_features=2,
           centers=[[-1,-1],[0,0],[1,1],[2,2]],
          cluster_std=[0.4,0.2,0.2,0.2],random_state=666)
 
# plt.scatter(X[:,0],X[:,1])
# plt.show()

from sklearn.cluster import KMeans
 
# 创建KMeans算法对象，设置聚成两类
km = KMeans(n_clusters=2,random_state=666) 
km.fit(X) # 无监督学习，拟合的时候不需要样本标签
y_predict = km.predict(X)  # 预测
plt.scatter(X[:,0],X[:,1],c=y_predict)  # 预测为同一簇的样本同颜色
plt.show()