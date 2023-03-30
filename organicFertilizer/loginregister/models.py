from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Company(models.Model):
    email = models.TextField()
    first_name = models.TextField()
    username = models.TextField()
    password = models.TextField()
    company = models.TextField()
    def __str__(self):
        return self.company
class Blogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    description = models.TextField()
    media = models.FileField(upload_to='')
    def __str__(self):
        return self.user.username+"-"+self.title
class Newsmodel(models.Model):
    title = models.TextField()
    description = models.TextField()
    media = models.FileField(upload_to='')
    def __str__(self):
        return self.title
class Fertilizermodel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    description = models.TextField()
    rating = models.IntegerField()
    media = models.FileField(upload_to='')
    def __str__(self):
        return self.title
class Expertsmodel(models.Model):
    name = models.TextField()
    description = models.TextField()
    rating = models.IntegerField()
    contact = models.TextField()
    email = models.EmailField()
    avtar = models.FileField(upload_to='')
    def __str__(self):
        return self.name
class AppointmentScheduleModel(models.Model):
    title = models.TextField()
    appointmentDate = models.TextField()
    farmer = models.ForeignKey(User ,on_delete=models.DO_NOTHING)
    expert =models.ForeignKey(Expertsmodel,on_delete=models.DO_NOTHING)
    description = models.TextField()
    
    def __str__(self):
        return self.title + self.expert.name
