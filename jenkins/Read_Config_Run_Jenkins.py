from Jenkins_Test import *
from ReadConfigFile import *

jenkins_server = get_server_instance(jenkins_url,username,password)
run_server_job(jenkins_server,"test")