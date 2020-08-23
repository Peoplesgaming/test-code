from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms



from .models import *


class StaffForm(ModelForm):
	class Meta:
		model = Staff
		fields = '__all__'
		exclude = ['user', 'employee_role', 'employee_permanent_role', 'employee_leave_amount', 'employee_unauthorized_leave_amount'
		,'employee_Warnings_amount', 'employee_comendations_amount', 'employee_agrees_terms', 'Date_created', 'ppe_issued', 'training_complete' ]


class StaffFormInternal(ModelForm):
	class Meta:
		model = Staff
		fields = '__all__'



class ordersForm(ModelForm):
	class Meta:
		model = orders
		fields = '__all__'


class employeeordersForm(ModelForm):
	class Meta:
		model = orders
		fields = '__all__'
		exclude = ['staff', 'status']




class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']