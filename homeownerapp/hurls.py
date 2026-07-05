from django.urls import path
from . import views

urlpatterns=[
    path('homeownerdash/',views.homeownerdash,name='homeownerdash'),
    path('homeownerlogout/',views.homeownerlogout,name='homeownerlogout'),
    path('homeownerprofile/',views.homeownerprofile,name='homeownerprofile'),
    path('homeowneredit/',views.homeowneredit,name='homeowneredit'),
    path('chpass2/',views.chpass2,name='chpass2'),
    
    path('viewhomeownerproject/',views.viewhomeownerproject,name='viewhomeownerproject'),
    path('addhomeownerproject/',views.addhomeownerproject,name='addhomeownerproject'),
    path('runninghomeownerproject/',views.runninghomeownerproject,name='runninghomeownerproject'),
    path('completehomeownerproject/',views.completehomeownerproject,name='completehomeownerproject'),
    path('homeownerviewapplications/<id>',views.homeownerviewapplications,name='homeownerviewapplications'),
    path('rejectapp/<id>',views.rejectapp,name='rejectapp'),
    path('approveapp/<id>',views.approveapp,name='approveapp'),
    path('viewupdates/<id>',views.viewupdates,name='viewupdates'),
    
    
]