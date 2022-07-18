# encoding:utf-8
# this part is difined to create division nums

import copy
import hashlib
import math
import random
import numpy as np


def gen_md5(userId, layerId):
    layerIdStr = str(layerId)
    baseStr = ["4paradigm", "qiuruizhi", "Alexander", "polaris"]
    baseStrSelect = baseStr[layerId % len(baseStr)]
    preStr = ["4paradigm", "qiuruizhi", "Alexander", "polaris", "buaa", "division"]
    preStrSelect = preStr[layerId % len(preStr)]

    userIdPlusLayer = preStrSelect + userId + baseStrSelect + layerIdStr

    userIdMd5 = hashlib.md5()
    userIdMd5.update(userIdPlusLayer.encode(encoding='utf-8'))
    userIdMd5Convert10 = int(userIdMd5.hexdigest(), 16)  # 16进制转成10进制
    return userIdMd5Convert10


# test the division and print it
def create_division(userId, layerId, bucketSum):
    userIdMd5Convert10 = gen_md5(userId, layerId)
    bucketNum = userIdMd5Convert10 % bucketSum
    print(bucketNum)
    return


# generate bucket num
def gen_spilt(userId, layerId, bucketSum):
    userIdMd5Convert10 = gen_md5(userId, layerId)
    bucketNum = userIdMd5Convert10 % bucketSum
    return bucketNum


def gen_userId(userIdScale):
    userIdGen = []
    for i in range(userIdScale):
        userIdGen.append(str(i))
    return userIdGen



def print_division(userId, layerId):
    # userId = 12345
    # layerId = 1
    bucketSum = 100
    create_division(userId, layerId, bucketSum)
    return


def gen_userId_inorder(userIdScale):
    userIdGen = []
    for i in range(userIdScale):
        userIdGen.append(str(i))
    return userIdGen


# 分出baseline的流量
def spilt_baseline(bucketSum, layerId, userId, baseLineFlowRate, userIdScale):
    bucketCount = [0 for i in range(bucketSum)]
    userIdSpiltLayer1 = []
    baseLineIdRecord = []
    experimentPartIdRecord = []

    # print(bucketCount)
    for i in range(len(userId)):
        bucketNum = gen_spilt(userId=userId[i], layerId=layerId, bucketSum=bucketSum)

        # 将每个userId的桶编号及逆行标记
        userIdSpiltLayer1.append(bucketNum)  # record the bucketNum
        # print(userId[i], userIdSpiltLayer1[i])
        if bucketNum < bucketSum * baseLineFlowRate:  # 分流，但不按照原有顺序进行
            baseLineIdRecord.append([userId[i], userIdSpiltLayer1[i]])
        else:
            experimentPartIdRecord.append([userId[i], userIdSpiltLayer1[i]])
        bucketCount[bucketNum] += 1

    # print("实验一各个userId的分桶情况：")
    # print(userIdSpiltLayer1)
    print("基础分桶时通过各桶的流量情况：")
    print(bucketCount)
    print("\033[33m流经桶流量的最大值\033[0m")
    print(min(bucketCount))
    print("\033[33m流经桶流量的最小值\033[0m")
    print(max(bucketCount))

    # split the user in baseline
    # In this part we will use num to spilt the userID
    # print("baseLineFlow:")
    # print(baseLineIdRecord)
    print("总的流量大小：" + str(userIdScale) + ";  基线流量截取的流量比例：" + str(baseLineFlowRate) + ";  baseline的流量：" + str(
        len(baseLineIdRecord)))
    baseLineIdRecord.sort(key=lambda x: x[1])  # 比较第二个元素
    experimentPartIdRecord.sort(key=lambda x: x[1])

    # now we have the baseLineIdRecord and the experimentId, in next part we will rescale the experiment
    return (baseLineIdRecord, experimentPartIdRecord)


def rescale_the_flowRate():
    # 之后要改个二分查找
    return


# 二分查找返回分流值
def binary_search(baseList, aim):
    baseList.sort()
    low = 0
    high = len(baseList)
    mid = low + (high - low) / 2
    while low < high:
        mid = low + (high - low) / 2
        if aim == baseList[mid]:
            return mid
        elif aim > baseList[mid]:
            low = mid + 1
        else:
            high = mid - 1
    return None


