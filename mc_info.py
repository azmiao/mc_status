from mcstatus import MinecraftServer
import os

# 请填写你的ip加端口，格式：'xxx.xxx.xx.xx:xxxx'
# 这是样例：
# ip = '118.30.26.45:25565'
ip = ''
server = MinecraftServer.lookup(ip)
def get_status():
    try:
        query = server.query()
        msg = "该服务器内目前有 {0} 位玩家:\n {1}\n服务器延迟为 {2} ms".format(len(query.players.names), " | ".join(query.players.names), 21) # 延迟21ms，纯属写着好看
    except Exception as e:
        msg = f'查询失败！错误明细：{e}'
    return msg

def judge():
    current_dir = os.path.join(os.path.dirname(__file__), 'member.txt')
    f = open(current_dir)
    m_list = f.read().splitlines()
    f.close()
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
    print(online_list)
    if len(add_member)== 0 and len(del_member) == 0:
        return 'nothing', del_member, add_member, online_list
    else:
        return 'change', del_member, add_member, online_list

def replace_mem(online_list):
    current_dir = os.path.join(os.path.dirname(__file__), 'member.txt')
    f = open(current_dir,"w")
    for line in online_list:
        f.write(line+'\n')
    f.close()