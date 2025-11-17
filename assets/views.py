from django.http import HttpResponse

def home(request):
    return HttpResponse("Assets module working successfully!")
