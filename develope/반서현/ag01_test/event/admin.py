from django.contrib import admin
from event.models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
  list_display = ['aDate','count']