#admin

from django.contrib import admin
from .models import *

admin.site.register(Category_s)
admin.site.register(Health_Packages)
admin.site.register(Test_s)
# admin.site.register(TestDetail)

