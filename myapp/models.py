from django.db import models

# Create your models here.
class Employee(models.Model):  
    eid = models.CharField(max_length=20)  
    ename = models.CharField(max_length=100)    
    econtact = models.CharField(max_length=15)  
    salary = models.IntegerField()
    
    class Meta:  
        db_table = "employee"


class Dreamreal(models.Model):
    website = models.CharField(max_length=50)
    mail = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    phonenumber = models.IntegerField()

    class Meta:
        db_table = "dreamreal"

class Online(models.Model):
    domain = models.CharField(max_length=30)
    # PERBAIKAN MODUL: ForeignKey ditaruh di sini agar One-to-Many nya benar
    company = models.ForeignKey(Dreamreal, on_delete=models.CASCADE) 
    
    class Meta:
        db_table = "online"

class Profile(models.Model):
   name = models.CharField(max_length = 50)
   picture = models.ImageField(upload_to = 'pictures')

   class Meta:
      db_table = "profile"