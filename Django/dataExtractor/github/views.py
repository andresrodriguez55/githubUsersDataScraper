from ast import Not
from dataclasses import dataclass
import json
from this import d
from typing import final
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import requests
from .models import GithubUser
from django.views.decorators.csrf import csrf_protect
from django.utils.safestring import SafeString

# Create your views here.

def main(request):
    return render(request, "main.html",)

def __graphqlQuery(searchedKeyword):
    variables = {"searchedKeyword" : searchedKeyword + " repos:>0"} #AUMENTAR TAMANO DE DATOS, EXTRAER TODO
    query = """
    query($searchedKeyword : String!)
    {
        search(query: $searchedKeyword, type:USER, first: 50) 
        { 
            nodes
            {
                ... on User
                {
                    login,
                    name,
                    avatarUrl,
                    bio,
                    email,
                    location,
                    company,
                    websiteUrl
                    followers(first: 0)
                    {
                        totalCount
                    }
                        repositories(first: 100)
                    {
                        totalCount,
                        nodes
                        {
                            ... on Repository
                            {
                                stargazerCount,
                                forkCount
                                primaryLanguage 
                                {
                                    name
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    """
    
    header = {'Authorization': "token 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", 'content-type': 'application/json'}
    json = {'query' : query, 'variables' : variables}
    request = requests.post('https://api.github.com/graphql', json=json, headers=header)
    if request.status_code == 200:
        return request.json()
    else:
        return {}

def extractData(request):
    searched = request.GET.get('query')
    if searched is not None and len(searched) != 0:
        result = []

        data = __graphqlQuery(searched).get("data")
        searchedUsers = data.get("search")
        searchedUsersNodes = searchedUsers.get("nodes")
        usersJsonArray = searchedUsersNodes

        checkedUserCounter = 0
        while checkedUserCounter<len(usersJsonArray): #controlar que el usuario no exista en la base de datos
            extractedUserJson = usersJsonArray[checkedUserCounter]
            
            userJson = { 
                "username" : extractedUserJson.get("login"),
                "name" : extractedUserJson.get("name").replace('\'', "") if extractedUserJson.get("name") is not None else '',
                "email" : extractedUserJson.get("email") if extractedUserJson.get("email") is not None else '',
                "websiteURL" : extractedUserJson.get("websiteUrl") if extractedUserJson.get("websiteUrl") is not None else '',
                "location" : extractedUserJson.get("location").replace('\'', "") if extractedUserJson.get("location") is not None else '',
                "company" : extractedUserJson.get("company").replace('\'', "") if extractedUserJson.get("company") is not None else '',
                "bio" : extractedUserJson.get("bio").replace('\'', "") if extractedUserJson.get("bio") is not None else '',
                "profilePictureURL" : extractedUserJson.get("avatarUrl") if extractedUserJson.get("avatarUrl") is not None else '',
                "followersCount" : 0,
                "repositoriesCount" : 0,

                "forksObtained" : 0,
                "starsObtained" : 0,
                "languageMostUsed" : ''
            }

            if extractedUserJson.get("followers") is not None:
                userJson["followersCount"] = extractedUserJson.get("followers").get("totalCount")

            if extractedUserJson.get("repositories") is not None:
                userJson["repositoriesCount"] = extractedUserJson.get("repositories").get("totalCount")

                languagesUsed = {}
                repositoriesJsonArray = extractedUserJson.get("repositories").get("nodes") 
                for repositoryJson in repositoriesJsonArray:

                    userJson["forksObtained"] = userJson.get("forksObtained") + repositoryJson.get("forkCount")
                    userJson["starsObtained"] = userJson.get("starsObtained") + repositoryJson.get("stargazerCount")
                    
                    primaryLanguage = repositoryJson.get("primaryLanguage")
                    if primaryLanguage is not None:
                        primaryLanguage=primaryLanguage.get("name")
                        languagesUsed[primaryLanguage] = languagesUsed.get(primaryLanguage, 0) + 1
                
                if(len(languagesUsed)>0):
                    userJson["languageMostUsed"] = max(languagesUsed, key=languagesUsed.get)
                    
                result.append(userJson)

            checkedUserCounter += 1 

        context = {
            "users" : result,
        }
        return render(request, "extractData.html", context)

    return render(request, "extractData.html")

@csrf_protect
def createGithubUser(request):
    if request.method == 'POST':
        values = request.POST.dict()

        try:
            GithubUser.objects.update_or_create(**values)
            return HttpResponse(request.POST['name'] + " added!")
        except Exception as e:
            return HttpResponse("error...")
    else:
        return HttpResponse("error..")

def extractedData(request):
    context = {"storedUsers" : GithubUser.objects.all()}
    return render(request, "extractedData.html", context)