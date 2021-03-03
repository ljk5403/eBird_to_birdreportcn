# /usr/bin/env python3
'''
此程序用于将ebird的观察数据转换为中国观鸟记录中心可以接受的数据格式。
参考：https://mp.weixin.qq.com/s/i17984F6CRl2v_g7fcmu5g
Version 0.4
by ljk5403
'''

import os  # 用于读写文件
import pandas as pd
import re  # 正则表达式

referance = 'referance.xls'
noteName = 'note.csv'

referanceDf = pd.read_excel(referance)
noteDf = pd.read_csv(noteName)

def transformer(filename):
    df = pd.read_csv(filename)
    print("处理文件：" + filename)
    # 截取前两列，并重命名使其符合格式要求
    df = df[[df.columns[0], df.columns[1]]]
    # 或：df = df.filter([df.columns[0], df.columns[1]], axis=1)
    df = df.rename(columns={df.columns[0]: '中文名', df.columns[1]: '数量'})
    # 完善物种名
    successSign = 1
    for i in range(0, len(df)):
        # 根据拉丁名检索
        pattern1 = re.compile(r'[(](.*?)[)]')
        latinName = re.findall(pattern1, df.iloc[i]['中文名'])
        chineseName = referanceDf[referanceDf['拉丁名'].isin(latinName)]
        if chineseName.empty == False:
            chineseName = chineseName['鸟种']
            chineseName = str(chineseName.values[0])
            df.loc[i, '中文名'] = chineseName
        else:
            # 根据中文名检索
            pattern3 = re.compile(r'(.*?) [(]')
            eBirdChineseName = re.findall(pattern3, df.iloc[i]['中文名'])
            # eBird 提供了亚种附加词，根据括号特征删除亚种附加词
            eBirdChineseNameSimplified = re.findall(r'(.*?)[（]', str(eBirdChineseName[0]))
            if eBirdChineseNameSimplified:
                eBirdChineseName = eBirdChineseNameSimplified
            chineseName = referanceDf[referanceDf['鸟种'].isin(eBirdChineseName)]
            if chineseName.empty == False:
                chineseName = chineseName['鸟种']
                chineseName = str(chineseName.values[0])
                df.loc[i, '中文名'] = chineseName
            else:
                # 特殊名字根据对照表(note.csv)直接检索
                chineseName = noteDf[noteDf['eBirdName'].isin(eBirdChineseName)]
                if chineseName.empty == False:
                    chineseName = chineseName['birdreportcnName']
                    chineseName = str(chineseName.values[0])
                    df.loc[i, '中文名'] = chineseName
                else:
                    print("无法处理的鸟种名，请手动修复：", df.iloc[i]['中文名'])
                    successSign = 0
    if successSign == 1:
        outputName = filename[0:-17] + "_importable.xls"
    else:
        outputName = filename[0:-17] + "_importable_需要手动修复.xls"

    df.to_excel(outputName, index=False)
    print("输出文件到：" + outputName)
    return outputName


pattern2 = re.compile(r'(.*?)observations[.]csv')
for targetFile in os.listdir():
    if pattern2.match(targetFile) is not None:
        transformer(targetFile)