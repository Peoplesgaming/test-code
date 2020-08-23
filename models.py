from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Staff(models.Model):
    YES_NO = (
            ('Yes','Yes'),
            ('No', 'No'),
            )
    STAFF_TYPE = (
              ('MANAGEMENT','MANAGEMENT'),
              ('SUPERVISER','SUPERVISER'),
              ('HGV DRIVER','HGV DRIVER'),
              ('LOADER','LOADER'),
              ('STREETS DRIVER','STREETS DRIVER'),
              ('STREETS LOADER','STREETS LOADER'),

    )
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=50, null=True)
    employee_role = models.CharField(choices=STAFF_TYPE, max_length=50, null=True)
    employee_permanent_role = models.CharField(max_length=50, null=True)
    employee_leave_amount = models.CharField(default=25, max_length=50, null=True)
    employee_unauthorized_leave_amount = models.CharField(default=0, max_length=50, null=True)
    employee_Warnings_amount = models.CharField(default=0,max_length=50, null=True)
    employee_comendations_amount = models.CharField(default=0, max_length=50, null=True)
    phone_number = models.CharField(max_length=50, null=True)
    email_address = models.EmailField(max_length=50, null=True)
    home_address = models.TextField(max_length=2000, null=True)
    next_of_kin = models.CharField(max_length=50, null=True)
    next_of_kin_address = models.TextField(max_length=2000, null=True)
    next_of_kin_phone = models.CharField(max_length=50, null=True)
    training_complete = models.CharField(choices=YES_NO, null=True, max_length=200)
    ppe_issued = models.CharField(choices=YES_NO, null=True, max_length=200)
    employee_agrees_terms = models.CharField(choices=YES_NO, null=True, max_length=200)
    profile_pic = models.ImageField(default='user.png',null=True, blank=True)
    Date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.employee_name


class tag(models.Model):
    tag_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.tag_name)



class requests(models.Model):
     REQTYPE = (
            ('Leave','Leave'),
            ('Uniform', 'Uniform'),
            ('Saftey Concern', 'Saftey Concern')
            )
     UNIFORMTYPE = (
            ('N/A','N/A'),
            ('Winter Jacket','Winter Jacket'),
            ('Shell Coat','Shell Coat'),
            ('Jumper','Jumper'),
            ('T-Shirt','T-Shirt'),
            ('Trousers','Trousers'),
            ('Boots','Boots'),
     )
           
     
     Date_created = models.DateTimeField(auto_now_add=True, null=True)
     tags = models.ManyToManyField(tag)

     def __str__(self):
        return self.request_type

class orders(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Denied', 'Denied'),
        ('Granted', 'Granted')
        )
    REQTYPE = (
            ('Leave','Leave'),
            ('Uniform', 'Uniform'),
            ('Saftey Concern', 'Saftey Concern')
            )
    UNIFORMTYPE = (
            ('N/A','N/A'),
            ('Winter Jacket','Winter Jacket'),
            ('Shell Coat','Shell Coat'),
            ('Jumper','Jumper'),
            ('T-Shirt','T-Shirt'),
            ('Trousers','Trousers'),
            ('Boots','Boots'),
     ) 
    staff = models.ForeignKey(Staff, null=True, on_delete= models.SET_NULL)
    request = models.CharField(choices=REQTYPE, null=True,max_length=50)
    leave_from = models.DateTimeField(null=True)
    leave_to = models.DateTimeField(null=True)
    Uniformtype = models.CharField(choices=UNIFORMTYPE, null=True, max_length=200)
    Uniformsize = models.CharField(max_length=50, null=True)
    Saftey_concern = models.TextField(max_length=1000, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(default='Pending',choices= STATUS, max_length=200, null=True)

    def __str__(self):
         return str(self.request)
   

