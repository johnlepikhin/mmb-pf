# from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import ImageStorage, MMBPFUsers, SystemSettings


class MMBPFUsersForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "password" in self.fields:
            self.fields[
                "password"
            ].help_text = '<h3><a class="h3" href="../password/">Принудительная смена пароля пользователя </a></h3>'

    def clean(self):
        if "groups" in self.cleaned_data and not self.cleaned_data.get("groups"):
            raise forms.ValidationError("Пользователь должен быть включён хотя бы в одну группу")

        return self.cleaned_data

    class Meta(UserChangeForm):
        model = MMBPFUsers
        fields = "__all__"


class MMBPFUsersCreationForm(UserCreationForm):
    def clean(self):
        if "groups" in self.cleaned_data and not self.cleaned_data.get("groups"):
            raise forms.ValidationError("Пользователь должен быть включён хотя бы в одну группу")

        return self.cleaned_data

    class Meta(UserCreationForm):
        model = MMBPFUsers
        fields = "__all__"


class SystemSettingsCreationForm(forms.ModelForm):
    class Meta:
        model = SystemSettings
        fields = "__all__"


class SystemSettingsForm(forms.ModelForm):
    def clean(self):
        return self.cleaned_data

    class Meta:
        model = SystemSettings
        fields = "__all__"


class ImageStorageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImageStorageForm, self).__init__(*args, **kwargs)
        # override default
        if "app_name" in self.fields:
            self.fields["app_name"].initial = "upload_from_admin"

    class Meta:
        model = ImageStorage
        fields = "__all__"
