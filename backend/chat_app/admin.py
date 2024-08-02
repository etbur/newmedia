from django.contrib import admin

# Register your models here.
from chat_app.models import Profile, Message, Student

admin.site.register(Message)
admin.site.register(Student)
@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ('user', 'photo', 'status', 'online')
