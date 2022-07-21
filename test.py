# This is a sample Python script.
import random

from split import *
from math import *

if __name__ == '__main__':
    bucketSum = 100
    layerId = 0
    userIdScale = 10000
    baseLineFlowRate = 0.5
    experimentAreaFlowRate = 1 - baseLineFlowRate

    userId = gen_userId_inorder(userIdScale)
    (baseLineIdFlow, experimentAreaIdFlow) = \
        spilt_baseline(bucketSum=bucketSum, layerId=layerId, userId=userId,
                       baseLineFlowRate=baseLineFlowRate, userIdScale=userIdScale)

    # create the first experiment，因为是第一层实验，所以并不需要对实验进行分流，按照第一次实验的方式分流即可
    # 定义实验参数, 一个记录比例, 另一个记录实验点
    expRateList = []
    expMarkPointList = []
    experimentRateList1 = [0.1, 0.05, 0.15]  # 输入创建的实验大小
    experimentRateList2 = [0.15, 0.25, 0.05]  # 输入创建的实验大小
    experimentRateList3 = [0.05, 0.05, 0.05]  # 输入创建的实验大小
    experimentOneNums = len(experimentRateList1)
    experimentTwoNums = len(experimentRateList2)
    experimentThreeNums = len(experimentRateList3)

    print()
    # 这三层可以采用函数的方式进行调用,问题是如何统一调用呢？
    experimentMarkPointList1 = experiment_mark_point(baseLineRate=baseLineFlowRate, bucketSum=bucketSum,
                                                     experimentRateList=experimentRateList1)
    experimentMarkPointList2 = experiment_mark_point(baseLineRate=baseLineFlowRate, bucketSum=bucketSum,
                                                     experimentRateList=experimentRateList2)
    experimentMarkPointList3 = experiment_mark_point(baseLineRate=baseLineFlowRate, bucketSum=bucketSum,
                                                     experimentRateList=experimentRateList3)

    # 记录各层流量的比例
    # 根据最终的结构再往上增添
    expRateList.append(experimentRateList1)
    expRateList.append(experimentRateList2)
    expRateList.append(experimentRateList3)

    # 记录各个流量标记点的比例
    expMarkPointList.append(experimentMarkPointList1)
    expMarkPointList.append(experimentMarkPointList2)
    expMarkPointList.append(experimentMarkPointList3)

    [layer1, layer2, layer3] = [1, 2, 3]
    # 创建重叠实验区
    expLayerOne = experiment_shuffle(experimentAreaRate=experimentAreaFlowRate, layerId=layer1,
                                     bucketSum=bucketSum, experimentAreaIdFlow=experimentAreaIdFlow)
    expLayerTwo = experiment_shuffle(experimentAreaRate=experimentAreaFlowRate, layerId=layer2,
                                     bucketSum=bucketSum, experimentAreaIdFlow=experimentAreaIdFlow)
    expLayerThree = experiment_shuffle(experimentAreaRate=experimentAreaFlowRate, layerId=layer3,
                                       bucketSum=bucketSum, experimentAreaIdFlow=experimentAreaIdFlow)

    # 实验区筛选分流
    layerWholeAllocated = []
    layer1FlowAllocated = experiment_flow_allocation(expLayerSlected=expLayerOne,
                                                     experimentMarkPointList=experimentMarkPointList1,
                                                     bucketSum=bucketSum)
    layer2FlowAllocated = experiment_flow_allocation(expLayerSlected=expLayerTwo,
                                                     experimentMarkPointList=experimentMarkPointList2,
                                                     bucketSum=bucketSum)
    layer3FlowAllocated = experiment_flow_allocation(expLayerSlected=expLayerThree,
                                                     experimentMarkPointList=experimentMarkPointList3,
                                                     bucketSum=bucketSum)
    layerWholeAllocated.append(layer1FlowAllocated)
    layerWholeAllocated.append(layer2FlowAllocated)
    layerWholeAllocated.append(layer3FlowAllocated)
    # layerWholeAllocated 存储了整个层的信息

    # 定义层间展示结构
    layerListShow = []
    layerListShow.append(layer1)
    layerListShow.append(layer2)
    layerListShow.append(layer3)
    expNumsListShow = [experimentOneNums, experimentTwoNums, experimentThreeNums]

    # 验证实验的独立性
    print("测试实验分配的独立性")
    exp_allocated_independence_show(layerListShow=layerListShow, expNumsListShow=expNumsListShow,
                                    userIdScale=userIdScale, expRateList=expRateList,
                                    baseLineFlowRate=baseLineFlowRate,
                                    layerWholeAllocated=layerWholeAllocated)
    # 减小流量
    splitLayerSelected = 2
    splitBucketSelected = 2
    splitFlowRate = 0.03  # splitFLowRate 一定要小于整体的大小
    # print("此时各实验层的流量结构如下所示")
    # print(expRateList)

    # # 减少流量的操作
    # try:
    #     print()
    #     print("\033[31m> 对第" + str(splitLayerSelected) + "层进行减少流量操作 \033[0m")
    #     layerAdjustedOut = flow_reduce_inOrder(splitLayerSelected=splitLayerSelected,
    #                                            splitBucketSelected=splitBucketSelected,
    #                                            splitFlowRate=splitFlowRate, expMarkPointList=expMarkPointList,
    #                                            layerWholeAllocated=layerWholeAllocated, bucketSum=bucketSum)
    #     print("成功对第\033[36m " + str(splitLayerSelected) + " \033[0m层第\033[36m " + str(splitBucketSelected)
    #           + " \033[0m实验减少\033[36m " + str(splitFlowRate * 100) + "% \033[0m流量")
    # except:
    #     print()
    #     print("\033[35m输入流量参数错误，清重新核对流量数据后输入！\033[0m")

    # chose to append flow
    appendLayerSelected = 1
    appendBucketSelected = 1
    appendFlowRate = 0.01

    # # 增加流量的操作
    # try:
    #     print()
    #     print("\033[31m> 对第" + str(appendLayerSelected) + "层增加流量操作 \033[0m")
    #     layerAppendOut = flow_add_inOrder(splitLayerSelected=appendLayerSelected, splitBucketSelected=appendBucketSelected,
    #                                       splitFlowRate=appendFlowRate, expMarkPointList=expMarkPointList,
    #                                       layerWholeAllocated=layerWholeAllocated, bucketSum=bucketSum)
    #     print("成功对第\033[36m " + str(appendLayerSelected) + " \033[0m层第\033[36m " + str(appendBucketSelected)
    #           + " \033[0m实验增加\033[36m " + str(appendFlowRate * 100) + "% \033[0m流量")
    #
    # except:
    #     print()
    #     print("\033[35m输入流量参数错误，清重新核对流量数据后输入！\033[0m")

    print()
    print("baseline的规模大小")
    print(len(baseLineIdFlow))

    # 对baseline 进行切割划分
    overlappingExpRate = 0.05
    baseLineBucketNums = ceil(baseLineFlowRate * bucketSum)

    [lstRefresh, overlappingExpExtract, baseLineRefreshed] = overlappingExpGen(baseLineBucketNums=baseLineBucketNums,
                                                                               overlappingExpRate=overlappingExpRate,
                                                                               baseLineIdFlow=baseLineIdFlow,
                                                                               bucketSum=bucketSum)
    print("\033[32m跨层实验桶如下：\033[0m")
    print(lstRefresh)
    print("成功创建跨层实验！")

    regionRate = 0.2
    regionIdFlow = regionId_flow_gen(userId, regionRate)

    print()
    [regionExtracted, regionRemain] = region_division(userId, regionIdFlow)
    print("\033[36m北京地区的流量情况：\033[0m")
    # print(regionExtracted)
    print("共计: \033[36m" + str(len(regionExtracted)) + "\033[0m")
    # you can use regionRemain to get the remain






    # 更改减小流量的操作逻辑
    splitLayerSelected = 2
    splitBucketSelected = 3
    splitFlowRate = 0.03  # splitFLowRate 一定要小于整体的大小
    print()
    print("此时各实验层的流量结构如下所示")
    print(expRateList)
    # for i in range(len(layerWholeAllocated)):
    #     print("第" + str(i+1) + "层：" )
    #     for j in range(len(layerWholeAllocated[i])):
    #         print(layerWholeAllocated[i][j])

    expBucketWholeStructureList = []
    for i in range(len(expMarkPointList)):
        expBucketStructureList =[]
        expMarkPointSelected = expMarkPointList[i]
        expMarkPointSelected.append(bucketSum)
        # print(expMarkPointSelected)
        for i in range(len(expMarkPointSelected) - 1):
            cont = expMarkPointSelected[i]
            expBucketSingleLayer = []
            while cont < expMarkPointSelected[i+1] :
                expBucketSingleLayer.append(round(cont))
                cont += 1
            expBucketStructureList.append(expBucketSingleLayer)
        # for i in range(len(expBucketStructureList)):
        #     print(expBucketStructureList[i])
        expBucketWholeStructureList.append(expBucketStructureList)


    # 存储了结构的信息 expBucketWholeStructureList
    print()
    print("\033[31m> 对第" + str(splitLayerSelected) + "层进行减少流量操作 \033[0m")
    expSelectedRate = expRateList[splitLayerSelected]
    print(expSelectedRate)
    expSelectedRate[splitBucketSelected - 1] += splitFlowRate
    print("调整流量后的")
    print(expSelectedRate)
    [layerAdjustedOut, experimentFlowList] \
        = flow_reduce(splitLayerSelected=splitLayerSelected,
                      splitBucketSelected=splitBucketSelected,
                      splitFlowRate=splitFlowRate, expBucketWholeStructureList=expBucketWholeStructureList,
                      layerWholeAllocated=layerWholeAllocated, bucketSum=bucketSum)

    print("成功对第\033[36m " + str(splitLayerSelected) + " \033[0m层第\033[36m " + str(splitBucketSelected)
              + " \033[0m实验增加\033[36m " + str(splitFlowRate * 100) + "% \033[0m流量")