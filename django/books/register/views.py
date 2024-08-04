from django.shortcuts import render
from django.http import HttpResponse
from .models import book

# Create your views here.
def register(request):
  # return HttpResponse('book is register!')
  context={
    "book":book.objects.all(),
  }
  return render(request,'index.html',context)
