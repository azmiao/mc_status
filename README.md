## mc_status

一个自用的hoshinobot的 mc数据查询监控 超简易插件

因为没有啥需求而且代码非常非常简单，应该不会考虑更新

本插件仅供学习研究使用，插件免费，请勿用于违法商业用途，一切后果自己承担

## 项目地址：

https://github.com/azmiao/mc_status

## 功能

```
[监控mc ip] 为本群增加监控该ip服务器，不带端口自动默认25565

[不要监控mc ip] 不在为本群监控该ip服务器，不带端口自动默认25565

[mc数据] 查询本群绑定的服务器，绑定多个默认查第一个

[mc数据 ip] 查询该ip服务器，不带端口自动默认25565

(自动推送服务器人数变动) 该功能无命令
```

## 简单食用教程：

1. git clone本插件：

    在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目
    ```
    git clone https://github.com/azmiao/mc_status
    ```

2. 安装依赖：下不了的自己换源，不多说了
    ```
    pip install mcstatus
    ```

3. 在 HoshinoBot\hoshino\config\ `__bot__.py` 文件的 MODULES_ON 加入 'mc_status'

    然后重启 HoshinoBot

4. 监控人员上线提醒默认关闭，需要开启的话请在群里发送'开启 mc_reminder'

## 如果无法查询到，可能是你端口和配置的问题

可以看我的这篇文章的补充部分解决

https://www.594594.xyz/2021/10/24/mc_status_for_hoshino/