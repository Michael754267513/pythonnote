from jenkinsapi.jenkins import Jenkins

def get_server_instance():
    jenkins_url = 'http://192.168.12.172:8080'
    server = Jenkins(jenkins_url, username = 'michael', password = 'laoshu')
    return server

if __name__ == '__main__':
    print get_server_instance().version

"""Get job details of each job that is running on the Jenkins instance"""
def get_job_details():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    for j in server.get_jobs():
        job_instance = server.get_job(j[0])
        print 'Job Name:%s' %(job_instance.name)
        print 'Job Description:%s' %(job_instance.get_description())
        print 'Is Job running:%s' %(job_instance.is_running())
        print 'Is Job enabled:%s' %(job_instance.is_enabled())

"""Disable a Jenkins job"""
def disable_job():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    job_name = 'test'
    if (server.has_job(job_name)):
        job_instance = server.get_job(job_name)
        job_instance.disable()
        print 'Name:%s,Is Job Enabled ?:%s' %(job_name,job_instance.is_enabled())

def get_plugin_details():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    for plugin in server.get_plugins().values():
        print "Short Name:%s" %(plugin.shortName)
        print "Long Name:%s" %(plugin.longName)
        print "Version:%s" %(plugin.version)
        print "URL:%s" %(plugin.url)
        print "Active:%s" %(plugin.active)
        print "Enabled:%s" %(plugin.enabled)
get_server_instance()
get_job_details()
'''get_plugin_details()'''