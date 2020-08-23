from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import ordersForm, CreateUserForm, StaffForm, StaffFormInternal, employeeordersForm
from .decorators import unauthenticated_user, allowed_users, admin_only


@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)
			#Added username after video because of error returning customer name if not added
			Staff.objects.create(
				user=user,
				employee_name=user.username,
				)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
	orders1 = orders.objects.all()
	customers = Staff.objects.all()
	reqs = requests.objects.all()
	tags = tag.objects.all()

	
#gnore
	Search_Requests = request.GET.get('Search_Requests')

	if Search_Requests != '' and Search_Requests is not None:
		#orders1 = Staff.objects.filter(orders__staff__startswith='Search_Requests')
	    orders1 = orders1.filter(status__startswith=Search_Requests)


	Search_Employees = request.GET.get('Search_Employees')

	if Search_Employees != '' and Search_Employees is not None:
		#orders1 = Staff.objects.filter(orders__staff__startswith='Search_Requests')
	    customers = customers.filter(employee_name__startswith=Search_Employees)
  #gnore

	total_staff = customers.count()

	total_orders = orders1.count()
	granted = orders1.filter(status='Granted').count()
	pending = orders1.filter(status='Pending').count()

	context = {'orders1':orders1, 'customers':customers,
	'total_orders':total_orders,'granted':granted,
	'pending':pending, 'reqs':reqs, 'tags':tags }

	return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request,):
	orders = request.user.staff
	form = ordersForm(instance=orders)
	
		
	if request.method == 'POST':
		form = ordersForm(request.POST, request.FILES,instance=orders)
		if form.is_valid():
			form.save()

	
	context = {'orders':orders, 'form':form}
	return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.staff
	form = StaffForm()

	if request.method == 'POST':
		form = StaffForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def accountSettingsinternal(request):
	customer = request.user.staff
	form2 = StaffFormInternal(instance=customer)

	if request.method == 'POST':
		form2 = StaffFormInternal(request.POST, request.FILES,instance=customer)
		if form2.is_valid():
			form2.save()


	context = {'form2':form2}
	return render(request, 'accounts/account_settings_internal.html', context)	

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = requests.objects.all()
	orders2 = orders.objects.all()



	context = {'orders2':orders2, 'products':products}


	return render(request, 'accounts/products.html', context) 

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,  pk_test):
	
	staff2 = Staff.objects.get(id=pk_test)
	form = StaffFormInternal(instance=staff2)

	if request.method == 'POST':
		form = StaffFormInternal(request.POST, request.FILES,instance=staff2)
		if form.is_valid():
			form.save()
	

	



	context = {'staff2':staff2, 'form':form, 'orders':orders}
	return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	staff = Staff.objects.get(id=pk)
	
	form = ordersForm(initial={'staff':staff})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = ordersForm(request.POST)
		
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

	order = orders.objects.get(id=pk)
	form = ordersForm(instance=order)

	if request.method == 'POST':
		form = ordersForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order = orders.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete.html', context)


	