#  eBird ⇒ birdreportcn

## 将ebird的观察数据转换为中国观鸟记录中心可以接受的数据格式

<center><form method=post enctype=multipart/form-data>
  <input type=file multiple name=file>
  <input type=submit value=Upload>
  <p></p>
	{% for key,value in downloadLink.items() %}
		<p><span>{{ key }} 转换为 </span><a href="{{ value[1] }}" download><span>{{ value[0][0] }}</span></a>，地点：{{ value[0][1] }} 时间：{{ value[0][2] }} </p>
	{% else %}
		<p>请选择csv文件（支持多文件上传！）</p>
	{% endfor %}
</form></center>




使用方法：

1. 从 <a href="https://ebird.org/mychecklists" target="_blank">eBird - 我的记录</a> 下载一个或多个checklist，得到若干名为 <code>xxyyzzww_observations.csv</code> 的文件。

2. 选中一个或多个csv文件上传，注意不要改变文件名字！

3. 转换结果为 <code>xxyyzzww_importable.xls</code> 或 <code>xxyyzzww_importable_需要手动修复.xls</code>，后者需要手动修复一些没能转换的数据。结果将自动下载。

   > Chrome 浏览器可能会直接打开xls文件，请留意地址栏，如结尾为`.xls`请直接右键保存

4. 进入 <a href="http://www.birdrecord.cn/member/index.html" target="_blank">中国观鸟记录中心</a>，点击“创建观鸟记录 > 定点记”，填写观察点，选择时间，选择“下一步，导入鸟种”，再选择“下一步，上传鸟种数据”，“下一步，预览完成”，即可。


源代码及更多信息请参考 Github 上的<a href="https://github.com/ljk5403/eBird_to_birdreportcn" target="_blank">项目网站</a>。

[^_^]: Generated by Typora with theme Gothic