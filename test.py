# encoding:utf-8
import split

userId = 1000
layerId = 1
bucketSum = 100
MD5 = split.gen_md5(str(userId), layerId)
print(MD5)

bucketNum = split.gen_spilt(str(userId), layerId, bucketSum)
print(bucketNum)