from django.urls import path
from . import views
urlpatterns = [
    path('admindash/',views.admindash,name='admindash'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
    path('viewenq/',views.viewenq,name='viewenq'),
    path('delenq/<id>',views.delenq,name='delenq'),
    path('chpass/',views.chpass,name='chpass'),
    path('managecontractors/',views.managecontractors,name='managecontractors'),
    path('managehomeowners/',views.managehomeowners,name='managehomeowners'),
    path('managecontractors/<int:id>/', views.managecontractors, name='managecontractors'),
    path('blockcontractor/<int:id>/', views.blockcontractor, name='blockcontractor'),
    path('unblockcontractor/<int:id>/', views.unblockcontractor, name='unblockcontractor'),
    path('blockhomeowner/<int:id>/', views.blockhomeowner, name='blockhomeowner'),
    path('unblockhomeowner/<int:id>/', views.unblockhomeowner, name='unblockhomeowner'),


]