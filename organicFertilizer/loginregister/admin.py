from django.contrib import admin
from .models import Blogs,Newsmodel,Expertsmodel,Fertilizermodel,Company,AppointmentScheduleModel
# Register your models here.
admin.site.register(Blogs)
admin.site.register(Newsmodel)
admin.site.register(Expertsmodel)
admin.site.register(Fertilizermodel)
admin.site.register(Company)
admin.site.register(AppointmentScheduleModel)