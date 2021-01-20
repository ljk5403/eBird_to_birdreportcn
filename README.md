# eBird to birdreportcn
本项目用于将ebird的观察数据转换为中国观鸟记录中心可以接受的数据格式。

Version 0.1

## 使用
参考[ 如何将【eBird】的数据同步至【中国观鸟记录中心】](https://mp.weixin.qq.com/s/i17984F6CRl2v_g7fcmu5g)。

步骤：

1. 安装 python3，并安装依赖：`pip3 install pandas xlrd xlwt`
2. 下载本项目到 `eBird_to_birdreportcn` 文件夹下
3. 从 eBird 下载一个checklist，将会得到一个名为 `xxyyzzww_observations.csv` 的文件，将其重命名为 `observations.csv`，并将其放到 `eBird_to_birdreportcn` 文件夹下
4. 运行 `python3 transformer.py`
5. 得到结果为 `result.xls` 或 `result_需要手动修复.xls`，后者需要手动修复一些没能转换到数据。
6. 提交记录到中国中国观鸟记录中心


## 注意

`referance.xls`: 来自“下载鸟种库”，如出现异常可以从中国观鸟记录中心重新下载，注意要重命名为 `referance.xls` 。


## TODO

[] 移除依赖 xlwt，换用 openpyxl  
[] 同时处理多份文件  
[] 编译为便携版本，方便小白使用