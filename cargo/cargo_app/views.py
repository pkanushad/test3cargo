from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.contrib import messages

from cargo_app.forms import PhysicalBlotterForm,LoginForm,PasswordResetForm,UserRegistrationForm
from django.views.generic import View,ListView,CreateView,FormView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout


from cargo_app.models import PhysicalBlotter,TraderModel,CounterPartyModel,BookModel,ProductModel,PricingContractModel,UnitModel,HolidayModel,BookModel,PricingMethodeModel,StrategyModel
from django.utils.decorators import method_decorator
# filter and search
from cargo_app.filters import PhysicalBlotterFilter
# pagination
from django.core.paginator import Paginator

import pandas as pd
import numpy as np

import datetime as dt
from datetime import datetime
from django.db.models import Q
import csv

# Create your views here.

# methode decorator
def signin_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            messages.error(request,"you must login")
            return redirect("sign-in")
    return wrapper

#index for testing
def index(request):
    return HttpResponse("hello world")

  # <!-- loginview -->

class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login2.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user= authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)
                print("success")
                return redirect("pb-list")
            else:
                messages.error(request,"invalid credentials")
                return render(request,"login2.html",{"form":form})
        return render(request,"login2.html",{"form":form})

    # <!-- end of loginview -->

# <!-- signup view -->
class SignUpView(CreateView):
    form_class=UserRegistrationForm
    template_name="signup.html"
    model=User
    success_url = reverse_lazy("sign-in")

#  <! ------Password reset view -------!>
@method_decorator(signin_required,name="dispatch")
class PasswordResetView(FormView):
    template_name = "password-reset.html"
    form_class = PasswordResetForm

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            oldpassword=form.cleaned_data.get("old_password")
            password1=form.cleaned_data.get("new_password")
            password2 = form.cleaned_data.get("confirm_password")
            user= authenticate(request,username=request.user.username,password=oldpassword)
            if user:
                user.set_password(password2)
                user.save()
                messages.success(request,"password changed successfully")
                return redirect("sign-in")
            else:
                messages.error(request,"invalid-credentials")
                return render(request,self.template_name,{"form":form})

#  <! ------Passwordreset view end  -------!>

# !--- logout ---!
def sign_out(request,*args,**kwargs):
    logout(request)
    return redirect("sign-in")
# !--- logout  end ---!



#physical blotter start
@method_decorator(signin_required,name="dispatch")
class PhysicalblotterCreateView(View):
    def get(self,request,*args,**kwargs):
        form= PhysicalBlotterForm()
        return render(request, "add-pb2.html", {"form": form})
    def post(self,request,*args,**kwargs):
        form=PhysicalBlotterForm(request.POST,files=request.FILES)
        singapore_holiday = ['2022-10-02', '2022-10-06','2022-12-26','2022-12-12']
        singapore_holi = HolidayModel.objects.values_list('Singapore_Platts')
        ICE = HolidayModel.objects.values_list('ICE')
        print("singapore_holi",singapore_holi)
        print("ICE HOLIDAYS:",ICE)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            date_ = form.cleaned_data.get("Date")
            trader_ = form.cleaned_data.get("Trader")
            # workingdays = np.busday_count(start_date, end_date, holidays=singapore_holiday)+1
            print("startdate:",start_date)
            print("enddate:",end_date)
            workingdays = pd.bdate_range(start=start_date, end=end_date, freq="C", holidays=singapore_holiday)
            workingdays = len(workingdays)
            print("working b4 overwrite:",workingdays)
            pb_id = form.cleaned_data.get('ID')
            # pb_id = int(pb_id)
            print("type of pb:", type(pb_id))
            # print("PB_ID.ID",pb_id.ID)
            # p = int(pb_id.Strategy)
            print("pb_id",pb_id)

            instance = form.save(commit=False)
            instance.Total_no_days = workingdays
            instance.save()

            print("working days ")
            print('+++++++++++++++++++++++++++++++++++++++++')

            range_date = pd.date_range(start_date, end_date)
            # PhysicalBlotter.Total_no_days= workingdays

            print("workingdays", workingdays)
            print(range_date)
            print('+++++++++++++++++++++++++++++++++++++++++')


            print("stat days",start_date)
            print("enddays",end_date)
            print("type startday:",type(start_date))
            print("type endate:",type(end_date))
            print("todays date",date_)
            print("type of todays date",type(date_))

            # <!----- priced and unpriced days start ----!>
            if  date_ <= start_date:
                print("first condition priced days")
                priced_days = 0
                # unpriced_days = np.busday_count(start_date, end_date, holidays=singapore_holiday)+1
                unprice_calcu= pd.bdate_range(start=start_date, end=end_date, freq="C", holidays=singapore_holiday)
                unpriced_days = len(unprice_calcu)
                instance = form.save(commit=False)
                instance.price_days = priced_days
                instance.unprice_days = unpriced_days
                instance.save()
                print("Priced days:", priced_days)
                print("Unpriced Days:", unpriced_days)
                print("first Priced/unpriced days ")
                print('+++++++++++++++++++++++++++++++++++++++++')
                print("ending of 2nd condition price days")
