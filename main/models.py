from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class camping(models.Model):
    name = models.CharField(max_length=100,null=True)
    type = models.CharField(max_length=20,null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    location = models.CharField(max_length=100,null=True)
    location2 = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=25,null=True)
    people = models.IntegerField(null=True)
    facilities = models.CharField(max_length=100,null=True)
    safefacilities = models.CharField(max_length=100,null=True)
    otherfacilities = models.CharField(max_length=100,null=True)
    time  = models.CharField(max_length=100,null=True)
    cost = models.CharField(max_length=500,null=True)
    managerphone = models.CharField(max_length=25,null=True)
    manager = models.CharField(max_length=100,null=True)
    managelocation = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='author_comment')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField() #글 등록할 때 timezone으로부터 받아옴
    modify_date = models.DateTimeField(null=True, blank=True)
    camping_id = models.ForeignKey(camping, on_delete=models.CASCADE, null=True )
    voter = models.ManyToManyField(User, related_name='voter_comment')

    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='author_answer')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')
    def __str__(self):
        return self.content