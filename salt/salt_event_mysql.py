#!/bin/env python
#coding=utf8
# Import python libs
import json
# Import salt modules
import salt.config
import salt.utils.event
# Import third part libs
import MySQLdb
import re
__opts__ = salt.config.client_config('/etc/salt/master')
#create MySQL connect
conn = MySQLdb.connect(host=__opts__['mysql.host'],user=__opts__['mysql.user'],passwd=__opts__['mysql.pass'],db=__opts__['mysql.db'],port=__opts__['mysql.port'])
cursor = conn.cursor()
# Listen Salt Master Event System
event = salt.utils.event.MasterEvent(__opts__['sock_dir'])
for eachevent in event.iter_events(full=True):
    ret = eachevent['data']
    if re.match(r"\d+", eachevent['tag']):
        sql_jids = ''' INSERT INTO `jids` (`jid`,`runtime`,`minions`)
                        VALUES ('%s','%s','%s') ''' % (eachevent['tag'], ret['_stamp']," ".join(ret['minions']))
        cursor.execute(sql_jids)
        cursor.execute("COMMIT")
    if "salt/job/" in eachevent['tag']:
        #Return Event
        if ret.has_key('id') and ret.has_key('return'):
            #Ignore saltutil.find_job event
            if ret['fun'] == "saltutil.find_job":
                continue
	    sql_jids = ''' INSERT INTO `jids` 
			(`jid`,`load`) VALUES (%s,%s)'''
            sql = '''INSERT INTO `salt_returns`
                (`fun`,`jid`,`return`,`id`,`success`,`full_ret` )
                VALUES (%s,%s,%s,%s,%s,%s)'''
            cursor.execute(sql,(ret['fun'],ret['jid'],
                                json.dumps(ret['return']),ret['id'],
                                ret['success'],json.dumps(ret)))
            cursor.execute("COMMIT")
    # Other Event
    else:
        pass
