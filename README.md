# eBird to birdreportcn

本项目用于将ebird的观察数据转换为中国观鸟记录中心可以接受的数据格式。

Version 0.4

## 使用
参考[ 如何将【eBird】的数据同步至【中国观鸟记录中心】](https://mp.weixin.qq.com/s/i17984F6CRl2v_g7fcmu5g)。

步骤：

1. 安装 python3，并安装依赖：`pip3 install pandas xlrd xlwt`
2. 下载本项目到 `eBird_to_birdreportcn` 文件夹下
3. 从 eBird 下载一个checklist，将会得到一个名为 `xxyyzzww_observations.csv` 的文件，将其放到 `eBird_to_birdreportcn` 文件夹下
4. 运行 `python3 transformer.py`
5. 得到结果为 `xxyyzzww_importable.xls` 或 `xxyyzzww_importable_需要手动修复.xls`，后者需要手动修复一些没能转换的数据
6. 提交 `xls` 格式的记录到中国中国观鸟记录中心

> 对于需要手动修复的情况，可以编辑 `note.csv` 来添加明确的对应法则。 `note.csv` 中的对应法则将在无法直接使用中文名和无法使用拉丁名搜索的时候生效。

## 注意

`referance.xls`: 来自“下载鸟种库”，如出现异常可以从中国观鸟记录中心重新下载，注意要重命名为 `referance.xls` 。

`note.csv` : 特别标注出来的无法通过中文名和 `referance.xls` 来转换的鸟种名。包含两列：eBirdName 和 birdreportcnName，分别对应两边可用的名字。


## TODO

- [ ] 移除依赖 xlwt，换用 openpyxl  
- [x] 同时处理多份文件  
- [ ] 编译为便携版本，方便小白使用

## Changelog
- Version 0.4: Add note.csv for outstanding differences
- Version 0.3: Improve name conversion
- Version 0.2: Multiple files process
- Version 0.1: Basic function
