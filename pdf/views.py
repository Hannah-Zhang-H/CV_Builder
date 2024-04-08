from django.shortcuts import render
from .models import Profile
# Create your views here.

def accept(request):
    return render(request, 'pdf/accept.html')