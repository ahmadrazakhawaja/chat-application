from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    status = models.CharField(max_length=7,null=True)
    pass


class contacts(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE,related_name="User")
    contact=models.CharField(max_length=30)
    channel=models.CharField(max_length=30)

    def serialize(self):
        return {
            "contact-name": self.contact
        }

class groups(models.Model):
    group_name = models.CharField(max_length=20)

class groupcontact(models.Model):
    group = models.ForeignKey(groups,on_delete=models.CASCADE,related_name="group")
    members = models.IntegerField()

class usermessages(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="User2")
    reciever = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

class notifications(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE,related_name="User3",null=True)
    message = models.TextField()
    channel = models.CharField(max_length=20)
    seen = models.CharField(max_length=8,default="Unseen")
     

class groupadmin(models.Model):
    group = models.ForeignKey(groups,on_delete=models.CASCADE,related_name="group2")
    User = models.ForeignKey(User,on_delete=models.CASCADE,related_name="User4")

class groupcreator(models.Model):
    group = models.ForeignKey(groups,on_delete=models.CASCADE,related_name="group3")
    User = models.ForeignKey(User,on_delete=models.CASCADE,related_name="User5")




    


