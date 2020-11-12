from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import (
    User,
    Manager,
    Staff,
    Doctor,
    Patient,
    Medicine,
    MedicalRecord,
    Prescription,
    Appointment,
    Test
)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
                                       'is_superuser', 'groups',
                                       'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(Staff)
admin.site.register(Manager)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Medicine)
admin.site.register(MedicalRecord)
admin.site.register(Prescription)
admin.site.register(Appointment)
admin.site.register(Test)