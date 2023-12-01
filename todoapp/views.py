from django.shortcuts import render ,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate,login ,logout
from django.contrib.auth.decorators import login_required
from todoapp.models import TODO
# Create your views here.



@login_required(login_url='login')
def homepage(request):
  if request.method== 'POST':
     task = request.POST.get('task')
     new_todo= TODO(user=request.user,todo_name=task)
     new_todo.save()

  all_todos= TODO.objects.filter(user=request.user)
  context = {
       'todos' : all_todos
     }
  return render(request, 'todo.html' ,context )

def Signuppage(request):
  if request.user.is_authenticated:
    return redirect('home')
  if request.method=='POST':
    uname=request.POST.get('username')
    email=request.POST.get('email')
    pass1=request.POST.get('password')
    pass2=request.POST.get('password1')

    if pass1!=pass2:
      return HttpResponse("PASSWORD ARE NOT SAME ")
    else:
      my_user=User.objects.create_user(uname,email,pass1)
      my_user.save()
      return redirect('login')
    
  return render (request, 'register.html')

def loginpage(request):
  if request.user.is_authenticated:
    return redirect('home')
  if request.method=='POST':
    username=request.POST.get('username')
    pass1=request.POST.get('pass')
    user=authenticate(request,username=username ,password=pass1)
    if user is not None:
      login(request,user)
      return redirect('home')
    else:
      return HttpResponse("<h2>INCOORECT USERNAME AND PASSWORD<h2>")

  return render (request, 'login.html')




def logoutpage(request):
  logout(request)
  return redirect ('login')


@login_required(login_url='login')
def deletepath(request ,name):
  get_todo= TODO.objects.get(user=request.user ,todo_name=name)
  get_todo.delete()
  return redirect('home')


@login_required(login_url='login')
def update(request,name):
    get_todo = TODO.objects.get(user=request.user, todo_name=name)
    get_todo.status = True
    get_todo.save()
    return redirect('home')

