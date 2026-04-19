from django.contrib import admin
from .models import Employee
from .models import Employee, Dreamreal

# Menggunakan fitur Decorator (@) agar kode lebih bersih
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # Sesuaikan dengan nama kolom yang baru di models.py
    list_display = ("eid", "ename", "econtact", "salary")
    
    # Kalau ada search_fields, pastikan pakai nama kolom yang baru juga
    search_fields = ("ename",)

    admin.site.register(Dreamreal)