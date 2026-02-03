# /usr/bin/env python3
'''
此程序用于将ebird的观察数据转换为中国观鸟记录中心可以接受的数据格式。
参考：https://mp.weixin.qq.com/s/i17984F6CRl2v_g7fcmu5g
Version 0.4
by ljk5403
'''

import os  # 用于读写文件
import sys
import pandas as pd
import re  # 正则表达式
import time

#referance = 'referance.xls' # before 2024
referance = 'referance.xlsx'
noteName = 'note.csv'

referanceDf = pd.read_excel(referance)
noteDf = pd.read_csv(noteName)

def transformer(filename):
    df = pd.read_csv(filename)
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))) # 打印当前时间
    print("处理文件：" + filename)
    # 截取前两列，并重命名使其符合格式要求
    location = df.iloc[0, 2];
    date = df.iloc[0, 4];
    startTime = df.iloc[0, 5];
    duration = df.iloc[0, 6];
    startTime, endTime = getTime(startTime, duration)
    df = df[[df.columns[0], df.columns[1]]]
    # 或：df = df.filter([df.columns[0], df.columns[1]], axis=1)
    df = df.rename(columns={df.columns[0]: '中文名', df.columns[1]: '数量'})
    # 完善物种名
    successSign = 1
    for i in range(0, len(df)):
        # 根据英文括号内的拉丁名（如果开启了sci name）检索
        #Old version: pattern1 = re.compile(r'[(](.*?)[)]')
        #New version: extract the first two words from the last parenthesis
        rawName = df.iloc[i]['中文名']
        pattern1 = re.compile(r'\(([^)]+)\)') #This pattern matches all text inside parentheses
        matches = re.findall(pattern1, rawName)
        if matches:
            latinName = ' '.join(matches[-1].split()[:2]) # select the last match and split and get first two words
            chineseName = referanceDf[referanceDf['拉丁名'].isin([latinName])]
        else:
            latinName = None
            chineseName = referanceDf.iloc[0:0]   # put a empty DataFrame here for the next `if`

        if chineseName.empty == False:
            chineseName = chineseName['中文名']
            chineseName = str(chineseName.values[0])
            df.loc[i, '中文名'] = chineseName
        else:
            # 提取括号前的中文名，根据中文名检索
            pattern3 = re.compile(r'(.*?)(?:\s*\(|$)')
            eBirdChineseName = re.findall(pattern3, rawName)
            eBirdChineseName = eBirdChineseName[:1]
            # eBird 提供了亚种附加词，根据中文括号特征删除亚种附加词
            eBirdChineseNameSimplified = re.findall(r'(.*?)[（]', str(eBirdChineseName[0]))
            if eBirdChineseNameSimplified:
                eBirdChineseName = eBirdChineseNameSimplified
            chineseName = referanceDf[referanceDf['中文名'].isin(eBirdChineseName)]
            if chineseName.empty == False:
                chineseName = chineseName['中文名']
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
                    print("无法处理的中文名，请手动修复：", rawName)
                    successSign = 0
    if successSign == 1:
        outputName = filename[0:-17] + "_importable.xlsx"
    else:
        outputName = filename[0:-17] + "_importable_需要手动修复.xlsx"
    df.to_excel(outputName, index=False)
    print("输出文件到：" + outputName)
    return (outputName, location, date+" "+startTime+" ~ "+endTime)

def getTime(startTime:str, duration:str):
    colonIndex = startTime.find(':')
    startHour = int(re.search(r'\d+:*',startTime).group(0)[0:-1])
    startMinute = int(startTime[colonIndex+1:colonIndex+3])
    if ('下午' in startTime) or ('PM' in startTime):
        startHour+=12
    endHour = startHour
    endMinute = startMinute
    if isinstance(duration,str):
        if ',' in duration:
            endHour+=int(re.match(r'^\d*', duration).group(0))
            duration = duration[duration.find(',')+2:]
        endMinute+=int(re.match(r'^\d*', duration).group(0))
    if endMinute >= 60:
        endMinute -=60
        endHour +=1
    if startMinute < 10:
        startTime = str(startHour)+":0"+str(startMinute)
    else:
        startTime = str(startHour)+":"+str(startMinute)

    if endMinute < 10:
        endTime = str(endHour)+":0"+str(endMinute)
    else:
        endTime = str(endHour)+":"+str(endMinute)
    print(startTime, endTime)
    return (startTime, endTime)

if __name__ == "__main__":
    # --- 如果用户提供了文件名参数 ---
    if len(sys.argv) > 1:
        for targetFile in sys.argv[1:]:
            if os.path.isfile(targetFile):
                transformer(targetFile)
            else:
                print(f"Error: File '{targetFile}' not found in current directory.")
    else:
        # --- 否则，批量处理所有当前文件夹下的*observations.csv数据 ---
        for targetFile in os.listdir():
            pattern2 = re.compile(r'(.*?)observations[.]csv$')
            if pattern2.match(targetFile) is not None:
                transformer(targetFile)

''' Old main function
if __name__ == "__main__":
    pattern2 = re.compile(r'(.*?)observations[.]csv$')
    for targetFile in os.listdir():
        if pattern2.match(targetFile) is not None:
            transformer(targetFile)
'''
