from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "role", "status", "is_staff", "is_superuser")
    search_fields = ("email",)
    readonly_fields = ("created_at", "last_login")

    def save_model(self, request, obj, form, change):
        """Ensure passwords are hashed when added/edited via admin."""
        if "password" in form.changed_data:
            raw_password = obj.password
            if raw_password and not raw_password.startswith("pbkdf2_"):
                obj.set_password(raw_password)
        super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)
