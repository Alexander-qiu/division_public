# encoding:utf-8
# this part is difined to create division nums

import hashlib
# generate md5 nums


def gen_md5(userId, layerId):
    layerIdStr = str(layerId)
    baseStr = ["4paradigm", "qiuruizhi", "Alexander", "polaris"]
    baseStrSelect = baseStr[layerId % len(baseStr)]
    userIdPlusLayer = userId + baseStrSelect + layerIdStr

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


