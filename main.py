# This is a sample Python script.
import random

import split
from split import *
from math import *

if __name__ == '__main__':
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


    # create the first experiment，因为是第一层实验，所以并不需要对实验进行分流，按照第一次实验的方式分流即可
    # 定义实验参数, 一个记录比例, 另一个记录实验点
    expRateList = []
    expMarkPointList = []
    experimentRateList1 = [0.1, 0.05, 0.15]  # 输入创建的实验大小
    experimentOneNums = len(experimentRateList1)
    print()

    experimentMarkPointList1 = experiment_mark_point(baseLineRate=baseLineFlowRate, bucketSum=bucketSum,
                                                     experimentRateList=experimentRateList1)

    experimentRateList2 = [0.15, 0.25, 0.05]  # 输入创建的实验大小
    experimentTwoNums = len(experimentRateList2)
    experimentMarkPointList2 = experiment_mark_point(baseLineRate=baseLineFlowRate, bucketSum=bucketSum,
                                                     experimentRateList=experimentRateList2)

    experimentRateList3 = [0.05, 0.05, 0.05]  # 输入创建的实验大小
    experimentThreeNums = len(experimentRateList2)
    experimentMarkPointList3 = experiment_mark_point(baseLineRate=baseLineFlowRate, bucketSum=bucketSum,
                                                     experimentRateList=experimentRateList3)
    # 记录各层流量的比例
    expRateList.append(experimentRateList1)
    expRateList.append(experimentRateList2)
    expRateList.append(experimentRateList3)
    # 记录各个流量标记点的比例
    expMarkPointList.append(experimentMarkPointList1)
    expMarkPointList.append(experimentMarkPointList2)
    expMarkPointList.append(experimentMarkPointList3)

    print()
    for i in range(len(experimentMarkPointList1)):
        if i != len(experimentMarkPointList1) - 1:
            print("\033[34m第" + str(i + 1) + "个实验起始点：\033[0m" + str(experimentMarkPointList1[i]))
        else:
            print("剩余流量的起始点：" + str(experimentMarkPointList1[i]))

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

    # # 验证实验的独立性
    # exp_allocated_independence_show(layerListShow=layerListShow, expNumsListShow=expNumsListShow,
    #                                 userIdScale=userIdScale, expRateList=expRateList,
    #                                 layerWholeAllocated=layerWholeAllocated)


    # 减小流量
    splitLayerSelected = 2
    splitBucketSelected = 2
    splitFlowRate = 0.03  # splitFLowRate 一定要小于整体的大小
    print(expRateList)

    # 减少流量的操作
    try:
        print()
        print("\033[31m 对第" + str() + "层进行减少流量操作 \033[0m")
        layerAdjustedOut = flow_reduce_sdk(splitLayerSelected=splitLayerSelected,
                                           splitBucketSelected=splitBucketSelected,
                                           splitFlowRate=splitFlowRate, expMarkPointList=expMarkPointList,
                                           layerWholeAllocated=layerWholeAllocated, bucketSum=bucketSum)
        print()
        # print("\033[36m减小流量后的剩余流量的结果\033[0m")
        # for i in range(len(layerAdjustedOut)):
        #     print(layerAdjustedOut[i])
    except:
        print()
        print("\033[35m输入流量参数错误，清重新核对流量数据后输入！\033[0m")

    # chose to append flow
    appendLayerSelected = 1
    appendBucketSelected = 1
    appendFlowRate = 0.01

    # 增加流量的操作
    try:
        # print()
        print("\033[31m 进行增加流量操作 \033[0m")
        layerAppendOut = flow_add_sdk(splitLayerSelected=appendLayerSelected, splitBucketSelected=appendBucketSelected,
                                      splitFlowRate=appendFlowRate, expMarkPointList=expMarkPointList,
                                      layerWholeAllocated=layerWholeAllocated, bucketSum=bucketSum)
        # print()
        # print("给第\033[36m " + str(appendLayerSelected) + " \033[0m层第\033[36m " + str(
        #     appendBucketSelected) + " \033[0m个实验增加流量的结果")
        # for i in range(len(layerAppendOut)):
        #     print(layerAppendOut[i])

    except:
        print()
        print("\033[35m输入流量参数错误，清重新核对流量数据后输入！\033[0m")

    print()
    # print("按照通编号排序后的baseLineFlow:")
    # print(baseLineIdFlow)
    # print("实验部分的流量experimentPartIdRecord:")
    # print(experimentAreaIdFlow)
    print("baseline的规模大小")
    print(len(baseLineIdFlow))
    # print("baselined的比例")

    # 对baseline 进行切割划分
    overlappingExpRate = 0.05
    baseLineBucketNums = ceil(baseLineFlowRate * bucketSum)

    [lstRefresh, overlappingExpExtract, baseLineRefreshed] = overlappingExpGen(baseLineBucketNums=baseLineBucketNums,
                                                                               overlappingExpRate=overlappingExpRate,
                                                                               baseLineIdFlow=baseLineIdFlow,
                                                                               bucketSum=bucketSum)
    print()
    print("抽取的重叠层如下：")
    print(lstRefresh)
    # print("抽取的实验结构如下")
    # print(overlappingExpExtract)
    # print("更新后的实验桶号")
    # print(baseLineRefreshed)
    print("成功创建跨层实验")