# 返回多元组list的第几个元素, 从0开始
def get_list_inorder(baseList, order):
    if len(baseList) < 1:
        return 0
    elif order >= len(baseList[0]):
        return - 1
    listReturn = []
    for element in baseList:
        listReturn.append(element[order])
    return listReturn


# Attention! This part is experimentAreaIdFlow, which is different from baseLineFlowRate.
# It shows the experiment flow rate which divide the experiment part.
# we should know that we are just shuffling the bucket.Inside, we reshuffling the whole id
def experiment_shuffle(experimentAreaRate, layerId, bucketSum, experimentAreaIdFlow):
    # use ceil according to the < before
    shuffleBucketNums = math.ceil(bucketSum * experimentAreaRate)  # 需要洗牌的桶数
    baseLineMark = math.ceil(bucketSum * experimentAreaRate)  # 标记点，从哪里开始计数
    bucketShuffledReturn = []  #
    experimentAreaIdList = get_list_inorder(experimentAreaIdFlow, 0)  # 得到实验部分的用户ID
    layerId = layerId* 10 + 2
    for i in range(len(experimentAreaIdList)):
        bucketShuffledId = gen_spilt(userId=str(experimentAreaIdList[i]), layerId=layerId,
                                           bucketSum=shuffleBucketNums)  # 计算洗牌后的编号
        bucketShuffledId += baseLineMark
        bucketShuffledReturn.append([experimentAreaIdList[i], bucketShuffledId])

    # print("第" + str(layerId) + "层前，洗牌的实验分桶情况:")
    # print(bucketShuffledReturn)
    bucketShuffledReturn.sort(key=lambda x: x[1])
    return bucketShuffledReturn


# 划分流量的分桶
def experiment_mark_point(baseLineRate, bucketSum, experimentRateList):
    if sum(experimentRateList) + baseLineRate > 1:
        print("\033[31m超出流量的的最大值，请重新设定流量大小\033[31m")
        return 0
    else:
        experimentMarkPoint = []
        remainFlow = 1 - baseLineRate
        print("创建实验层成功，桶结点如下所示：")
        # 计算各个阶段的流量
        contentMarkPoint = baseLineRate * bucketSum
        experimentMarkPoint.append(contentMarkPoint)
        for i in range(len(experimentRateList)):
            contentMarkPoint += experimentRateList[i] * bucketSum
            experimentMarkPoint.append(contentMarkPoint)
        print(experimentMarkPoint)
    return experimentMarkPoint


# correct
def experiment_flow_allocation(expLayerSlected, experimentMarkPointList, bucketSum):
    flowAllocatedReturn = []
    countStart = round(experimentMarkPointList[0])
    count = 0  # 记录第一个标记点
    for i in range(len(experimentMarkPointList)):
        singleExpAllocated = []

        # 其实是相当于遍历一遍
        if i < len(experimentMarkPointList) - 1:
            while expLayerSlected[count][1] < experimentMarkPointList[i + 1]:
                singleExpAllocated.append(expLayerSlected[count])
                count += 1
        else:
            while count < len(expLayerSlected):
                singleExpAllocated.append(expLayerSlected[count])
                count += 1
        flowAllocatedReturn.append(singleExpAllocated)
    # 展示结构
    # print("标号位置")
    # print(experimentMarkPointList)
    #
    # for i in range(len(flowAllocatedReturn)):
    #     print("\033[31m 第" +  str(i+1) + "个实验的分配情况\033[0m")
    #     print(flowAllocatedReturn[i])
    return flowAllocatedReturn


# 传入实验层和 实验编号
def exp_allocated_show(experimentElementNums, expMark, layer1FlowAllocated):
    # print("\033[31m 第" + str(expMark) + "个实验的分配情况 \033[0m")
    MemberInTotal = []
    experimentOneNums = experimentElementNums
    for i in range(experimentOneNums + 1):
        layer1Exp = layer1FlowAllocated[i]
        # if i < experimentOneNums:
        #     print("\033[31m 第" + str(expMark) + "个实验第" + str(i + 1) + "实验的分配情况是：\033[0m")
        # else:
        #     print("\033[34m 剩余流量是: \033[0m")
        # print(layer1Exp)
        layer1ExpSort = copy.deepcopy(layer1Exp)
        layer1ExpSort.sort(key=lambda x: x[0])
        # print("\033[35m 重新按序号排序后的数量和标号: \033[0m")
        # print(layer1ExpSort)
        # print("\033[32m共计： \033[0m" + str(len(layer1Exp)))
        MemberInTotal.append(len(layer1Exp))
    return MemberInTotal


