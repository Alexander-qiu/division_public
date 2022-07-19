# encoding:utf-8

if __name__ == '__main__':
    bucketSum = 100
    layerId = 0
    userIdScale = 100000
    baseLineFlowRate = 0.5
    experimentAreaFlowRate = 1 - baseLineFlowRate

    stateNum = input("请输入您要进行的操作,[1]创建实验层,[2]创建新的实验层,[3]减小实验的流量,[4]增加实验流量,[5]创建跨层实验，")
