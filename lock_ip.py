import os
import json

current_dir = os.path.join(os.path.dirname(__file__), 'server.json')

# 监控 or 不监控
async def lock_or_unlock(is_lock, ip, group_id):
    with open(current_dir, 'r', encoding = 'UTF-8') as f:
        f_data = json.load(f)
    if group_id not in list(f_data.keys()):
        f_data[group_id] = {}
    if is_lock:
        if ip in list(f_data[group_id].keys()):
            return f'本群已经监控过该ip：{ip}啦'
        f_data[group_id][ip] = []
        msg = f'该群成功监控ip：{ip}'
    else:
        if group_id not in list(f_data.keys()):
            return f'该群未监控过ip：{ip}'
        if ip not in list(f_data[group_id].keys()):
            return f'该群未监控过ip：{ip}'
        f_data[group_id].pop(ip)
        msg = f'该群不再监控ip：{ip}'
    with open(current_dir, 'w', encoding = 'UTF-8') as af:
        json.dump(f_data, af, indent=4, ensure_ascii=False)
    return msg