from django.urls import path,include
from cargo_app import views

urlpatterns = [
    # path('', views.index, name="index"),
    path('', views.PhysicalblotterListView.as_view(), name="pb-list"),
    path("accounts/signup/", views.SignUpView.as_view(), name="sign-up"),
    path("accounts/signin/", views.LoginView.as_view(), name="sign-in"),
    path("accounts/signout/", views.sign_out, name="sign-out"),
    path("users/password/change", views.PasswordResetView.as_view(), name="password-reset"),
    path('add-pb/', views.PhysicalblotterCreateView.as_view(), name="pb-add"),
    # path('pb-list/', views.PhysicalblotterListView.as_view(), name="pb-list"),
    path('pb-details/<str:ID>', views.PbDetailsView.as_view(), name="pb-details"),
    path('pb-edit/<str:ID>', views.PbEditView.as_view(), name="pb-edit"),
    path("remove/<str:ID>", views.remove_pb, name="pb-remove"),
    path("testlist/",views.test_list,name="testlist"),
    path("search/",views.search_items,name ="search"),
    path('export-to-csv/',views.export_to_csv,name = "export"),

]
