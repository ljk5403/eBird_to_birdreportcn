# eBird to birdreportcn

本项目用于将ebird的观察数据转换为中国观鸟记录中心可以接受的数据格式。

Version 0.4.1

## 网页版应用

网页版应用可直接使用，并已支持多文件！  
详情见<a href="https://xebird.lijiankun.com/eBird_to_birdreportcn/" target="_blank">网页版应用</a>。

网页版应用的源代码在 `webapp.py`，有个性化修改，不保证移植可用性。

## 使用
参考[ 如何将【eBird】的数据同步至【中国观鸟记录中心】](https://mp.weixin.qq.com/s/i17984F6CRl2v_g7fcmu5g)。

步骤：

1. 安装 python3，并安装依赖：`pip3 install pandas openpyxl`
   - 老版本使用 `xlrd xlwt` ，新版 `pandas` 不再支持。
2. 下载整个项目（右上角"code"选择喜欢的下载方式，萌新可选 "Download ZIP" 之后解压），也可从 release 中下载，解压得到 `eBird_to_birdreportcn` 文件夹
3. 从 eBird 下载一个或多个checklist，将会得到一个名为 `xxyyzzww_observations.csv` 的文件，将其放到 `eBird_to_birdreportcn` 文件夹下
4. 在 `eBird_to_birdreportcn` 文件夹下运行 `python3 transformer.py`
5. 得到结果为 `xxyyzzww_importable.xlsx` 或 `xxyyzzww_importable_需要手动修复.xlsx`，后者需要手动修复一些没能转换的数据
6. 提交 `xlsx` 格式的记录到[中国观鸟记录中心](http://www.birdrecord.cn/)

> 对于需要手动修复的情况，可以编辑 `note.csv` 来添加明确的对应法则。 `note.csv` 中的对应法则将在无法直接使用中文名和无法使用拉丁名搜索的时候生效。

## 鸟种名录

`referance.xlsx`: 在中国观鸟记录中心中，任意开启一个记录，选择任意一个地点后点击“下一步，导入鸟种”，再点击“下载鸟种库”（如图所示），如出现异常可以从中国观鸟记录中心重新下载，注意要重命名为 `referance.xlsx` 。

![](how_to_get_referance_xls.png)



`note.csv` : 特别标注出来的无法通过中文名和 `referance.xlsx` 来转换的鸟种名。包含两列：eBirdName 和 birdreportcnName，分别对应两边可用的名字。


## TODO

- [x] 同时处理多份文件  
- [x] 在网页中显示note.csv
- [ ] 调整网页布局，分为两列
- [x] 移除依赖 xlwt，换用 openpyxl  

## Changelog

- Version 0.4.1: Update referance.xls to 郑四
- Version 0.4: Add note.csv for outstanding differences
- Version 0.3: Improve name conversion
- Version 0.2: Multiple files process
- Version 0.1: Basic function
