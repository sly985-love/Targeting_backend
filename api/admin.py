from django.contrib import admin

# Register your models here.
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin, ExportActionModelAdmin
# from django.contrib import admin
# from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# 在此添加站点
# Register your models here.
admin.site.site_header = '报靶系统管理后台'
admin.site.site_title = '报靶系统管理后台'
admin.site.index_title = '报靶系统管理后台'


class SoldierAdmin(admin.ModelAdmin):
    list_display = ('name', 'army', 'telephone')
    search_fields = ('name', 'army', 'telephone')


admin.site.register(Soldier, SoldierAdmin)


class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'army', 'telephone',)
    search_fields = ('name', 'army', 'telephone',)


admin.site.register(Instructor, InstructorAdmin)


class TargetAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Target, TargetAdmin)


class AchievementAdmin(admin.ModelAdmin):
    list_display = ('score', 'direction', 'creat_dtime')
    # 过滤器（list_filter）显示在列表右侧的过滤器，快捷的过滤方法，一般用作boolean或者有限的值
    list_filter = ('score', 'direction', 'creat_dtime')
    search_fields = ('score', 'direction', 'creat_dtime')
    date_hierarchy = 'creat_dtime'


admin.site.register(Achievement, AchievementAdmin)


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ('name', 'army', 'telephone', 'target', 'is_active', 'is_staff', 'is_superuser', 'last_login',)
    fieldsets = (
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'army', 'telephone', 'password1', 'password2'),
        }),
    )


admin.site.register(User, UserAdmin)

admin.site.register(Photo)


class SelectTargetAdmin(admin.ModelAdmin):
    list_display = ('score', 'direction', 'solider', 'target', 'creat_dtime')


admin.site.register(SelectTarget)


class GoshootingAdmin(admin.ModelAdmin):
    list_display = ('creat_dtime')


admin.site.register(Goshooting)
