from django.db import models


class UserInfo(models.Model):

    Username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    Email = models.EmailField(default="754267513@qq.com")


class UserType(models.Model):

    Name = models.CharField(max_length=100)


class UserGroup(models.Model):

    GroupName = models.CharField(max_length=50,default="guest")


class HostGroup(models.Model):

    hg = models.CharField(max_length=50)


class HostList(models.Model):

    ip = models.CharField(max_length=100)
    hg = models.ForeignKey(HostGroup)
    ug = models.ForeignKey(UserGroup)

