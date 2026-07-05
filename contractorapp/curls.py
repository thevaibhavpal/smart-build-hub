from django.urls import path
from . import views


urlpatterns=[
    path('contractordash/',views.contractordash,name='contractordash'),
    path('contractorlogout/',views.contractorlogout,name='contractorlogout'),
    path('contractorprofile/',views.contractorprofile,name='contractorprofile'),
    path('contractoredit/',views.contractoredit,name='contractoredit'),
    path('contractorapplications/',views.contractorapplications,name='contractorapplications'),
    path('applyproject/<id>',views.applyproject,name='applyproject'),
    path('contractorviewprojects/',views.contractorviewprojects,name='contractorviewprojects'),
    path('assignedproject/',views.assignedproject,name='assignedproject'),
    path('chpass1/',views.chpass1,name='chpass1'),
    path('addprogress/<id>',views.addprogress,name='addprogress'),
]
