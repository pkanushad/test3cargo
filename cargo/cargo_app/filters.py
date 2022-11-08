import django_filters
from django_filters import DateFilter
from .models import *
from django import forms

class PhysicalBlotterFilter(django_filters.FilterSet):
    # start_date = DateFilter(field_name="Date", lookup_expr='gte',label='From')
    # end_date = DateFilter(field_name="Date", lookup_expr='lte',label='To')
    start_date = DateFilter(
        field_name='Date',
        widget=forms.DateInput(attrs={'type': 'date'}),
        lookup_expr='gte', label='From')

    end_date = DateFilter(
        field_name='Date',
        widget=forms.DateInput(attrs={'type': 'date'}),
        lookup_expr='lte', label='To')


    class Meta:
        model = PhysicalBlotter
        fields = ["Trader",
                # "Pricing_Contract",
                # "Vessal_name",
                ]

