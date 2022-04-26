import json
import os

from hoshino import Service, get_bot
from .mc_info import judge, replace_mem, get_status
from .lock_ip import lock_or_unlock

# 首次启动创建文件
current_dir = os.path.join(os.path.dirname(__file__), 'server.json')
if not os.path.exists(current_dir):
    with open(current_dir, 'w', encoding = 'UTF-8') as af:
        json.dump({}, af, indent=4, ensure_ascii=False)

time_set = 2 # 计划任务设置时间的间隔，单位：喵
sv_help = '''
[监控mc ip] 为本群增加监控该ip服务器，不带端口自动默认25565

[不要监控mc ip] 不在为本群监控该ip服务器，不带端口自动默认25565

[mc数据] 查询本群绑定的服务器，绑定多个默认查第一个

[mc数据 ip] 查询该ip服务器，不带端口自动默认25565

(自动推送服务器人数变动) 分群功能，需群管理员发送："开启 mc_reminder"
注：没反应就是你命令输错了
'''.strip()

sv = Service('mc_query', help_=sv_help, enable_on_default=True)
svmc = Service('mc_reminder', enable_on_default=False)

# 帮助界面
@sv.on_fullmatch("mc帮助")
async def help(bot, ev):
    await bot.send(ev, sv_help)

# 查mc数据
@sv.on_rex(r'^mc数据 ?([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})?(:[0-9]{1,5})?$')
async def query_status(bot, ev):
    with open(current_dir, 'r', encoding = 'UTF-8') as f:
        f_data = json.load(f)
    group_id = str(ev.group_id)
    ip = ev['match'].group(1)
    port = ev['match'].group(2)
    if (not ip) and (not port):
        if group_id not in list(f_data.keys()):
            await bot.finish(ev, '该群还未绑定任何IP呢')
        if not list(f_data[group_id].keys()):
            await bot.finish(ev, '该群还未绑定任何IP呢')
        ip = list(f_data[group_id].keys())[0]
    elif ip and (not port):
        ip += ':25565'
    else:
        ip += port
    msg = await get_status(ip)
    await bot.send(ev, msg)

# 监控数据和取消监控
@sv.on_rex(r'^(不要)?监控mc ?([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})(:[0-9]{1,5})?$')
async def add_server(bot, ev):
    group_id = str(ev.group_id)
    is_lock = ev['match'].group(1)
    ip = ev['match'].group(2)
    port = ev['match'].group(3)
    if port:
        ip += port
    else:
        ip += ':25565'
    is_lock = False if is_lock else True
    msg = await lock_or_unlock(is_lock, ip, group_id)
    await bot.send(ev, msg)

# 上线人员提醒
@svmc.scheduled_job('cron', minute=f'*/{time_set}')
async def mc_poller():
    bot = get_bot()
    with open(current_dir, 'r', encoding = 'UTF-8') as f:
        f_data = json.load(f)
    for group_id in list(f_data.keys()):
        for ip in list(f_data[group_id].keys()):
            try:
                flag, del_member, add_member, online_list = await judge(ip, f_data[group_id][ip])
            except Exception as e:
                svmc.logger.info(f'检测到错误！可能是服务器未开启或已关闭，具体原因：{e}')
                return
            add_num = len(add_member)
            del_num = len(del_member)
            if flag == 'change':
                svmc.logger.info(f'检测到MC服务器{ip}内玩家变化')
                msg = f'检测到MC服务器\n{ip}\n近 {time_set} 分钟内'
                if add_num != 0:
                    msg += f'\n增加了 {add_num} 人:\n'
                    msg += ' | '.join(add_member)
                if del_num != 0:
                    msg += f'\n减少了 {del_num} 人:\n'
                    msg += ' | '.join(del_member)
                await bot.send_group_msg(group_id=group_id, message=msg)
                await replace_mem(group_id, ip, online_list)
            else:
                svmc.logger.info(f'MC服务器{ip}内人数未变化')