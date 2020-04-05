# 拼音输入法
计81 严韫洲 2018011299

2019-2020学年人工智能导论课第一次大作业

## 简介
这是一个利用python实现的基于隐马尔可夫模型的拼音输入法。

这一输入法是基于字的三元模型，除此之外我们还实现了添加了在现有语料基础上额外添加语料的接口，以及接收测试集格式文件输出准确率的方便调试的接口。此外我们在语料选择、处理和模型对比上也有特别的考虑。

github地址：[https://github.com/Billyyanyz/Pinyin](https://github.com/Billyyanyz/Pinyin)

## 目录结构
* `pinyin.py`：主文件，直接运行即可得到结果
* `train.py`：训练模型的文件，需要带参数运行
* `src/`：源代码和语料资源文件夹
	* `src/original_material/`：存放原始语料的文件夹
	* `src/processed_materal/`：存放处理后语料的文件夹，其中文件名与原始语料一一对应
	* `src/stats/`：存放统计数据的文件夹
	* `src/word_range.py`：设置汉字范围
	* `src/preprocessor.py`：预处理原始语料
	* `src/analyzer.py`：分析处理后语料并统计词频
	* `src/num_to_freq_translater.py`：将词频翻译为转移概率
	* `src/HMM_pinyin.py`：实现的HMM模型
	* `src/Const.py`：存放过程中需要用到的常数
	* `src/tester.py`：利用测试集测试模型准确率
* `data/`：测试数据文件夹（其中input.txt，output.txt如题目要求，test.txt按照测试集的格式即可调用tester.py进行测试）

##依赖
本项目依赖python库`pypinyin`，你可以执行下列指令来安装它们：
```
$ pip install pypinyin
```

## 使用
执行下列指令即可运行拼音输入法程序得到结果：
```
$ python -m pinyin
```

## 用例

bei jing shi yi ge mei li de cheng shi

北京是一个美丽的城市

gei a yi dao yi bei ka bu qi nuo

给阿姨倒一杯卡布奇诺

shi san jie quan guo ren da yi ci hui yi

十三届全国人大一次会议

chun jiang chao shui lian hai ping

春江潮水连海平

tan tan jian jian neng neng fou fou ding ding lv

碳碳键键能能否否定定律

## 注意事项

输入的拼音要求为一般标准注音，因此若需输出“略”，应输入`lve`而非`lue`，“虐”亦然。

由于模型训练耗时较长，我们没有在主程序中设置统一的模型训练接口。
不过如果确有必要训练模型，可以运行`train.py`进行不同类型的训练，具体操作方式详见实验报告。