#encoding: utf-8
import ConfigParser
class ReadHost:
    cf = ConfigParser.ConfigParser()
    cf.read("G:\code\config\hosts")
    '''返回指定ip'''
    def get_pc_ip(self,section,pc_name):
        ip = self.cf.get(section,pc_name)
        return ip
    '''返回分组内主机信息'''
    def get_pc_section(self,name):
        ip_lists = self.cf.options(name)
        return ip_lists
    '''返回分组机器名'''
    def get_pc_items(self,section):
        items = self.cf.items(section)
        return items

