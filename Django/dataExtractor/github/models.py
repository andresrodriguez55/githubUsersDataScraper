from django.db import models

#https://github.com/dead-claudia/github-limits
class GithubUser(models.Model):
    username = models.CharField(max_length=39, primary_key=True)
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True) 
    websiteURL = models.CharField(max_length=255, null=True)
    location =  models.CharField(max_length=255, null=True)  
    company = models.CharField(max_length=255, null=True) 
    bio = models.CharField(max_length=160, null=True) 
    profilePictureURL = models.CharField(max_length=255, null=True)
    followersCount = models.IntegerField(default=0)
    repositoriesCount = models.IntegerField(default=0)
    forksObtained = models.IntegerField(default=0)
    starsObtained = models.IntegerField(default=0)
    languageMostUsed = models.CharField(max_length=100, null=True) 