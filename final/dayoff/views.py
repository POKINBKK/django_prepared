from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from dayoff.forms import EmployeeForm, LoginForm, leaveRequestForm
from django.contrib.auth.models import User
from dayoff.models import Dayoff


@login_required
def index(request):
    context = {}
    try:
        context['dayoff_list'] = Dayoff.objects.all().filter(
            create_by=User.objects.get(username=request.user.username)
        )

    except User.DoesNotExist:
        context['dayoff_list'] = None
    return render(request, 'dayoff/index.html', context=context)

def mylogin(request):
    login_form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if request.user.is_staff:
                    return redirect("admin:index")
                else:
                    return redirect("index")
    elif request.method == 'GET':
        if (request.user.is_authenticated):
            return redirect("index")
    context = {'login_form': login_form}
    return render(request, 'dayoff/login.html', context=context)

def register(request):
    user_form = EmployeeForm()
    if request.method == "POST":
        user_form = EmployeeForm(request.POST)
        if user_form.is_valid():
            user = User.objects.create_user(
                username=user_form.cleaned_data.get("username"),
                first_name=user_form.cleaned_data.get("firstname"),
                last_name=user_form.cleaned_data.get("lastname"),
                email=user_form.cleaned_data.get("email"),
                password=user_form.cleaned_data.get("password1")
            )

            user.save()
            return redirect('index')

    context = {'user_form': user_form}
    return render(request, 'dayoff/register.html', context=context)


@login_required
def leaveRequest(request):
    leave_form = leaveRequestForm()
    if request.method == "POST":
        leave_form = leaveRequestForm(request.POST)
        if leave_form.is_valid():
            Dayoff.objects.create(
                create_by_id = (User.objects.get(username=request.user.username)).id,
                reason=leave_form.cleaned_data.get("reason"),
                type=leave_form.cleaned_data.get("type"),
                date_start=leave_form.cleaned_data.get("start_date"),
                date_end=leave_form.cleaned_data.get("end_date"),
            )
            return redirect('index')
    context = {'leave_form': leave_form}
    return render(request, 'dayoff/leaveRequest.html', context=context)
