from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields
        # NEXT LINE WAS FOR OPTION WITH EMAIL
        # fields = UserCreationForm.Meta.fields + ("email",)
