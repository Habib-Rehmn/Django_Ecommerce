from django import forms
from allauth.account.forms import SignupForm
from .models import CustomUser



class CustomSignupForm1(SignupForm):
    phone_number = forms.CharField(max_length=11 ,required=False) 
    

    def save(self, request):
        # Call the parent class's save to create the user
        user = super(CustomSignupForm1, self).save(request)

        # Now, add your custom fields to the user
        user.phone_number = self.cleaned_data['phone_number']

        # Save the user with the custom fields
        user.save()

        # You must return the original result
        return user


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'address', 'phone_number', 'city', 'province', 'profile_image', 'gender']

    # You can add additional fields or validation as needed.