# ---------------------------------------------------------------------------
            elif (date_>start_date) and (date_<=end_date):

                print("2nd pricing days condition")
                unpriced_days = len(pd.bdate_range(start=date_, end=end_date, freq="C", holidays=singapore_holiday))

                workday = len(pd.bdate_range(start=start_date, end=end_date, freq="C", holidays=singapore_holiday))
                priced_days = workday-unpriced_days
                instance = form.save(commit=False)
                instance.price_days = priced_days
                instance.unprice_days = unpriced_days
                instance.save()
                print("second Priced/unpriced days ")
                print('+++++++++++++++++++++++++++++++++++++++++')

            # elif (today > start_date_value) and (today<=end_date_value):


            elif (date_ >end_date):
                print("Hi 3rd priced days CONDITION")
                unpriced_days = 0
                # priced_days = np.busday_count(start_date, end_date, holidays=singapore_holiday)+1
                priced_days = pd.bdate_range(start=start_date, end=end_date, freq="C", holidays=singapore_holiday)
                print(priced_days)
                priced_days = len(priced_days)

                print("priced days:", priced_days)
                print("Unpriced days:", unpriced_days)

                print("Third Priced/unpriced days ")
                print('+++++++++++++++++++++++++++++++++++++++++')

                instance = form.save(commit=False)
                instance.price_days = priced_days
                instance.unprice_days = unpriced_days
                instance.save()

            else:
                pass
                # messages.error(request,"invalid")
                # return redirect("pb-add")

            # <!----- priced unpriced end ---!>

                # <!-----priced volume ----!>
            pricing_methode = form.cleaned_data.get("Pricing_method")
            pricing_methode = str(pricing_methode)
            unit = form.cleaned_data.get("unit")
            print(pricing_methode)
            # if pricing_methode == "fixed":
            #     fixed = form.cleaned_data.get("Pricing_method")
            #     print("test after fixed")
            # elif pricing_methode == "float":
            #     float = form.cleaned_data.get("Pricing_method")
            #     print("test after fixed")

            print("type",type(pricing_methode))
            print(unit)
            unit = str(unit)
            print("type of unit:",type(unit))
            pricing_method = pricing_methode
            pricing_method=pricing_method.strip()
            print("pricing_method:",pricing_method)
            print("dileemas pricng mehtd:",pricing_method)
            if pricing_methode == "fixed":
                print('hi')
                print("startdate:",start_date)
                print("type of startdate:",type(start_date))
                print("enddate:",end_date)
                print("type of enddate:", type(end_date))
                if start_date == end_date:
                    print("hello")
                    if unit== "MT":
                        print("MT")
                        total_volume= form.cleaned_data.get("kMT")
                        priced_volume = total_volume
                        unpriced_volume = 0
                        instance = form.save(commit=False)
                        instance.total_volume = total_volume
                        instance.position = total_volume
                        instance.price_volume = priced_volume
                        instance.unprice_volume = unpriced_volume
                        instance.save()
                        print(" fixed 1st Priced/unpriced volume ")
                        print('+++++++++++++++++++++++++++++++++++++++++')
                    elif unit =="BBL":
                        total_volume = form.cleaned_data.get("kbbl")
                        priced_volume = total_volume
                        unpriced_volume = 0
                        instance = form.save(commit=False)
                        instance.total_volume = total_volume
                        instance.position = total_volume
                        instance.price_volume = priced_volume
                        instance.unprice_volume = unpriced_volume
                        instance.save()
                        print(" fixed 2nd Priced/unpriced volume ")
                        print('+++++++++++++++++++++++++++++++++++++++++')
                    elif unit == "m3":
                        total_volume = form.cleaned_data.get("m3")
                        priced_volume = total_volume
                        unpriced_volume = 0
                        instance = form.save(commit=False)
                        instance.total_volume = total_volume
                        instance.position = total_volume
                        instance.price_volume = priced_volume
                        instance.unprice_volume = unpriced_volume
                        instance.save()
                        print(" fixed 3rd Priced/unpriced volume ")
                        print('+++++++++++++++++++++++++++++++++++++++++')
                    else:
                        pass
                # else:
                #     messages.error(request,"Start and End Date should be same for fixed")
            elif pricing_methode == "float":
                if unit == "MT":
                    total_volume = form.cleaned_data.get("kMT")
                    priced_volume = (total_volume/workingdays)* priced_days
                    print("priced volume:",priced_volume)
                    unpriced_volume = (total_volume/workingdays)* unpriced_days
                    print("unpriced_volume",unpriced_volume)
                    instance = form.save(commit=False)
                    instance.total_volume = total_volume
                    instance.position = total_volume
                    instance.price_volume = priced_volume
                    instance.unprice_volume = unpriced_volume
                    instance.save()
                    print(" float First Priced/unpriced volume ")
                    print('+++++++++++++++++++++++++++++++++++++++++')

                elif unit =="BBL":
                    total_volume = form.cleaned_data.get("kbbl")
                    priced_volume = (total_volume/workingdays)* priced_days
                    print("priced volume:", priced_volume)
                    unpriced_volume = (total_volume / workingdays) * unpriced_days
                    print("unpriced_volume", unpriced_volume)
                    instance = form.save(commit=False)
                    instance.total_volume = total_volume
                    instance.position = total_volume
                    instance.price_volume = priced_volume
                    instance.unprice_volume = unpriced_volume
                    instance.save()
                    print(" float second Priced/unpriced volume ")
                    print('+++++++++++++++++++++++++++++++++++++++++')
                elif unit == "m3":
                    total_volume = form.cleaned_data.get("m3")
                    priced_volume = (total_volume / workingdays) * priced_days
                    print("priced volume:", priced_volume)
                    unpriced_volume = (total_volume / workingdays) * unpriced_days
                    print("unpriced_volume", unpriced_volume)
                    instance = form.save(commit=False)
                    instance.total_volume = total_volume
                    instance.position = total_volume
                    instance.price_volume = priced_volume
                    instance.unprice_volume = unpriced_volume
                    instance.save()
                    print(" float third Priced/unpriced volume ")
                    print('+++++++++++++++++++++++++++++++++++++++++')
                else:
                    messages.error(request, "Please enter values correctly")
                    return redirect("pb-add")

                # <!------priced volume end ---!>
            form.save()
            messages.success(request,"Trade has been added")
            return redirect("pb-list")
        else:
            messages.error(request,"Trade adding failed")
            return render(request, "add-form.html", {"form": form})


