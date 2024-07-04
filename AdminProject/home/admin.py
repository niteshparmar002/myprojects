from django.http import HttpResponse
from django.apps import apps
from django.contrib import admin
from django.db.models import CharField, TextField, ForeignKey, BooleanField, ManyToManyField, PositiveBigIntegerField, BigIntegerField, ImageField
from django.contrib.sessions.models import Session
from django.db.migrations.recorder import MigrationRecorder
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from .models import User
import csv

class ListAdminMixin:
    def __init__(self, model, admin_site):
        exclude_fields = {'track', 'utrack', 'locate', 'password', 'id', 'last_login', 'date_joined', 'raw_data'}
        readonly_field = {'id', 'timestamp', 'utimestamp', 'track', 'utrack', 'locate'}
        char_fields = []
        fk_fields = []
        boolean_fields = []
        other_fields = []
        status_fields = []
        search_fields = []
        list_filters = []
        raw_id_fields = []
        readonly_fields = []

        for field in model._meta.fields:
            if field.name in readonly_field:
                readonly_fields.append(field.name)
            if field.name in exclude_fields:
                continue
            
            if isinstance(field, TextField) or isinstance(field, ManyToManyField):
                continue
            
            if isinstance(field, CharField):
                if field.choices:
                    status_fields.append(field.name)
                    list_filters.append(field.name)
                else:
                    method_name = f'get_{field.name}_short'
                    def truncation_method(self, obj, field_name=field.name):
                        value = getattr(obj, field_name)
                        if value and len(value) > 20:
                            return value[:20] + '...'
                        return value
                    truncation_method.short_description = field.verbose_name
                    setattr(self.__class__, method_name, truncation_method)
                    char_fields.append(method_name)
                    search_fields.append(field.name)
            elif isinstance(field, ImageField):
                def image_tag(self, obj, field_name=field.name):
                    image_url = getattr(obj, field_name)
                    if image_url:
                        return mark_safe('<img src="%s" width="100" height="100"/>' % (image_url.url))
                    else:
                        return '-'
                method_name = f'get_{field.name}_short'
                image_tag.short_description = field.verbose_name
                image_tag.allow_tags = True
                setattr(self.__class__, method_name, image_tag)
                char_fields.append(method_name)
            elif isinstance(field, ForeignKey):
                fk_fields.append(field.name)
                search_fields.append(f"{field.name}__id")
                raw_id_fields.append(field.name)
            elif isinstance(field, BooleanField):
                boolean_fields.append(field.name)
                list_filters.append(field.name)
            elif isinstance(field, PositiveBigIntegerField) or isinstance(field, BigIntegerField):
                other_fields.append(field.name)
                search_fields.append(field.name)
            else:
                other_fields.append(field.name)
        
        self.list_display = char_fields + fk_fields + boolean_fields + other_fields + status_fields
        self.search_fields = search_fields
        self.list_filter = list_filters
        self.raw_id_fields = raw_id_fields
        self.readonly_fields = readonly_fields

        if model == Session:
            self.list_display.append('_session_data')
  
        super().__init__(model, admin_site)
    
    def _session_data(self, obj):
        return obj.get_decoded()
    _session_data.short_description = 'Session Data'
    
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response
    export_as_csv.short_description = "Export Selected to CSV"
    
    actions = ['export_as_csv']

class CustomUserAdmin(ListAdminMixin, UserAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

    add_fieldsets = (
        (None, {
            'classes': ('wide', 'extrapretty'),
            'fields': ('first_name', 'last_name', 'email', 'mobile', 'username', 'password1', 'password2', ),
        }),
    )

    fieldsets = [
        ('Personal info', {
            'fields': (
                'referrer', 'service', 'shift', 'mobile', 'phone', 'gender', 'dob', 'father', 'image', 'cover', 'about', 'city', 'zipcode', 'locality', 'address', 'notification', 'otp', 'identifier', 'verified', 'multilogin', 'private', 'lock', 'status'
            ),
        }),
        ('Work info', {
            'fields': (
                'esi', 'pf', 'occupation', 'married', 'exman', 'ex_service', 'hours', 'hourly','rawdata', 'salary', 'rating', 'tagline', 'experience'
            ),
        }),
        ('Social Detail', {
            'classes': ('collapse', ),
            'fields': ('facebook', 'twitter', 'instagram', 'linkedin', 'source'),
        }),
        ('Permissions', {
            'classes': ('collapse', ),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Location', {
            'classes': ('collapse', ),
            'fields': ('latitude', 'longitude'),
        }),
        ('Important dates', {
            'classes': ('collapse', ),
            'fields': ('last_login', 'date_joined'),
        }),
        ('Track Record', {
            'classes': ('collapse', ),
            'fields': ('timestamp', 'utimestamp', 'track', 'utrack', 'locate'),
        }),
    ]


models = apps.get_models()
for model in models:
    if model == User:
        admin_class = CustomUserAdmin
    else:
        admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass

class MigrationRecorderAdmin(ListAdminMixin, admin.ModelAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

admin.site.register(MigrationRecorder.Migration, MigrationRecorderAdmin)
