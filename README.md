## mc_status

一个自用的hoshinobot的 mc数据查询监控 超简易插件

因为没有啥需求而且代码非常非常简单，应该不会考虑更新

本插件仅供学习研究使用，插件免费，请勿用于违法商业用途，一切后果自己承担

## 项目地址：

https://github.com/azmiao/mc_status

## 功能

```
命令如下：
[如何加入mc服务器] 简单步骤

[mc数据] 查询当前服务器人数和延迟
```

## 简单食用教程：

1. 下载或git clone本插件：

    在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目
    ```
    git clone https://github.com/azmiao/mc_status
    ```

2. 安装依赖：下不了的自己换源，不多说了
    ```
    pip install mcstatus
    ```

3. 在 `mc_info.py` 最上面填写你的服务器ip和端口

4. 在 HoshinoBot\hoshino\config\ `__bot__.py` 文件的 MODULES_ON 加入 'mc_status'

    然后重启 HoshinoBot

5. 监控人员上线提醒默认关闭，需要开启的话请在群里发送'开启 mc_reminder'