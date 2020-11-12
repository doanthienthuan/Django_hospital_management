import datetime
from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import (
    User,
    Patient,
    MedicalRecord,
    Medicine,
    Appointment,
    Test,
    Prescription
)


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth',
                  'address', 'phone_number','BHYT']


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'doctor', 'exam_date',
                  'disease_info', 'treatment_info','test_info', 'fee']
    exam_date = forms.DateField(initial=datetime.date.today, disabled = True)
    fee = forms.IntegerField(disabled = True, initial = 0)
    test_info = forms.ModelMultipleChoiceField(queryset=Test.objects.all(),widget=forms.CheckboxSelectMultiple)

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'category', 'quantity',
                  'date_added', 'expiration','price']


class ApppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['booked']

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medical_record', 'medication', 'dosage',
                  'frequency', 'directions','comments','fee']
    dosage = forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'Số lượng thuốc thứ nhất / Số lượng thuốc thứ 2 / ...'}))
    medication = forms.ModelMultipleChoiceField(queryset=Medicine.objects.all(),widget=forms.CheckboxSelectMultiple)
    fee = forms.IntegerField(disabled = True, initial = 0)

            