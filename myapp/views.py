from django.http import JsonResponse
from myapp.forms import DreamrealForm
from django_comments.models import Comment
from myapp.models import Dreamreal
from django.views.decorators.cache import cache_page
import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import DreamrealForm
from .models import Dreamreal
from django.core.mail import send_mail, mail_admins, EmailMessage
from myapp.forms import LoginForm
from myapp.forms import ProfileForm
from myapp.models import Profile

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
    username = 'not logged in'
    
    if request.method == 'POST':
        MyLoginForm = LoginForm(request.POST)
        
        if MyLoginForm.is_valid():
            username = MyLoginForm.cleaned_data['username']
            # Menyimpan sesi (session) di server
            request.session['username'] = username
            return render(request, 'loggedin.html', {"username" : username})
        else:
            # Jika form tidak valid, kembali ke halaman login
            return render(request, 'login.html', {"form": MyLoginForm})
            
    # Jika method GET (akses URL langsung)
    MyLoginForm = LoginForm()
    return render(request, 'login.html', {"form": MyLoginForm})

def formView(request):
    # Mengecek apakah user sudah memiliki sesi 'username' yang aktif
    if request.session.has_key('username'):
        username = request.session['username']
        return render(request, 'loggedin.html', {"username" : username})
    else:
        # Jika belum ada sesi, tampilkan form login
        MyLoginForm = LoginForm()
        return render(request, 'login.html', {"form": MyLoginForm})

def logout(request):
    # Menghapus sesi 'username' untuk melakukan logout
    try:
        del request.session['username']
    except KeyError:
        pass
    
    # Menampilkan pesan berhasil logout
    return HttpResponse("<strong>You are logged out.</strong> <br><br> <a href='/connection/'>Kembali ke Login</a>")
    
def SaveProfile(request):
   saved = False
   
   if request.method == "POST":
      # PENTING: Tambahkan request.FILES untuk menangkap file yang diunggah
      MyProfileForm = ProfileForm(request.POST, request.FILES)
      
      if MyProfileForm.is_valid():
         profile = Profile()
         profile.name = MyProfileForm.cleaned_data["name"]
         profile.picture = MyProfileForm.cleaned_data["picture"]
         profile.save()
         saved = True
   else:
      MyProfileForm = ProfileForm()
		
   # Menggunakan locals() untuk mengirim semua variabel lokal (seperti 'saved') ke template
   return render(request, 'saved.html', locals())

# Angka di dalam kurung adalah durasi cache dalam detik (contoh: 30 detik)
@cache_page(30)
def view_caching(request):
    waktu_sekarang = datetime.datetime.now().strftime("%H:%M:%S")
    teks = f"<h2>Halaman ini di-cache!</h2> <p>Waktu saat halaman ini dibuat: <b>{waktu_sekarang}</b></p> <p>Coba refresh browser terus menerus. Waktunya akan membeku selama 30 detik!</p>"
    return HttpResponse(teks)

def hello(request, Name):
    today = datetime.datetime.now().date()
    daysOfWeek = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    # Mengambil data dari database berdasarkan parameter nama di URL
    dreamreal = Dreamreal.objects.get(name=Name)

    return render(request, 'hello.html', locals())

def comment(request, object_pk):
    # Mengambil data komentar berdasarkan ID (Primary Key)
    mycomment = Comment.objects.get(pk=object_pk)
    
    # Menampilkan detail komentar di layar (Menggunakan format string f-string modern)
    text = f"<strong>User :</strong> {mycomment.user_name} <br><br>"
    text += f"<strong>Comment :</strong> {mycomment.comment}"
    
    return HttpResponse(text)

def dreamreal_ajax(request):
    # Jika ada pengiriman data dari AJAX (metode POST)
    if request.method == "POST":
        form = DreamrealForm(request.POST)
        if form.is_valid():
            # Simpan data ke database tabel Dreamreal
            from myapp.models import Dreamreal
            dr = Dreamreal()
            dr.website = form.cleaned_data.get('website')
            dr.name = form.cleaned_data.get('name')
            dr.phonenumber = form.cleaned_data.get('phonenumber')
            dr.save()
            
            # Kembalikan pesan sukses tanpa me-refresh halaman
            pesan = f"Dreamreal Entry {dr.name} was successfully saved."
            return JsonResponse({"status": "success", "message": pesan})
        else:
            return JsonResponse({"status": "error", "errors": form.errors})
            
    # Jika method GET (pertama kali membuka halaman)
    form = DreamrealForm()
    return render(request, 'dreamreal.html', {'form': form})