from django.contrib import admin

# Register your models here.
from models import Advices, Questions, Stories

admin.site.register(Questions)
admin.site.register(Stories)
admin.site.register(Advices)
