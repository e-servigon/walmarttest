from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import * 

# Create your views here.
@login_required
def home (request):
    #aqui va un comentario
    return render(request,'home.html',{})

def createuser (request):
    user_form = CreateUserForm()
    user_profile = UserProfileForm()
    contexto = {'user_form': user_form}
    contexto['user_profile_form']=user_profile
    if request.method== 'POST':
        print(request.POST)
        user_form = CreateUserForm(request.POST)
        user_profile=UserProfileForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            user_to_profile = User.objects.get(username=request.POST.get('username'))
            user_extended_data = ExtendedData.objects.create(user=user_to_profile,user_type=request.POST.get('user_type'))
            user_extended_data.save()
            return redirect('login')
    return render(request,'create_user.html',contexto)

def vendor(request):
    vendor_list = Vendor.objects.all()
    vendor_count = Vendor.objects.count()
    vendor_form = CreateVendorForm()
    data_context = {'vendor_list':vendor_list,'vendor_form':vendor_form}
    print("el conteo de proveedors es: ",vendor_count)
    if vendor_count == 0:
        data_context['empty_vendor'] = True
    
    if request.method == "POST":
        print(request.POST)
        vendor_form = CreateVendorForm(request.POST)
        if vendor_form.is_valid():
            try:
                vendor_validate = Vendor.objects.get(vendor_name = request.POST.get('vendor_name'))
                if vendor_validate is not None:
                    data_context['vendor_exist'] = True
            except:
                vendor_form.save()
                return render(request,'vendor.html',data_context)


    return render(request,'vendor.html',data_context)

