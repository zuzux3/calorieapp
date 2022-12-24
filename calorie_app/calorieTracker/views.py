from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SelectFoodForm, AddFoodForm, CreateUserForm, ProfileForm
from .models import *
from datetime import timedelta
from django.utils import timezone
from datetime import date
from datetime import datetime
from .filters import FoodFilter

# home page view
@login_required(login_url='login')
def HomePageView(request):
    calories = Profile.objects.filter(personOf=request.user).last()
    calorieGoal = calories.calorieGoal

    if date.today() > calories.date:
        profile=Profile.objects.create(personOf=request.user)
        profile.save()

    calories = Profile.objects.filter(personOf=request.user).last()

    allFoodToday = PostFood.objects.filter(profile=calories)

    calorieGoalStatus = calorieGoal - calories.totalCalorie
    overCalorie = 0

    if calorieGoalStatus < 0:
        overCalorie = abs(calorieGoalStatus)

    context = {
        'totalCalorie': calories.totalCalorie,
        'calorieGoal': calorieGoal,
        'calorieGoalStatus': calorieGoalStatus,
        'overCalorie': overCalorie,
        'foodSelectedToday': allFoodToday
    }

    return render(request, 'home.html', context)

# signup page
def RegisterPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    else:
        form = CreateUserForm()
        
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

            context = {
                'form': form
            }

            return render(request, 'register.html', context)

#login page
def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')

            else:
                messages.info(request, 'Username or password is incorrect. Please try again.')
        
        context = {}

        return render(request, 'login.html', context)

#logout page
def LogoutPage(request):
    logout(request)
    return redirect('login')

#for selecting each day
@login_required
def selectFood(request):
    person = Profile.objects.filter(personOf=requestUser).last()

    foodItems = Food.objects.filter(personOf=request.user)
    form = SelectFoodForm

    if request.method == 'POST':
        form = SelectFoodForm(request.user, request.POST, instance=person)

        if form.is_valid():
            form.save()
            return redirect('home')

        else:
            form = SelectFoodForm(request.user)

        context = {
            'form': form,
            'foodItems': foodItems
        }

        return render(request, 'selectFood.html', context)

def addFood(request):
    foodItems = Food.objects.filter(personOf = request.user)
    form = AddFoodForm(request.POST)

    if request.method == 'POST':
        form = AddFoodForm(request.POST)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.personOf = request.user
            profile.save()

            return redirect('addFood')

        else:
            form = AddFoodForm()

        myFilter = FoodFilter(request.GET, queryset=foodItems)
        foodItems. myFilter.qs

        context = {
            'form': form,
            'foodItems': foodItems,
            'myFilter': myFilter
        }

        return render(request, 'addFood.html', context)

@login_required
def updateFood(request, pk):
    foodItems = Food.objects.filter(personOf=request.user)
    foodItem = Food.objects.get(id=pk)
    form = AddFoodForm(instance=foodItem)

    if request.method == 'POST':
        form = AddFoodForm(request.POST, instance=foodItem)

        if form.is_valid():
            form.save()
            return redirect('profile')

    myFilter = FoodFilter(request.GET, queryset=foodItems)
    context = {
        'form': form,
        'foodItems': foodItems,
        'myFilter': myFilter
    }

    return render(request, 'addFood.html', context)
@login_required
def deleteFood(request,pk):
	food_item = Food.objects.get(id=pk)
	if request.method == "POST":
		food_item.delete()
		return redirect('profile')
	context = {'food':food_item,}
	return render(request,'delete_food.html',context)


#profile page of user
@login_required
def ProfilePage(request):
    person = Profile.objects.filter(personOf=request.user).last()
    foodItems = Food.objects.filter(personOf=request.user)
    form = ProfileForm(instance=person)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=person)

        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = ProfileForm(instance=person)

    someDayLastWeek = timezone.now().date() - timedelta(days=7)
    records = Profile.objects.filter(date__gte=someDayLastWeek, date__lt=timezone.now().date(), personOf=request.user)

    context = {
        'form': form,
        'foodItems': foodItems,
        'records': records
    }

    return render(request, 'profile.html', context)