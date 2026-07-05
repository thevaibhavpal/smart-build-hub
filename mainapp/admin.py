from django.contrib import admin
from mainapp.models import userinfo
from.models import Enquiry,loginInfo
# Register your models here.
admin.site.register(Enquiry)
admin.site.register(loginInfo)
admin.site.register(userinfo)