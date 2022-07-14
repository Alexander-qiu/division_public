# encoding:utf-8
import random
import math

import split
baseLineFlowRate = 0.5
bucketSum = 100
overlappingExpRate = 0.05
baseLineBucketNunms = math.ceil(baseLineFlowRate * bucketSum)
overlappingBucketExtract = round(overlappingExpRate * bucketSum)

lst = range(baseLineBucketNunms)
print(lst)
overlappingExpSelected = random.sample(lst, overlappingBucketExtract)
print(overlappingExpSelected)  # 取出1个元素


