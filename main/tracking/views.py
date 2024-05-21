from django.http import HttpRequest, HttpResponse

def home(request):
    return HttpResponse("This is the tracking dashboard")