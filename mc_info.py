import os
import json
from mcstatus import JavaServer, BedrockServer # 第一个java版，第二个基岩版(能查的东西太少了，就不写了)

current_dir = os.path.join(os.path.dirname(__file__), 'server.json')

# 查服务器信息
async def get_status(ip):
    server = JavaServer.lookup(ip)
    try:
        query = server.query()
        latency = server.ping()
        player = ' | '.join(query.players.names).encode("iso-8859-1").decode("utf-8", 'ignore')
        msg = f'该服务器内目前有 {len(query.players.names)} 位玩家:\n {player}\n服务器延迟为 {round(latency,3)} ms'
    except Exception as e:
        msg = f'查询失败！错误明细：{e}'
    return msg

# 判断是否有人员变动
async def judge(ip, m_list):
    server = JavaServer.lookup(ip)
    query = server.query()
    online_list = query.players.names
    del_member = []
    add_member = []
    for n in range(len(m_list)):
        del_member.append(m_list[n])
    for m in range(len(online_list)):
        add_member.append(online_list[m])
    for member in online_list:
        if member in del_member:
            del_member.remove(member)
    for member in m_list:
        if member in add_member:
            add_member.remove(member)
    if len(add_member)== 0 and len(del_member) == 0:
        return 'nothing', del_member, add_member, online_list
    else:
        return 'change', del_member, add_member, online_list

# 替换人员变动
async def replace_mem(group_id, ip, online_list):
    with open(current_dir, 'r', encoding = 'UTF-8') as f:
        f_data = json.load(f)
    f_data[group_id][ip] = online_list
    with open(current_dir, 'w', encoding = 'UTF-8') as af:
        json.dump(f_data, af, indent=4, ensure_ascii=False)