# def allocatedTest
def test_allocated_independence(userIdScale, rateList, layerWholeAllocated, expStruct):

    wholeIdTable = [0 for i in range(userIdScale)]
    overlappingIdList = []
    overlappingIdCount = 0
    overlappingLayerNums = len(expStruct)  # use this to difination
    numberInTheory = userIdScale       # the case for overlapping in theory
    rateInTest = []

    # 创建概率列表
    for i in range(overlappingLayerNums):
        layerSelect = expStruct[i][0] - 1
        rateSelect = expStruct[i][1] - 1
        rateInTest.append(rateList[layerSelect][rateSelect])
    print("\033[31m抽取的比例列表\033[0m")
    print(rateInTest)
    print(expStruct)

    for rate in rateInTest:
        numberInTheory *= rate
    # print("\033[31m理论上的人员数目:\033[0m")
    # print(numberInTheory)

    # 染色标记命中实验的情况，两层for循环，分别统计两个的情况
    for layerCount in range(overlappingLayerNums):
        # layerSelect = expStruct[layerCount][0] - 1
        flowSelect = expStruct[layerCount][1] - 1
        # 三个维度实验层 流量分块, 第一步是抽取实验层, 总体结构是没问题的
        print("第" + str(layerCount+1) + "层抽取了第" + str(flowSelect+1) + "个实验" )
        layerExp = layerWholeAllocated[layerCount][flowSelect]
        # print(layerExp)
        print("\033[34m 抽取的比例是: " + str(rateInTest[layerCount]) + " 抽取的数目是: " + str(len(layerExp)) + "\033[0m")
        # 这一部分没问题
        userIdElementList = []

        # 针对实验层大小进行统计
        for elementCount in range(len(layerExp)):
            userIdElement = int(layerExp[elementCount][0])
            userIdElementList.append(userIdElement)
            wholeIdTable[userIdElement] += 1
        userIdElementList.sort()
        # print(userIdElementList)

    # 用户数量统计
    for userIdCode in range(len(wholeIdTable)):
        if wholeIdTable[userIdCode] == overlappingLayerNums:
            overlappingIdCount += 1
            overlappingIdList.append(userIdCode)

    print("\033[31m理论上的人员数目:\033[0m")
    print(numberInTheory)
    print("\033[31m重叠的层内同时经过实验的的Id数量：\033[0m")
    print(overlappingIdCount)
    # print("\033[31m Id统计：\033[0m")
    # print(overlappingIdList)
    print()

    particleOverTheory = overlappingIdCount/ numberInTheory
    return [rateInTest, round(numberInTheory), overlappingIdCount, round(particleOverTheory, 2)]


# [[],[],[]] 三层可以看成两层的组合
def generate_two_layers_combination(rateList):
    expStructList = []
    # userLayer
    for i in range(len(rateList[0])):
        for j in range(len(rateList[1])):
            lay1 = i + 1
            lay2 = j + 1
            expStructList.append([[1, lay1], [2, lay2]])
    print("全部的组合情况：")
    print(expStructList)
    return expStructList


