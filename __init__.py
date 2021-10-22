import hoshino
from hoshino import Service, R, priv
from .mc_info import *

time_set = 2 # 计划任务设置时间的间隔，单位：喵
sv_help = '''[如何加入mc服务器] 简单步骤

[mc数据] 查询当前服务器人数和延迟'''.strip()

sv = Service('mc_query', help_=sv_help, enable_on_default=True)
svmc = Service('mc_reminder', enable_on_default=False)

# 帮助界面
@sv.on_fullmatch("mc帮助")
async def help(bot, ev):
    await bot.send(ev, sv_help)

# mc加入教程
@sv.on_fullmatch('如何加入mc服务器')
async def join_mc(bot, ev):
    msg = f'''1. 安装java 64位版本
2. 下载HMCL最新测试版
3. 打开HMCL安装mc 版本x.xx.x
4. 安装上暮色森林mod
5. 进游戏添加服务器：xxx.xxx.xx.xx
6. 进入服务器即可'''
    await bot.send(ev, msg)

# 查mc数据
@sv.on_fullmatch('mc数据')
async def query_status(bot, ev):
    msg = get_status()
    await bot.send(ev, msg)

# 上线人员提醒
@svmc.scheduled_job('cron', minute=f'*/{time_set}')
async def mc_poller():
    try:
        flag, del_member, add_member, online_list = judge()
    except Exception as e:
        svmc.logger.info(f'检测到错误！可能是服务器未开启或已关闭，具体原因：{e}')
        return
    add_num = len(add_member)
    del_num = len(del_member)
    if flag == 'change':
        svmc.logger.info('检测到mc服务器内玩家变化')
        msg = f'检测到mc服务器近 {time_set} 分钟内：'
        if add_num != 0:
            msg = msg + f'\n增加了 {add_num} 人:\n'
            msg = msg + '{0}'.format(" | ".join(add_member))
        if del_num != 0:
            msg = msg + f'\n减少了 {del_num} 人:\n'
            msg = msg + '{0}'.format(" | ".join(del_member))
        await svmc.broadcast(msg, 'mc_reminder', 0.2)
        replace_mem(online_list)
    else:
        svmc.logger.info('mc服务器内人数未变化')