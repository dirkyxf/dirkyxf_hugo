---
title: "创建甲骨文虚拟主机后的设置"
description: "创建甲骨文虚拟主机后的设置"
slug: setup-after-create-an-oracle-vps
date: 2026-11-14
tags:
  - VPS
  - Oracle
draft: false
---

# 新甲骨文主机设置记录
## Cloud Shell的连接
1. 登录Cloud.oracel.com之后，右上角工具栏，找到Cloud Shell
![pasted-1793351267319.png](https://img.dirkyxf.de/file/ImageBed/blog/1794662980425.png)
2. 下方会出现窗口，等待一会启动会出现如下界面：
![pasted-1793351422106.png](https://img.dirkyxf.de/file/ImageBed/blog/1794662981781.png)
   右上角点菜单，下载/上载主要作用是处理ssh的key。
> 新建主机后会有一个私钥，格式为`ssk-key-yyyy-mm-dd.key`
3. 点`上载`将key上传至该Cloud terminal小主机。
4. 然后直接运行如下命令修改key的权限：
`chmod 600 sssk-key-yyyy-mm-dd.key`
5. 接着用如下指令连接到新建的主机。
`ssh -i ssk-key-yyyy-mm-dd.key ubuntu@你的公网IP地址`
### 安装Tailscale
安装Tailscale是为了方便后期维护，和网络互通。
1. 使用如下命令进行安装：
`curl -fsSL https://tailscale.com/install.sh | sh`
2. 等一会儿安装好后会有提示，然后运行：
`sudo tailscale up`
  会生成一窜链接，点链接直接跳转至浏览器进行账号验证，跟着操作即可。

## 端口放行
由于甲骨文主机Ubuntu中端口默认禁用，需要手动打开。
1. 先安装`ufw`来管理：
`sudo apt install ufw`
2. 放行ssh
`sudo ufw allow ssh`
3. 放行80
`sudo ufw allow 80/tcp`
4. 放行443
`sudo ufw allow 443/tcp`
5. 启用ufw
`sudo ufw enable`
## VPN的设置
### 安装3X-UI
1. 在命令行窗口执行如下：
`bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)`
2. 安装过程中会生成随机的用户名、密码和访问路径，记得记下来。
3. 记得把这个端口放行
`sudo ufw allow 21020/tcp`
4. 安装完成后，以`sudo x-ui`来运行设置
![pasted-1793359792137.png](https://img.dirkyxf.de/file/ImageBed/blog/1794662980285.png)
### 配置证书
输入`20` 进行SSL设置
![pasted-1793360210008.png](https://img.dirkyxf.de/file/ImageBed/blog/1794662976130.png)
输入`6`进行无域名自动续期设置
一路回车，都是绿色即可。
### 入站规则
登录到3X-UI到管理网页，添加入站
![pasted-1793364300777.png](https://img.dirkyxf.de/file/ImageBed/blog/1794662974025.png)
选择Vless
![pasted-1793365783675.png](https://img.dirkyxf.de/file/ImageBed/blog/1794662980813.png)
![pasted-1793365809555.png](https://img.dirkyxf.de/file/ImageBed/blog/1794662986513.png)
![pasted-1793365834124.png](https://img.dirkyxf.de/file/ImageBed/blog/1794662980646.png)
![pasted-1793365882007.png](https://img.dirkyxf.de/file/ImageBed/blog/1794662982851.png)
![pasted-1793365901977.png](https://img.dirkyxf.de/file/ImageBed/blog/1794662982487.png)

### 建立客户端
客户端就是基于入站规则运行到所有终端，比如手机、电脑等
![pasted-1793365995138.png](https://img.dirkyxf.de/file/ImageBed/blog/1794662981522.png)
把刚才的入站规则关联至这个客户端
![pasted-1793366162372.png](https://img.dirkyxf.de/file/ImageBed/blog/1794662986593.png)
![pasted-1793366204665.png](https://img.dirkyxf.de/file/ImageBed/blog/1794662985386.png)
二维码和感叹号里面是手机、电脑等需要连接的信息：
![pasted-1793366300479.png](https://img.dirkyxf.de/file/ImageBed/blog/1794662985337.png)

### 客户端安装和配置
mac os客户端用的是V2rayN
安卓手机端用的是v2rayNG