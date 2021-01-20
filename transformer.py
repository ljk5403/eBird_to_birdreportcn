#/usr/bin/env python3
'''
此程序用于将ebird的观察数据转换为中国观鸟记录中心可以接受的数据格式。
参考：https://mp.weixin.qq.com/s/i17984F6CRl2v_g7fcmu5g
Version 0.1
by ljk5403
'''

#import os #用于读写文件
import pandas as pd
import re  # 正则表达式

targetFile = 'observations.csv'
referance = 'referance.xls'

referanceDf = pd.read_excel(referance)


def transformer(filename):
    df = pd.read_csv(filename)
    #截取前两列，并重命名使其符合格式要求
    df = df[[df.columns[0], df.columns[1]]]
    # 或：df = df.filter([df.columns[0], df.columns[1]], axis=1)
    df = df.rename(columns={df.columns[0]: '中文名', df.columns[1]: '数量'})
    #完善物种名 TODO:分别通过拉丁名和物种名搜索，无法检出的抛出异常
    successSign = 1
    for i in range(0, len(df)):
        latinName = re.findall(re.compile(
            r'[(](.*?)[)]', re.S), df.iloc[i]['中文名'])
        chineseName = referanceDf[referanceDf['拉丁名'].isin(latinName)]
        if chineseName.empty == False:
            chineseName = chineseName['鸟种']
            chineseName = str(chineseName.values[0])
            df.loc[i, '中文名'] = chineseName
        else:
            print("无法处理的鸟种名，请手动修复：", df.iloc[i]['中文名'])
            successSign = 0
    if successSign == 1:
        df.to_excel("result.xls", index=False)
    else:
        df.to_excel("result_需要手动修复.xls", index=False)


transformer(targetFile)