@method_decorator(signin_required,name="dispatch")
class PhysicalblotterListView(View):
    def get(self,request,*args,**kwargs):
        if 'q' in request.GET:
            q = request.GET.get('q')
            print(q)
            # qs = PhysicalBlotter.objects.filter(Trader__Trader__icontains=q)
            # print(qs)

            multiple_q = Q(Q(Trader__Trader__icontains=q) | Q(Counter_Party__Counter_Party__icontains=q) |
                           Q(Product__Product__icontains=q) | Q(Pricing_Contract__Pricing_Contract__icontains=q) |
                           Q(unit__unit__icontains=q) | Q(Pricing_method__Pricing_method__icontains=q) |
                           Q(Strategy__Strategy__icontains=q) | Q(BL_Date__icontains=q) |
                           Q(start_date__icontains=q) | Q(end_date__icontains=q) |
                           Q(holidays__icontains=q) | Q(Delivery_mode__icontains=q) |
                           Q(port__icontains=q) | Q(Terminal__icontains=q) |
                           Q(Vessal_name__icontains=q) | Q(Tank_no__icontains=q) |
                           Q(External_Terminal__icontains=q) | Q(Notes__icontains=q) |
                           Q(Status__icontains=q) | Q(Total_no_days__icontains=q)

                           )
            qs = PhysicalBlotter.objects.filter(multiple_q)
            print(qs)
            return render(request, "list-pb.html", {"physicalblotter": qs})
        else:
            # messages.error(request," No information to show")
            redirect("pb-list")

        qs = PhysicalBlotter.objects.all()
        # filter/search
        myFilter = PhysicalBlotterFilter(request.GET, queryset=qs)
        qs = myFilter.qs
        # paginator
        paginator =Paginator(qs,10)
        page_number = request.GET.get('page')
        qs = paginator.get_page(page_number)
        return render(request,"list-pb.html",{"physicalblotter":qs,"myFilter":myFilter})

