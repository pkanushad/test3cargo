from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm

from cargo_app.models import PhysicalBlotter,TraderModel,StrategyModel,PricingMethodeModel,HolidayModel,CounterPartyModel,BookModel,ProductModel,PricingContractModel,UnitModel
import datetime as dt
from datetime import datetime, date

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model= User
        fields=["first_name",
                "email",
                "username",
                "password1",
                "password2",
                ]

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput())


class PhysicalBlotterForm(ModelForm):
    class Meta:
        model = PhysicalBlotter
        exclude = ("Difference", "Shore_recieved", "unpriced_price",
                   "priced_price", "position", "unprice_volume",
                   "price_volume", "total_volume", "unprice_days",
                   "price_days", "Total_no_days", "Heading_text",
                   )

        widgets = {
            # 'Date':forms.DateField(widget=forms.DateInput(attrs={'type':'date'})),
            'Date': forms.DateInput(attrs={'class': 'form-control', 'id': 'Date', 'type': 'date'}),
            'Trader': forms.Select(attrs={'class': 'form-control', 'id': 'Trader','label':'Select'}),
            'Counter_Party': forms.Select(attrs={'class': 'form-control', 'id': 'Counter_Party'}),
            'Book': forms.Select(attrs={'class': 'form-control', 'id': 'Book'}),
            'Strategy': forms.Select(attrs={'class': 'form-control', 'id': 'Strategy'}),
            'Derivative': forms.Select(attrs={'class': 'form-control', 'id': 'Derivative'}),
            'Product': forms.Select(attrs={'class': 'form-control', 'id': 'Product'}),
            'Pricing_Contract': forms.Select(attrs={'class': 'form-control', 'id': 'Pricing_Contract'}),
            'unit': forms.Select(attrs={'class': 'form-control', 'id': 'unit'}),
            'kbbl': forms.NumberInput(attrs={'class': 'form-control', 'id': 'kbbl'}),
            'kMT': forms.NumberInput(attrs={'class': 'form-control', 'id': 'kMT'}),
            'm3': forms.NumberInput(attrs={'class': 'form-control', 'id': 'm3'}),
            'Nominated_quantity': forms.TextInput(attrs={'class': 'form-control', 'id': 'Nominated_quantity'}),
            'Density': forms.NumberInput(attrs={'class': 'form-control', 'id': 'Density'}),
            'Pricing_method': forms.Select(attrs={'class': 'form-control', 'id': 'Pricing_method'}),
            'Premium_discount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'Premium_discount'}),
            'BL_Date': forms.DateInput(attrs={'class': 'form-control', 'id': 'BL_Date', 'type': 'date'}),
            'Pricing_term': forms.Select(attrs={'class': 'form-control', 'id': 'Pricing_term'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'start_date', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'end_date', 'type': 'date'}),
            'holidays': forms.Select(attrs={'class': 'form-control', 'id': 'holidays'}),
            'Delivery_mode': forms.Select(attrs={'class': 'form-control', 'id': 'Delivery_mode'}),
            'port': forms.Select(attrs={'class': 'form-control', 'id': 'port'}),
            'Terminal': forms.Select(attrs={'class': 'form-control', 'id': 'Terminal'}),
            'Vessal_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'Vessal_name_textbox'}),
            'Tank_no': forms.Select(attrs={'class': 'form-control', 'id': 'Tank_no'}),
            'External_Terminal': forms.TextInput(attrs={'class': 'form-control', 'id': 'External_Terminal'}),
            'Terminal_cost': forms.NumberInput(attrs={'class': 'form-control', 'id': 'Terminal_cost'}),
            'Fright_cost':forms.NumberInput(attrs={'class': 'form-control', 'id': 'Fright_cost'}),
            'additional_secondary_charge': forms.NumberInput(attrs={'class': 'form-control', 'id': 'additional_secondary_charge'}),
            # 'Heading_text':forms.TextInput(attrs={'class': 'form-control', 'id': 'Heading_text'}),
            # 'Total_no_days':forms.NumberInput(attrs={'class': 'form-control', 'id': 'Total_no_days'}),
            # 'price_days':forms.NumberInput(attrs={'class': 'form-control', 'id': 'price_days'}),
            # 'unprice_days':forms.NumberInput(attrs={'class': 'form-control', 'id': 'unprice_days'}),

            # 'total_volume':forms.NumberInput(attrs={'class': 'form-control', 'id': 'total_volume'}),
            # 'price_volume':forms.NumberInput(attrs={'class': 'form-control', 'id': 'price_volume'}),
            # 'unprice_volume':forms.NumberInput(attrs={'class': 'form-control', 'id': 'unprice_volume'}),
            # 'position':forms.NumberInput(attrs={'class': 'form-control', 'id': 'position'}),

            # 'priced_price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'priced_price'}),
            # 'unpriced_price':forms.NumberInput(attrs={'class': 'form-control', 'id': 'unpriced_price'}),
            # 'Shore_recieved' :forms.NumberInput(attrs={'class': 'form-control', 'id': 'Shore_recieved'}),
            # 'Difference' : forms.NumberInput(attrs={'class': 'form-control', 'id': 'Difference'}),

            'ID':forms.NumberInput(attrs={'class': 'form-control', 'id': 'ID'}),
            # 'Reference_no': forms.TextInput(attrs={'class': 'form-control', 'id': 'Reference_no'}),

            'Status':forms.Select(attrs={'class': 'form-control', 'id': 'Status'}),
            'Notes': forms.Textarea(attrs={'class': 'form-control', 'id': 'Notes', 'row': 2}),
            'Supporting_document': forms.FileInput(attrs={"class": "form-control", 'id': 'Supporting_document'}),

        }

class TraderModelForm(ModelForm):
    class Meta:
        model = TraderModel
        fields = "__all__"

class CounterPartyModelForm(ModelForm):
    class Meta:
        model = CounterPartyModel
        fields = "__all__"

class BookModelForm(ModelForm):
    class Meta:
        model = BookModel
        fields = "__all__"

class ProductModelForm(ModelForm):
    class Meta:
        model = ProductModel
        fields = "__all__"

class PricingContractModelForm(ModelForm):
    class Meta:
        model = PricingContractModel
        fields = "__all__"


class PricingMethodeModelForm(ModelForm):
    class Meta:
        model = PricingMethodeModel
        fields = "__all__"

class StrategyModelForm(ModelForm):
    class Meta:
        model = StrategyModel
        fields = "__all__"

class HolidayModelForm(ModelForm):
    class Meta:
        model = HolidayModel
        fields = "__all__"

class UnitModelForm(ModelForm):
    class Meta:
        model = UnitModel
        fields = "__all__"

class PasswordResetForm(forms.Form):
    old_password=forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField()