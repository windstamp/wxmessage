# -*- coding:utf-8 -*-

__author__ = 'Furnace'

import json
import redis
import tool

def reload():
    # load conf.json 
    with open("conf.json",'r') as conf_file:
        conf = json.load(conf_file)
	
    ipaddr = conf['ipaddr']
    port = conf['port']
    dbno = conf['dbno']
	
    redis_tool = tool.RedisTool(ipaddr, port, dbno)
    conn = redis_tool.get_conn()
    # print('Is connected to Redis: ', conn.ping() )
    if not conn.ping():
        print('Is connected to Redis: ', conn.ping() )
        return
	
	# clear
    conn.delete('friend_name_list')
	
	# load friends
    with open("friends.txt",'r') as friends_file:
        for line in friends_file.readlines():
            if not len(line) or line.startswith('#'):
                continue
            line = line.replace('\n', '')
            print('line = ', line)
            conn.rpush('friend_name_list', line)
	
    friend_name_list = conn.lrange('friend_name_list', 0, -1)
    # print('friend_name_list = ', friend_name_list)
    for friend_name in friend_name_list:
        # friend_name = unicode(friend_name, 'utf-8')	# python 2
        friend_name = friend_name.decode('utf-8').replace('\n', '')		# python 3
        print('friend_name = ', friend_name )

if __name__ == '__main__':
    reload()
