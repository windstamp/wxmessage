# -*- coding:utf-8 -*-

__author__ = 'Furnace'

import json
import redis
import tool

def setup():
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
    conn.delete('index')
    conn.delete('message_pool')
    conn.delete('message_pool_crc')
	
	# load friends
    with open("friends.txt",'r') as friends_file:
        for line in friends_file.readlines():
            if not len(line) or line.startswith('#'):
                continue
            print('line = ', line)
            conn.rpush('friend_name_list', line)
	
    friend_name_list = conn.lrange('friend_name_list', 0, -1)
    # print('friend_name_list = ', friend_name_list)
    for friend_name in friend_name_list:
        # friend_name = unicode(friend_name, 'utf-8')	# python 2
        friend_name = friend_name.decode('utf-8').replace('\n', '')		# python 3
        print('friend_name = ', friend_name )
	
	# initial message index
    conn.set('index', 0)
    index = conn.get('index')
    print('index = ', index)
	
	# initial message pool
    conn.rpush('message_pool', '你好')
    conn.rpush('message_pool', '我好')
    conn.rpush('message_pool', '他好')
    conn.rpush('message_pool', '大家好')
    conn.rpush('message_pool', '风暴英雄')
    conn.rpush('message_pool', '炉石传说')
    conn.rpush('message_pool', '魔兽世界')
    conn.rpush('message_pool', '暗黑破坏神')
    conn.rpush('message_pool', '星际争霸')
    conn.rpush('message_pool', '守望先锋')
    conn.rpush('message_pool', '英雄联盟')
    conn.rpush('message_pool', '绝地求生')
    conn.rpush('message_pool', '虎口脱险')
    conn.rpush('message_pool', '毕业生')
    conn.rpush('message_pool', '实习生')
    conn.rpush('message_pool', '歌舞青春')
    conn.rpush('message_pool', '放牛班的春天')
	
    message_pool = conn.lrange('message_pool', index, 20)
    print('message_pool = ', message_pool)
	
    for msg in message_pool:
        msg = msg.decode('utf-8')
        print('msg = ', msg)
	
	# initial message pool crc
    crc_tool = tool.CRCTool()
    conn.sadd('message_pool_crc', crc_tool.get_value('你好') )
    conn.sadd('message_pool_crc', crc_tool.get_value('我好') )
    conn.sadd('message_pool_crc', crc_tool.get_value('他好') )
    conn.sadd('message_pool_crc', crc_tool.get_value('大家好') )
    conn.sadd('message_pool_crc', crc_tool.get_value('风暴英雄') )
    conn.sadd('message_pool_crc', crc_tool.get_value('炉石传说') )
    conn.sadd('message_pool_crc', crc_tool.get_value('魔兽世界') )
    conn.sadd('message_pool_crc', crc_tool.get_value('暗黑破坏神') )
    conn.sadd('message_pool_crc', crc_tool.get_value('星际争霸') )
    conn.sadd('message_pool_crc', crc_tool.get_value('守望先锋') )
    conn.sadd('message_pool_crc', crc_tool.get_value('英雄联盟') )
    conn.sadd('message_pool_crc', crc_tool.get_value('绝地求生') )
    conn.sadd('message_pool_crc', crc_tool.get_value('虎口脱险') )
    conn.sadd('message_pool_crc', crc_tool.get_value('毕业生') )
    conn.sadd('message_pool_crc', crc_tool.get_value('实习生') )
    conn.sadd('message_pool_crc', crc_tool.get_value('歌舞青春') )
    conn.sadd('message_pool_crc', crc_tool.get_value('放牛班的春天') )
	
    message_pool_crc = conn.smembers('message_pool_crc')
    print('message_pool_crc = ', message_pool_crc)
	
    for msg_crc in message_pool_crc:
        msg_crc = msg_crc.decode('utf-8')
        print('msg_crc = ', msg_crc)

if __name__ == '__main__':
    setup()
