---
title: Strata跑Qwen3.8-Flash-Next
description: null
slug: strata跑qwen3-8-flash
date: 2026-10-06
tags:
  - LocalLLM
---

最近Strata这个推理引擎比较火热。
主要是用这个引擎跑Qwen3.8-Flash-Next模型，在显存只有12GB的时候能跑出50+tps；
在一些大显存的情况下，能够达到100-200tps。
要知道，Qwen3.8-Flash-Next是一个125B的MoE模型，用llama.cpp直接跑可能只在5-20tps(普通消费显卡)。

> 网上有很多Strata的帖子，就只说速度快，牛X，截几张图就啥也没了。
> 今天我也下载了，试着跑一下。把每个步骤记录下来，让感兴趣的朋友先看下，再决定是否跑。

> #### 我的电脑配置：
> |硬件|型号|
> |---|---|
> |CPU|intel i9-10940X|
> |内存|64GB DDR4|
> |显卡|5060Ti 16GB*2| 
> |Windows 11|

### 网站(所有的信息都在这，有中文的README)
[Github/Niko1221/Strata](https://github.com/Niko1221/Strata)
找到最新的release下载就可以了（13MB）。

> 建议硬盘可用空间至少100GB

解压文件后运行`START-HERE.bat`

![1.png](https://imgbed.dirkyxf.ccwu.cc/file/ImageBed/blog/1791029002327.png)
* 检查硬件
  * 如果显卡有多张，也会让你选择
* 模型参数
  * 选择你要运行哪个模型
  * 选择你要运行的量化版本
  * 选择上下文大小
  * KV cache的量化大小
  * 是否要有识图能力
  * 是否要加载速度投影模型
* 依赖运行的Python包

![2.png](https://imgbed.dirkyxf.ccwu.cc/file/ImageBed/blog/1791029002106.png)
* 推理引擎
  * llama.cpp
  * Strata engine
  * NVIDIA CUDA相关
* 模型文件
  * 如果自己下载好了，可以直接放在对应路径下吗
  * 如果没有文件，代码会自自己下载（用的还是huggingface的代理，不错。不过速度有点慢。我从modelscope上下载好了放到这个文件夹里面的。）

![3.png](https://imgbed.dirkyxf.ccwu.cc/file/ImageBed/blog/1791291425490.png)

开始准备MTP模型，要等待一直下载完。

![4.png](https://imgbed.dirkyxf.ccwu.cc/file/ImageBed/blog/1791291441606.png)

写入Strata启动脚本。
比如：KV cache, GPU张量并行，模型分层等。

![5.png](https://imgbed.dirkyxf.ccwu.cc/file/ImageBed/blog/1791291449612.png)

开始启动服务，加载模型。需要耐心等待。
等启动好后会提示浏览器打开http://127.0.0.1:8080

打开网页后可以chat对话，monitor监控和查看推理硬件及软件信息。

![6.png](https://imgbed.dirkyxf.ccwu.cc/file/ImageBed/blog/1791291450458.png)
![7.png](https://imgbed.dirkyxf.ccwu.cc/file/ImageBed/blog/1791291454931.png)

以上两张图是我两张5060Ti的GPU占用情况，基本已经占据到14+或15+GB显存了。（这个是我之前用llama.cpp无法分配成功的。）

![10.png](https://imgbed.dirkyxf.ccwu.cc/file/ImageBed/blog/1791297368592.png)

上图是我让做了一个html游戏，可以看到输出速度可以达到75+tps, 在运行期间甚至可以达到100+的峰值。

在此真的感叹开源的力量！！！

![9.png](https://imgbed.dirkyxf.ccwu.cc/file/ImageBed/blog/1791291972611.png)

要关闭服务很简单，把命令行窗口关闭即可。
下次启动的时候再运行`START-HERE.bat`即可。
不用再进行配置了，直接启动服务。

> 提示：如果之前浏览器运行过llama.cpp的网页，需要清理浏览数据后再运行，否则打开127.0.0.1:8080后显示的还是llama.cpp的网页内容和设置。