def exp_allocated_independence_show(layerListShow, expNumsListShow, userIdScale, expRateList, layerWholeAllocated):
    # # show the allocated
    [layer1, layer2, layer3] = layerListShow
    [experimentOneNums, experimentTwoNums, experimentThreeNums] = expNumsListShow
    MemberInExpOne = exp_allocated_show(experimentOneNums, layer1, layerWholeAllocated[0])
    MemberInExpTwo = exp_allocated_show(experimentTwoNums, layer2, layerWholeAllocated[1])
    MemberInExpThree = exp_allocated_show(experimentThreeNums, layer3, layerWholeAllocated[2])
    experimentRateList1 = expRateList[0]
    experimentRateList2 = expRateList[1]
    experimentRateList3 = expRateList[2]

    print()
    print("\033[34m理论上第一层的分配人数情况：\033[0m")
    print([round(i * userIdScale) for i in experimentRateList1])
    print("\033[31m第一个实验的分配人数情况：\033[0m")
    print(MemberInExpOne)
    print("\033[34m理论上第二层的分配人数情况：\033[0m")
    print([round(i * userIdScale) for i in experimentRateList2])
    print("\033[31m第二个实验的分配人数情况：\033[0m")
    print(MemberInExpTwo)
    print("\033[34m理论上第三层的分配人数情况：\033[0m")
    print([round(i * userIdScale) for i in experimentRateList3])
    print("\033[31m第三个实验的分配人数情况：\033[0m")
    print(MemberInExpThree)

    # # 流量测试，看是否能复合重叠的标准和要求
    # 定义抽取的跨层实验结构
    # 假设输入的数据结构是完全正确的
    # 全部测试
    expStruct = []
    layerExpBase1 = [1, 1]
    expStruct.append(layerExpBase1)
    layerExpBase2 = [2, 1]
    expStruct.append(layerExpBase2)

    print()
    expRateListTest = [experimentRateList1, experimentRateList2]
    print("要测试的跨层实验情况")
    print(expRateListTest)
    expStructList = generate_two_layers_combination(rateList=expRateListTest)

    testResultList = []
    # 仅考虑前两层的情况
    for i in range(len(expStructList)):
        expStruct = expStructList[i]
        testResult = test_allocated_independence(userIdScale=userIdScale, rateList=expRateList,
                                                 layerWholeAllocated=layerWholeAllocated, expStruct=expStruct)
        testResultList.append(testResult)

    testResultRateExtract = get_list_inorder(testResultList, 0)
    testResultMemberNumsInTheory = get_list_inorder(testResultList, 1)
    testResultMemberNumsInParticle = get_list_inorder(testResultList, 2)
    testResultBiasRate = get_list_inorder(testResultList, 3)

    print("\033[031m抽取的跨层实验比例:\033[0m")
    print(testResultRateExtract)
    print("\033[031m理论上的人员数目:\033[0m")
    print(testResultMemberNumsInTheory)
    print("\033[031m重叠层内的通过重叠实验的ID数量:\033[0m")
    print(testResultMemberNumsInParticle)
    print("\033[031m偏差的比例:\033[0m")
    print(testResultBiasRate)

    return


