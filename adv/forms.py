from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from adv.models import (
    SCHOOL_CLASS,
    Student,
    SchoolSubject,
    GRADES,
    Message,
    StudentNotice,
)
from adv.validators import validate_range, validate_username


class SearchStudentForm(forms.Form):
    last_name = forms.CharField(max_length=100, required=False)


class AddStudentForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=200, widget=forms.Textarea)
    school_class = forms.ChoiceField(choices=SCHOOL_CLASS, widget=forms.RadioSelect)
    year_of_birth = forms.IntegerField(validators=[validate_range(1975, 2010)])


class AddGradeForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all())
    subject = forms.ModelChoiceField(queryset=SchoolSubject.objects.all())
    grade = forms.ChoiceField(choices=GRADES)


class PresenceListForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all())
    day = forms.DateField(widget=forms.HiddenInput)
    present = forms.NullBooleanField()


class SchoolSubjectForm(forms.ModelForm):
    class Meta:
        model = SchoolSubject
        fields = '__all__'


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ['date_sent']


class StudentNoticeForm(forms.ModelForm):
    class Meta:
        model = StudentNotice
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)


class UserCreateForm(forms.Form):
    username = forms.CharField(max_length=128, validators=[validate_username])
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        password2 = cleaned_data['confirm_password']
        if password != password2:
            raise ValidationError('Podane hasła się różnią!')
        return cleaned_data


class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_confirm_password(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        password2 = cleaned_data['confirm_password']
        if password != password2:
            raise ValidationError('Podane hasła się różnią!')
        return cleaned_data