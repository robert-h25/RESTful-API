

# Create your views here.
from urllib.parse import parse_qs
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
import json
from .models import Story


@csrf_exempt
def login_user(request):
    # preparing method is not POST
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-type'] = 'text/plain'
    if(request.method != 'POST'):
        http_bad_response.content = 'POST request is expected: ERROR\n'
        return http_bad_response
    
    #Else we have a POST request
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    # Not logged in
    if user is not None:
        login(request, user)
        # return code 200 and welcome message
        return HttpResponse("Welcome {}.".format(username),status=200)
    else:
        return HttpResponse("The login has failed, please check username and password",status=401)
        
@csrf_exempt
@login_required
def logout_user(request):
    # catch unauthorised requests
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-type'] = 'text/plain'
    if(request.method != 'POST'):
        http_bad_response.content = 'POST request is expected: ERROR\n'
        return http_bad_response
    # else logout
    logout(request)
    return HttpResponse("See you later aligator!", status=200, content_type="text/plain")

@csrf_exempt
@login_required
def post_stories(request):
    # prepare bad request
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-type'] = 'text/plain'
    if(request.method == "GET"):
        return get_stories(request)    
    if(request.method != 'POST'):
        http_bad_response.content = 'POST request is expected: ERROR\n'
        return http_bad_response
    # Else post request
    
    try:
        data = json.loads(request.body)
        headline = data.get('headline')
        category = data.get('category')
        region = data.get('region')
        details = data.get('details')
        # write and save to DB
        story = Story.objects.create(headline=headline, category=category, region=region, details=details, author=request.user.username, date=datetime.now())
        story.save()
        return HttpResponse("Story has been posted successfully.",status=200, content_type="text/plain")
    except Exception as e:
        return HttpResponse("Unable to post the story: {}".format(str(e)), status=503, content_type="text/plain")

@csrf_exempt
@login_required
def get_stories(request):
    
    # prepare bad request
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-type'] = 'text/plain'
    if(request.method != 'GET'):
        http_bad_response.content = 'GET request is expected: ERROR\n'
        return http_bad_response

    # try except clause
    try:

        # get story category,region, date from json
       
        story_cat = request.GET.get('story_cat', '*')
        story_region = request.GET.get('story_region', '*')
        story_date = request.GET.get('story_date', '*')
    
        # query DB
        category = Q(category=story_cat) if story_cat != "*" else Q()
        region = Q(region=story_region) if story_region != "*" else Q()
        date = Q(date=story_date) if story_date != "*" else Q()
        query = category & region & date
        stories = Story.objects.filter(query)

        if len(stories)==0:
            return HttpResponse("No stories with them parameters",status=404, content_type="text/plain")
        # return as JSON response
        response = []
        for story in stories:
            response.append({
                'key':story.key,
                'headline':story.headline,
                'story_cat':story.category,
                'story_region':story.region,
                'author':story.author,
                'story_date':story.date,
                'story_details':story.details
            })
        return JsonResponse({'stories':response},status=200, content_type="application/json")

    #catch exception
    except Exception as e:
        return HttpResponse("Unable to retirieve the stories from the server: {}".format(str(e)),status=404, content_type="text/plain")

@csrf_exempt
@login_required
def delete(request,key):
    # prepare bad request
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-type'] = 'text/plain'
    if(request.method != 'DELETE'):
        http_bad_response.content = 'DELETE request is expected: ERROR\n'
        return http_bad_response
    # try get story from key
    try:
        story = Story.objects.get(key=key)
        # check its the same author
        if story.author == request.user.username:
            story.delete()
            return HttpResponse("The story has been successfully deleted.",status=200, content_type="text/plain")
        else:
            return HttpResponse("You do not have permission to delete that story",status=503, content_type="text/plain")
    #catch exception
    except Exception as e:
        return HttpResponse("Unable to delete the story: {}".format(str(e)),status=503, content_type="text/plain")
    
def temp(request):
    return HttpResponse(status=404)