from django.contrib import admin
from .models import User, Papers

# Register your models here.

admin.site.register([User, Papers])
