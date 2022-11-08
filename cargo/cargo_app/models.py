from django.db import models
from datetime import datetime, date

# Create your models here.

class TraderModel(models.Model):
    Trader = models.CharField(max_length=120, default="Select")
    def __str__(self):
        return self.Trader

class CounterPartyModel(models.Model):
    Counter_Party = models.CharField(max_length=120,)
    def __str__(self):
        return self.Counter_Party

class BookModel(models.Model):
    Book = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.BookModel

class ProductModel(models.Model):
    Product = models.CharField(max_length=100)
    def __str__(self):
        return self.Product

class PricingContractModel(models.Model):
    Pricing_Contract= models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.Pricing_Contract

class UnitModel(models.Model):
    unit = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.unit


class PricingMethodeModel(models.Model):
    Pricing_method = models.CharField(max_length=120)
    def __str__(self):
        return self.Pricing_method

class StrategyModel(models.Model):
    Strategy = models.CharField(max_length=100, primary_key=True, null=False)
    def __str__(self):
        return self.Strategy

class HolidayModel(models.Model):
    Singapore_Platts = models.DateField(default=datetime.now)
    ICE = models.DateField(default= datetime.now)



class BookModel(models.Model):
    Book = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.Book


# main model

class PhysicalBlotter(models.Model):
    ID = models.IntegerField(primary_key=True)
    # Reference_no = models.CharField(primary_key=True,max_length=100)
    Date = models.DateField(default=datetime.now)
    Trader = models.ForeignKey(TraderModel, on_delete=models.CASCADE)
    # COUNTERPARTY_CHOICE = (
    #     ("X", "X"),
    #     ("Y", "Y"),
    #     ("Z", "Z"),
    # )
    Counter_Party = models.ForeignKey(CounterPartyModel,on_delete=models.CASCADE,null=True)
    # BOOK_CHOICE = (
    #     ("Book1", "Book1"),
    #     ("Book2", "Book2"),
    # )
    Book = models.ForeignKey(BookModel,on_delete=models.CASCADE,null=True)
    Strategy = models.ForeignKey(StrategyModel,on_delete=models.CASCADE,null=True)
    DERIVATIVE_CHOICE = (
        ("physical", "physical"),
    )
    Derivative = models.CharField(max_length=100, choices=DERIVATIVE_CHOICE, default="physical")
    # PRODUCT_CHOICE = (
    #     ("Fuel Oil", "Fuel Oil"),
    #     ("Naphtha", "Naphtha"),
    #     ("Gasoline Blend sb", "Gasoline Blend sb")
    # )
    Product = models.ForeignKey(ProductModel,on_delete=models.CASCADE,null=True)
    # PRICINGCONTRACT_CHOICE = (
    #     ("Naphtha FOB Arar", "Naphtha FOB Arar"),
    #     ("ECO-1042/2022", "ECO-1042/2022"),
    #     ("Others", "Others"),
    # )
    Pricing_Contract = models.ForeignKey(PricingContractModel, on_delete=models.CASCADE, null=True)
    # UNIT_CHOICE = (
    #     ("MT", "MT"),
    #     ("BBL", "BBL"),
    #     ("m\u00b3", "m\u00b3"),
    # )
    # unit = models.CharField(max_length=100, choices=UNIT_CHOICE, null=True)
    unit = models.ForeignKey(UnitModel,on_delete=models.CASCADE ,null=True)
    kbbl = models.FloatField(null=True,blank=True)
    kMT = models.FloatField(null=True, blank=True)
    m3 = models.FloatField(null=True, blank=True)
    Nominated_quantity = models.CharField(max_length=100, null=True)
    Density = models.FloatField(null=True)

    Pricing_method = models.ForeignKey(PricingMethodeModel, on_delete=models.CASCADE, null=True)
    Premium_discount = models.FloatField(null=True)
    BL_Date = models.DateField(default=datetime.now, null=True)
    PRICINGTERM_CHOICE = (
        ("Tomorrow", "Tomorrow"),
        ("25 days after", "25 days after"),
    )
    Pricing_term = models.CharField(max_length=100, choices=PRICINGTERM_CHOICE, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    HOLIDAY_CHOICES = (
        ("singapore_holidays", "singapore_holidays"),
        ("plate_holidays", "plate_holidays"),
    )

    holidays = models.CharField(max_length=100, choices=HOLIDAY_CHOICES, null=True)
    DELIVERY_MODE_CHOICES = (
        ("1", "Tank"),
        ("2", "Vessel"),
        ("3", "PLT"),
    )
    Delivery_mode = models.CharField(max_length=100, choices=DELIVERY_MODE_CHOICES, null=True, blank=True)
    PORT_CHOICE = (
        ("Port1", "Port1"),
        ("Port2", "Port2"),
    )
    port = models.CharField(max_length=120, choices=PORT_CHOICE,null=True)
    TERMINAL_CHOICE = (
        ("Terminal1", "Terminal1"),
        ("Terminal2", "Terminal2"),
    )
    Terminal = models.CharField(max_length=120, choices=TERMINAL_CHOICE,null=True)
    Vessal_name = models.CharField(max_length=120, null=True, blank=True)
    TANK_NUM_CHOICE = (
        ("Tank1", "Tank1"),
        ("Tank2", "Tank2"),
        ("Tank3", "Tank3"),
        ("Tank4", "Tank4"),
    )
    Tank_no = models.CharField(max_length=120, choices=TANK_NUM_CHOICE, null=True, blank=True)
    External_Terminal = models.CharField(max_length=120, null=True, blank=True)

    Terminal_cost = models.IntegerField(null=True, blank=True)
    Fright_cost = models.IntegerField(null=True, blank=True)
    additional_secondary_charge = models.IntegerField(null=True, blank=True)
    Total_no_days = models.IntegerField(null=True, blank=True)
    price_days = models.IntegerField(null=True, blank=True)
    unprice_days = models.IntegerField(null=True, blank=True)

    total_volume = models.FloatField(null=True, blank=True)
    price_volume = models.FloatField(null=True, blank=True)
    unprice_volume = models.FloatField(null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)

    priced_price = models.IntegerField(null=True, blank=True)
    unpriced_price = models.IntegerField(null=True, blank=True)
    Shore_recieved = models.IntegerField(null=True, blank=True)
    Difference = models.IntegerField(null=True, blank=True)
    Notes = models.CharField(max_length=250, blank=True, null=True)
    Supporting_document = models.FileField(upload_to="file_uploads/", null=True, blank=True)
    STATUS_CHOICES = (
        ("Open", "Open"),
        ("Closed", "Closed"),
    )
    Status = models.CharField(max_length=120, choices=STATUS_CHOICES, null=True, blank=True, default="Open")

    # def __str__(self):
    #     return self.Trader