@method_decorator(signin_required,name="dispatch")
class PbDetailsView(View):
    def get(self,request,*args,**kwargs):
        # print(kwargs)
        qs=PhysicalBlotter.objects.get(ID=kwargs.get("ID"))
        return render(request,"pb-details.html",{"pb":qs})


@method_decorator(signin_required,name="dispatch")
class PbEditView(View):
    def get(self,request,*args,**kwargs):
        ID = kwargs.get("ID")
        product=PhysicalBlotter.objects.get(ID=ID)
        form = PhysicalBlotterForm(instance=product)
        return render(request, "pb-edit.html", {"form": form})
    def post(self,request,*args,**kwargs):
        ID= kwargs.get("ID")
        product=PhysicalBlotter.objects.get(ID=ID)
        form =PhysicalBlotterForm(request.POST,instance=product,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"product has updated")
            return render(request,"list-pb.html",{"form":form})
        else:
            messages.error(request,"product updation failed")
            return render(request,"add-pb.html",{"form":form})

# @method_decorator(signin_required,name="dispatch")
def remove_pb(request,*args,**kwargs):
    ID=kwargs.get("ID")
    product=PhysicalBlotter.objects.get(ID=ID)
    product.delete()
    messages.error(request,"Item has been removed")
    return redirect("pb-list")


def test_list(request):
    return render(request,"tables.html")

def search_items(request):
    return render(request, "list-pb.html")

def export_to_csv(request):
    pb= PhysicalBlotter.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = Physicalblotter_export.csv'
    writer = csv.writer(response)
    writer.writerow(['ID','Date','Trader','Counter_Party','Book',
                    'Strategy','Derivative','Product','Pricing_Contract','unit',
                    'kbbl','kMT','m3','Nominated_quantity','Density','Pricing_method','Premium_discount','BL_Date','Pricing_term','start_date','end_date',
                    'holidays', 'Delivery_mode', 'port', 'Terminal', 'Vessal_name', 'Tank_no','External_Terminal','Terminal_cost','Fright_cost','additional_secondary_charge',
                    'Total_no_days','price_days','unprice_days','total_volume','price_volume','unprice_volume','position','priced_price',
                    'unpriced_price', 'Shore_recieved', 'Difference', 'Notes', 'Status'] )

    pb_fields = pb.values_list(

        'ID', 'Date', 'Trader', 'Counter_Party', 'Book',
        'Strategy', 'Derivative', 'Product', 'Pricing_Contract', 'unit',
        'kbbl', 'kMT', 'm3', 'Nominated_quantity', 'Density', 'Pricing_method', 'Premium_discount', 'BL_Date',
        'Pricing_term', 'start_date', 'end_date',
        'holidays', 'Delivery_mode', 'port', 'Terminal', 'Vessal_name', 'Tank_no', 'External_Terminal', 'Terminal_cost',
        'Fright_cost', 'additional_secondary_charge',
        'Total_no_days', 'price_days', 'unprice_days', 'total_volume', 'price_volume', 'unprice_volume', 'position',
        'priced_price',
        'unpriced_price', 'Shore_recieved', 'Difference', 'Notes', 'Status',)

    for item in pb_fields:
        writer.writerow(item)
    return response












    # str(datetime.datetime.now())+'.csv'
    #


    #
    # pbs= PhysicalBlotter.objects.filter(owner=request.user)
    #
    # for pb in pbs:
    #     writer.writerow('pb.ID','pb.Date','pb.Trader','pb.Counter_Party','pb.Book')
    # return response