# 流量减小操作
def flow_reduce_sdk(splitLayerSelected, splitBucketSelected, splitFlowRate, expMarkPointList, layerWholeAllocated, bucketSum):

    layer1FlowSpilt = []
    flowAdjustRemain = []
    flowAdjustOut = []
    experimentMarkPointList1 = expMarkPointList[splitLayerSelected - 1]
    layer1FlowAllocated = layerWholeAllocated[splitLayerSelected - 1]
    print("层 \033[36m"+str(splitLayerSelected)+"\033[0m 各流量的标记点")
    print(experimentMarkPointList1)
    adjustMarkPoint = experimentMarkPointList1[splitBucketSelected] - splitFlowRate * bucketSum
    print("分割桶的标记位置")
    print(adjustMarkPoint)

    for i in range(len(layer1FlowAllocated)):
        if i == splitBucketSelected - 1:
            # layer1FlowSpilt.append(layer1FlowAllocated[i])
            # layer1FlowSpilt.append(layer1FlowAllocated[i])
            for j in range(len(layer1FlowAllocated[i])):
                if layer1FlowAllocated[i][j][1] < adjustMarkPoint:
                    flowAdjustRemain.append(layer1FlowAllocated[i][j])
                else:
                    flowAdjustOut.append(layer1FlowAllocated[i][j])
            layer1FlowSpilt.append(flowAdjustRemain)
            layer1FlowSpilt.append(flowAdjustOut)
        else:
            layer1FlowSpilt.append(layer1FlowAllocated[i])

    # 标记结束后的情况
    markSpiltAdjustPoint = []
    print()
    # print("\033[32m调整流量后实验层"+str(splitLayerSelected)+"的分配情况:\033[0m")
    for i in range(len(layer1FlowSpilt)):
        # print(layer1FlowSpilt[i])
        markSpiltAdjustPoint.append(layer1FlowSpilt[i][0][1])
    print("\033[34m切除的流量在:\033[0m 第" + str(splitBucketSelected + 1) + "个桶的位置上")
    print("选择第\033[32m " + str(splitLayerSelected) + " \033[0m层")
    print("分割第\033[32m " + str(splitBucketSelected) + " \033[0m个实验")

    # 回收桶,统一回收剩余流量,并重新标号
    layer1FlowAllocatedAdjusted = []
    adjustPointCount = 0

    for i in range(len(layer1FlowSpilt)):
        if i == splitBucketSelected:
            # 跳过
            adjustPointCount += 1
        elif i == len(layer1FlowSpilt) - 1:
            layer1FlowAllocatedAdjusted.append(layer1FlowSpilt[splitBucketSelected])
            layer1FlowAllocatedAdjusted.append(layer1FlowSpilt[i])
        else:
            layer1FlowAllocatedAdjusted.append(layer1FlowSpilt[adjustPointCount])
            adjustPointCount += 1

    print("\033[31m调整后的流量标记桶:\033[0m")
    print(markSpiltAdjustPoint)
    spiltBucketNumsOut = markSpiltAdjustPoint[splitBucketSelected + 1] - markSpiltAdjustPoint[splitBucketSelected]
    print("减少并回收流量\033[32m " + str(spiltBucketNumsOut) + " \033[0m个桶")
    print("回收桶的标记位置:\033[32m " + str(adjustMarkPoint) + " <--> " + str(adjustMarkPoint + spiltBucketNumsOut) + " \033[0m")

    splitBucketAdjustedMarkContent = []
    for i in range(len(markSpiltAdjustPoint)):
        if i <= splitBucketSelected:
            splitBucketAdjustedMarkContent.append(markSpiltAdjustPoint[i])
        elif i == len(markSpiltAdjustPoint) - 1:
            splitBucketAdjustedMarkContent.append(markSpiltAdjustPoint[i])
        else:
            splitBucketMarkUpdate = markSpiltAdjustPoint[i + 1] - spiltBucketNumsOut
            splitBucketAdjustedMarkContent.append(splitBucketMarkUpdate)
    # print("\033[34m重新标记划分后的流量标号(暂存未合并):\033[0m")
    # print(splitBucketAdjustedMarkContent)

    splitBucketAdjustedMark = []
    adjustFlowMarkCount = 0
    for i in range(len(markSpiltAdjustPoint) - 1):
        if i <= splitBucketSelected:
            splitBucketAdjustedMark.append(markSpiltAdjustPoint[i])
        else:
            splitBucketMarkUpdate = markSpiltAdjustPoint[i + 1] - spiltBucketNumsOut
            splitBucketAdjustedMark.append(splitBucketMarkUpdate)
    print("\033[34m合并后的流量标号:\033[0m")
    print(splitBucketAdjustedMark)

    # 全部以最暴力的方法来解决
    # 创建跨层实验
    # 下面来新建跨层实验
    # print()
    # print("\033[32m切割后的的流量分配情况:\033[0m")
    # for i in range(len(layer1FlowSpilt)):
    #     print(layer1FlowSpilt[i])
    #
    # print("\033[31m调整流量后的情况:\033[0m")
    # for i in range(len(layer1FlowAllocatedAdjusted)):
    #     print(layer1FlowAllocatedAdjusted[i])

    layer1FlowAdjusted = []
    for i in range(len(layer1FlowAllocatedAdjusted)):
        if i < splitBucketSelected:
            layer1FlowAdjusted.append(layer1FlowAllocatedAdjusted[i])

        elif i == len(layer1FlowAllocatedAdjusted) - 2:
            layer1BucketAdded = []
            # 其余的每个都要加上一个常数
            # print("\033[36m标记的桶位\033[0m")
            # print(splitBucketMarkUpdate)
            for j in range(len(layer1FlowAllocatedAdjusted[i])):
                bucketId = layer1FlowAllocatedAdjusted[i][j][1] - layer1FlowAllocatedAdjusted[i][0][
                    1] + splitBucketMarkUpdate
                layer1BucketAdded.append([layer1FlowAllocatedAdjusted[i][j][0], bucketId])
            layer1FlowAdjusted.append(layer1BucketAdded)

        elif i == len(layer1FlowAllocatedAdjusted) - 1:
            layer1FlowAdjusted[i - 1] = layer1FlowAdjusted[i - 1] + layer1FlowAllocatedAdjusted[i]

        else:
            layer1BucketAdded = []
            # 其余的每个都要加上一个常数
            for j in range(len(layer1FlowAllocatedAdjusted[i])):
                bucketId = layer1FlowAllocatedAdjusted[i][j][1]
                bucketId -= spiltBucketNumsOut
                layer1BucketAdded.append([layer1FlowAllocatedAdjusted[i][j][0], bucketId])
            layer1FlowAdjusted.append(layer1BucketAdded)
    return layer1FlowAdjusted


