from django.db import models

class Users(models.Model):
  uid = models.AutoField(primary_key=True)
  fname = models.CharField(max_length=250)
  lname = models.CharField(max_length=250)
  email = models.CharField(max_length=500)
  handle = models.CharField(unique=True,max_length=100)
  password = models.CharField(max_length=250)
  about = models.TextField()
  def __unicode__(self):
        return self.handle


class Followers(models.Model):
  fs_id = models.AutoField(primary_key=True)
  uid = models.ForeignKey(Users)
  follower_id = models.IntegerField(Users)
  since = models.DateTimeField('Followed on')

class Following(models.Model):
  fg_id = models.AutoField(primary_key=True)
  uid = models.ForeignKey(Users)
  following_id = models.IntegerField(Users)
  since = models.DateTimeField('Following on')

class Tweets(models.Model):
  tid = models.AutoField(primary_key=True)
  uid = models.ForeignKey(Users)
  posted = models.DateTimeField('Followed on')
  tweet = models.TextField(max_length = 160)
  
class Hashtag(models.Model):
  hid = models.AutoField(primary_key=True)
  tid = models.ForeignKey(Tweets)
  hash_name = models.CharField(max_length = 160)

  
