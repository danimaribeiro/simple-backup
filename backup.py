#coding=utf-8
'''
Created on 14/10/2013

@author: Danimar
'''
from time import gmtime, strftime
import subprocess
import os
import glob
import time
import psycopg2
import storage 
import mail
 
# change these as appropriate for your platform/environment :
USER = "postgres"
PASS = ""
HOST = "localhost"
 
BACKUP_DIR = "D:\\postgresql_backups\\"
dumper = """ "C:\\Program Files\\PostgreSQL\\9.3\\bin\\pg_dump" -U %s -Z 9 -f %s -F c %s  """                  
 
def log(string):
    print time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime()) + ": " + str(string)


def execute_backup(): 
    # Change the value in brackets to keep more/fewer files. time.time() returns seconds since 1970...
    # currently set to 2 days ago from when this script starts to run.
     
    x_days_ago = time.time() - ( 60 * 60 * 24 * 2 )     
    os.putenv('PGPASSWORD', PASS)
     
    con = psycopg2.connect(database='postgres', user=USER, host=HOST, password=PASS)
    cur = con.cursor()
    cur.execute("""SELECT datname from pg_database where datistemplate = false;""")
     
    database_list = cur.fetchall()    
    
    # Delete old backup files first.
    for database_name in database_list :
        database_name = database_name[0]
        if database_name == '':
            continue
     
        glob_list = glob.glob(BACKUP_DIR + database_name + '*' + '.pgdump')
        for file in glob_list:
            file_info = os.stat(file)
            if file_info.st_ctime < x_days_ago:
                log("Unlink: %s" % file)
                os.unlink(file)
            else:
                log("Keeping : %s" % file)
     
    log("Backup files older than %s deleted." % time.strftime('%c', time.gmtime(x_days_ago)))
     
    # Now perform the backup.
    for database_name in database_list:
        database_name = database_name[0]
        if database_name == 'postgres':
            continue
     
        log("dump started for %s" % database_name)
        thetime = str(strftime("%Y-%m-%d-%H-%M")) 
        file_name = database_name + '_' + thetime + ".sql.pgdump"
        #Run the pg_dump command to the right directory
        command = dumper % (USER,  BACKUP_DIR + file_name, database_name)
        log(command)
        subprocess.call(command,shell = True)
        log("%s dump finished" % database_name)
        
        storage.upload_to_s3('secret', 'key', 'danimaribeiro_aws_backup', BACKUP_DIR + file_name)
        mail.send_email('@gmail.com', 'para', 'Backup completo', 'Alguns backups não puderam ser completados')
        
    log("Backup job complete.")


if __name__ == '__main__':
    execute_backup()
