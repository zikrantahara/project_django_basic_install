from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import DreamrealForm
from .models import Dreamreal
from django.core.mail import send_mail, mail_admins, EmailMessage
from myapp.forms import LoginForm

def addnew(request):
    # Jika user mengklik tombol Submit (Kirim Data)
    if request.method == 'POST':
        form = DreamrealForm(request.POST) # Tangkap semua isian form sekaligus
        
        if form.is_valid(): # Cek apakah datanya benar/tidak ada yang kosong
            form.save()     # Simpan langsung ke database!
            return HttpResponse("<h2 align='center'>Data Berhasil Disimpan ke Database! 🎉</h2>")
            
    # Jika user baru pertama kali buka halaman (belum submit)
    else:
        form = DreamrealForm() 

    # Bawa form kosong tersebut ke halaman HTML
    context = {'form': form}
    return render(request, "myform.html", context)

def update_data(request, pk):
    # 1. Cari data di database berdasarkan nomor ID (pk)
    obj = Dreamreal.objects.get(pk=pk) 
    
    if request.method == "POST":
        # 2. Tangkap isian form baru, TAPI BERITAHU DJANGO INI DATA LAMA (instance=obj)
        # INI PERBAIKAN DARI ERROR DI MODULMU!
        form = DreamrealForm(request.POST, instance=obj)
        
        if form.is_valid():
            form.save()
            return HttpResponse("<h2 align='center'>Record Updated Successfully! 🎉</h2>")
            
    else:
        # 3. Kalau baru buka halaman, tampilkan form yang SUDAH TERISI data lama
        form = DreamrealForm(instance=obj)
        
    context = {"form": form}
    # Kita bisa pakai ulang myform.html yang sama persis seperti materi sebelumnya!
    return render(request, "myform.html", context)


def delete_data(request, pk):
    # 1. Cari data yang mau dihapus berdasarkan ID
    obj = Dreamreal.objects.get(pk=pk) 
    
    # 2. Jika user mengklik tombol "Ya, Hapus" (metode POST)
    if request.method == "POST":
        obj.delete() # Cukup ini saja, jangan pakai obj.save() !!!
        return HttpResponse("<h2 align='center'>Data Berhasil Dihapus Selamanya! 🗑️</h2>")
        
    # 3. Jika user baru nge-klik link (metode GET), tampilkan halaman konfirmasi "Are you sure?"
    context = {"obj": obj}
    return render(request, "delete_confirm.html", context)

def show_cities(request):
    # Membuat daftar (list) nama-nama kota
    cities = ['Mumbai', 'New Delhi', 'Kolkata', 'Bengaluru', 'Chennai', 'Hyderabad', 'Medan', 'Lhokseumawe']
    
    # Membawa data kota tersebut ke file cities.html
    return render(request, "cities.html", {"cities": cities})


# 1. Contoh Redirect Eksternal (ke luar website)
def hello(request):
    return redirect("https://www.youtube.com")

# 2. Halaman Tujuan Internal
def viewArticles(request, year, month):
    text = f"Displaying articles of : {year}/{month}"
    return HttpResponse(text)

# 3. Contoh Redirect Internal (lempar ke viewArticles)
def viewArticle(request, articleId):
    # Mengalihkan menggunakan 'name' dari URL (yaitu 'articles') beserta parameternya
    return redirect('articles', year="2045", month="02")

# 1. Mengirim Email Sederhana
def sendSimpleEmail(request, emailto):
    # Parameter: Subject, Message, From, To_List
    res = send_mail("Test Simple Email", "Halo, ini email uji coba dari Django!", "admin@garudanews.com", [emailto])
    return HttpResponse(f"Status Pengiriman Simple Email: {res} (Cek terminalmu)")

# 2. Mengirim Email Massal ke Admin (Pastikan ADMINS sudah diset di settings.py)
def sendAdminsEmail(request):
    res = mail_admins('Pemberitahuan Sistem', 'Website sedang dalam perbaikan rutin.')
    return HttpResponse(f"Status Pengiriman Admin Email: {res} (Cek terminalmu)")

# 3. Mengirim Email dengan Lampiran (Attachment)
def sendEmailWithAttach(request, emailto):
    # Menggunakan EmailMessage untuk fitur lebih lanjut
    email = EmailMessage("Laporan Mingguan", "Silakan cek file terlampir.", "admin@garudanews.com", [emailto])
    
    # Membaca file yang ada di folder (misal: manage.py) untuk dijadikan lampiran
    try:
        with open('manage.py', 'r') as fd:
            email.attach('manage.py_copy.txt', fd.read(), 'text/plain')
        res = email.send()
        return HttpResponse(f"Status Pengiriman Attachment Email: {res} (Cek terminalmu)")
    except Exception as e:
         return HttpResponse(f"Error membaca file lampiran: {e}")
    

def login(request):
    if request.method == "POST":
        MyLoginForm = LoginForm(request.POST)
        
        if MyLoginForm.is_valid():
            # JIKA SUKSES: Pindah ke halaman hasil
            username = MyLoginForm.cleaned_data['username']
            return render(request, 'loggedin.html', {"username" : username})
        else:
            # JIKA GAGAL: Tetap di halaman form, dan bawa pesan error-nya!
            return render(request, 'login.html', {"form": MyLoginForm})
            
    else:
        # Jika baru pertama kali buka link
        MyLoginForm = LoginForm()
        return render(request, 'login.html', {"form": MyLoginForm})