def flow_add_sdk(splitLayerSelected, splitBucketSelected, splitFlowRate, expMarkPointList, layerWholeAllocated, bucketSum):

    # 下面是对层的流量
    layer1FlowSpilt = []
    flowAdjustRemain = []
    flowAdjustOut = []
    experimentMarkPointList1 = expMarkPointList[splitLayerSelected - 1]
    layer1FlowAllocated = layerWholeAllocated[splitLayerSelected - 1]
    print("层 \033[36m" + str(splitLayerSelected) + "\033[0m 各流量的标记点")
    print(experimentMarkPointList1)
    adjustMarkPoint = experimentMarkPointList1[len(experimentMarkPointList1) - 1] + splitFlowRate * bucketSum
    # print("\033[33m需要切割剩余流量的桶的标记位置\033[0m")
    # print(adjustMarkPoint)
    expAppendMarkList1 = []
    for i in range(len(experimentMarkPointList1)):
        expAppendMarkList1.append(experimentMarkPointList1[i])
    expAppendMarkList1.append(adjustMarkPoint)

    # print("\033[31m重新划分的流量情况标记点\033[0m")
    # print(expAppendMarkList1)

    # 分配按照先划分再实现的逻辑
    # layer1FlowSpilt 是代表流量划分后的结果
    for i in range(len(layer1FlowAllocated)):
        if i == len(layer1FlowAllocated) - 1:
            for j in range(len(layer1FlowAllocated[i])):
                if layer1FlowAllocated[i][j][1] < adjustMarkPoint:
                    flowAdjustRemain.append(layer1FlowAllocated[i][j])
                else:
                    flowAdjustOut.append(layer1FlowAllocated[i][j])
            layer1FlowSpilt.append(flowAdjustRemain)
            layer1FlowSpilt.append(flowAdjustOut)
        else:
            layer1FlowSpilt.append(layer1FlowAllocated[i])


    # 标记结束后的情况
    markSpiltAdjustPoint = []
    print()
    # print("\033[32m调整流量后实验层" + str(splitLayerSelected) + "的分配情况:\033[0m")
    for i in range(len(layer1FlowSpilt)):
        # print(layer1FlowSpilt[i])
        markSpiltAdjustPoint.append(layer1FlowSpilt[i][0][1])

    print("\033[34m分配增加的流量在:\033[0m 第" + str(len(layer1FlowAllocated)) + "个桶的位置上")
    print("\033[31m调整后的流量情况:\033[0m")
    print(markSpiltAdjustPoint)

    print()
    print("选择第\033[32m " + str(splitLayerSelected) + " \033[0m层")
    print("分割第\033[32m " + str(splitBucketSelected) + " \033[0m个实验")

    # 回收桶,统一回收剩余流量,并重新标号
    layer1FlowAllocatedAdjusted = []
    adjustPointCount = 0

    print("\033[31m调整后的流量标记桶:\033[0m")
    print(markSpiltAdjustPoint)
    spiltBucketNumsOut = markSpiltAdjustPoint[len(markSpiltAdjustPoint)-1] - markSpiltAdjustPoint[len(markSpiltAdjustPoint)-2]
    print("减少并回收流量\033[32m " + str(spiltBucketNumsOut) + " \033[0m个桶")
    print("增添的桶的位置:\033[32m " + str(markSpiltAdjustPoint[splitBucketSelected]) + " <--> " +
          str(markSpiltAdjustPoint[splitBucketSelected] + spiltBucketNumsOut) + " \033[0m")

    splitBucketAdjustedMarkContent = []
    # [50, 60, 65, 80, 85]
    # [50, 60, 65, 70, 85]
    for i in range(len(markSpiltAdjustPoint)):
        if i <= splitBucketSelected:
            splitBucketAdjustedMarkContent.append(markSpiltAdjustPoint[i])
        elif i == len(markSpiltAdjustPoint) - 1:
            splitBucketAdjustedMarkContent.append(markSpiltAdjustPoint[i])
        else:
            splitBucketMarkUpdate = markSpiltAdjustPoint[i-1] + spiltBucketNumsOut
            splitBucketAdjustedMarkContent.append(splitBucketMarkUpdate)

    # print("\033[34m重新标记划分后的流量标号(暂存未合并):\033[0m")
    # print(splitBucketAdjustedMarkContent)

    splitBucketAdjustedMark = []
    for i in range(len(splitBucketAdjustedMarkContent)):
        if i != splitBucketSelected :
            splitBucketAdjustedMark.append(splitBucketAdjustedMarkContent[i])
    print("\033[34m合并后的流量标号:\033[0m")
    print(splitBucketAdjustedMark)

    # print()
    # print("\033[32m切割后的的流量分配情况:\033[0m")
    # for i in range(len(layer1FlowSpilt)):
    #     print(layer1FlowSpilt[i])

    # 处理流量调整的情况了
    for i in range(len(layer1FlowSpilt) - 2):
        if i == splitBucketSelected:
            layer1FlowAllocatedAdjusted.append(layer1FlowSpilt[len(layer1FlowSpilt) - 2])
        layer1FlowAllocatedAdjusted.append(layer1FlowSpilt[i])

    layer1FlowAllocatedAdjusted.append(layer1FlowSpilt[len(layer1FlowSpilt) - 1])

    # print("\033[31m流量区块重新划分后的情况:\033[0m")
    # for i in range(len(layer1FlowAllocatedAdjusted)):
    #     print(layer1FlowAllocatedAdjusted[i])

    # correct 这部分正确，下一步就是重新标号和合并
    layer1FlowAdjusted = []

    # 重新编号,
    for i in range(len(layer1FlowAllocatedAdjusted)):
        if i < splitBucketSelected or i == len(layer1FlowAllocatedAdjusted) - 1:
            # 分配流量数据
            layer1FlowAdjusted.append(layer1FlowAllocatedAdjusted[i])
        elif i == splitBucketSelected:
            bucketMarkPoint = expAppendMarkList1[splitBucketSelected]
            layer1BucketAdded = []
            for j in range(len(layer1FlowAllocatedAdjusted[i])):
                bucketId = layer1FlowAllocatedAdjusted[i][j][1] - layer1FlowAllocatedAdjusted[i][0][1] + bucketMarkPoint
                layer1BucketAdded.append([layer1FlowAllocatedAdjusted[i][j][0], bucketId])
            layer1FlowAdjusted[i-1] = layer1FlowAdjusted[i-1] +  layer1BucketAdded
        else:
            layer1BucketAdded = []
            # 其余的每个都要加上一个常数
            for j in range(len(layer1FlowAllocatedAdjusted[i])):
                bucketId = layer1FlowAllocatedAdjusted[i][j][1]
                bucketId += spiltBucketNumsOut
                layer1BucketAdded.append([layer1FlowAllocatedAdjusted[i][j][0], bucketId])
            layer1FlowAdjusted.append(layer1BucketAdded)

    # print("\033[31m最终的桶位\033[0m")
    # for i in range(len(layer1FlowAdjusted)):
    #     print(layer1FlowAdjusted[i])
    return layer1FlowAdjusted


def overlappingExpGen(baseLineBucketNums, overlappingExpRate, baseLineIdFlow, bucketSum):
    overlappingBucketExtract = round(overlappingExpRate * bucketSum)
    lst = []
    for i in range(baseLineBucketNums):
        lst.append(i)
    # print(lst)
    overlappingExtract = random.sample(lst, overlappingBucketExtract)
    print("baseLine中抽取的桶号")
    print(overlappingExtract)  # 取出1个元素

    overlappingExpExtract = []
    baseLineRefreshed = []

    lstRefresh = list(filter(lambda x: x not in overlappingExtract, lst))

    for i in range(len(baseLineIdFlow)):
        if baseLineIdFlow[i][1] in overlappingExtract:
            overlappingExpExtract.append(baseLineIdFlow[i])
        else:
            baseLineRefreshed.append(baseLineIdFlow[i])

    return [overlappingExtract, baseLineRefreshed, lstRefresh]
