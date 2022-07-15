# encoding:utf-8

from split import *
from math import *

bucketSum = 100
layerId = 0
userIdScale = 10000
baseLineFlowRate = 0.5
experimentAreaFlowRate = 1 - baseLineFlowRate

# 生成用户ID, 基础分桶
print()
userId = gen_userId_inorder(userIdScale)
(baseLineIdFlow, experimentAreaIdFlow) = \
    spilt_baseline(bucketSum=bucketSum, layerId=layerId, userId=userId,
                   baseLineFlowRate=baseLineFlowRate, userIdScale=userIdScale)

expRateList = []
expMarkPointList = []

# 这个是输入的数值
print("\033[31m 请输入创建的实验流量情况 \033[0m:")

data = input("请输入第2个实验的流量: ")
print(data)

experimentRateList1 = [0.1, 0.05, 0.15]  # 输入创建的实验大小

experimentOneNums = len(experimentRateList1)

print()
experimentMarkPointList1 = experiment_mark_point(baseLineRate=baseLineFlowRate, bucketSum=bucketSum,
                                                 experimentNum=experimentOneNums,
                                                 experimentRateList=experimentRateList1)