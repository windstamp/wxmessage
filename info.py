# -*- coding:utf-8 -*-

__author__ = 'Furnace'

import crcmod
import json
import redis
import tool

def info():
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
	
	# infos
    friend_name_list = conn.lrange('friend_name_list', 0, -1)
    # print('friend_name_list = ', friend_name_list)
    for friend_name in friend_name_list:
        # friend_name = unicode(friend_name, 'utf-8')	# python 2
        friend_name = friend_name.decode('utf-8').replace('\n', '')		# python 3
        print('friend_name = ', friend_name )
    print('')
	
    index = conn.get('index')
    index = int(index)
    print('index = ', index)
    print('')
	
    message_pool_length = conn.llen('message_pool')
    print('message_pool_length = ', message_pool_length)
    message_pool = conn.lrange('message_pool', 0, -1)
    # print('message_pool = ', message_pool)
    for i, msg in enumerate(message_pool):
        if i >= 5:
            break
		
        # msg = unicode(msg, 'utf-8')	# python 2
        msg = msg.decode('utf-8')		# python 3
        print('i = %d, msg = %s' % (i, msg) )
    print('')
	
    message_pool_crc_length = conn.scard('message_pool_crc')
    print('message_pool_crc_length = ', message_pool_crc_length)
    message_pool_crc = conn.smembers('message_pool_crc')
    # print('message_pool_crc = ', message_pool_crc)
    for i, msg_crc in enumerate(message_pool_crc):
        if i >= 5:
            break
		
        # msg_crc = unicode(msg_crc, 'utf-8')	# python 2
        msg_crc = msg_crc.decode('utf-8')		# python 3
        print('i = %d, msg_crc = %s' % (i, msg_crc) )
    print('')
	
    last_hot_msg_update_timestamp = conn.get('last_hot_msg_update_timestamp')
    last_hot_msg_update_timestamp = int(last_hot_msg_update_timestamp)
    print('last_hot_msg_update_timestamp = ', last_hot_msg_update_timestamp)
    print('')

if __name__ == '__main__':
    info()
