from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    UpdateView
)
from django.http import HttpResponseRedirect,HttpResponse
from django.db.models import Q

from .models import (
    Patient,
    Staff,
    Doctor,
    Medicine,
    MedicalRecord,
    Appointment,
    Prescription
)
from .forms import (
    UserForm,
    PatientForm,
    MedicalRecordForm,
    MedicineForm,
    ApppointmentForm,
    PrescriptionForm
)

# def get_lasted_patient_id (request):
#     last_patient_list = Patient.objects.order_by('id')[:0]
#     id_ = last_patient_list.get(0).id
#     print(id_)
#     return id_

def create_medical_record(request):
    if request.method == 'POST':
        medical_record_form = MedicalRecordForm(request.POST)

        if medical_record_form.is_valid():
            medical_record = medical_record_form.save(commit=False)
            cleaned_data = medical_record_form.cleaned_data
            medical_record.patient = cleaned_data['patient']
            medical_record.doctor = cleaned_data['doctor']
            medical_record.exam_date = cleaned_data['exam_date']
            medical_record.disease_info = cleaned_data['disease_info']
            medical_record.treatment_info = cleaned_data['treatment_info']
            medical_record.save()
            if(medical_record.patient.BHYT == "KHONG"):
                medical_record.fee = 37800
            if(medical_record.patient.BHYT == "BHYT"):
                medical_record.fee = 7800
            if(medical_record.patient.BHYT == "DICHVU"):
                medical_record.fee = 100000
            phi_kham_benh = medical_record.fee
            phi_xet_nghiem = 0
            for test in cleaned_data['test_info']:
                medical_record.test_info.add(test)
                medical_record.fee += test.price
                phi_xet_nghiem += test.price
            medical_record.save()
            messages.success(request, "Cập nhật hồ sơ bệnh án thành công, Tổng số tiền bạn phải đóng là "+str(medical_record.fee)+" bao gồm phí khám bệnh là "+str(phi_kham_benh)+" và phí xét nghiệm là "+str(phi_xet_nghiem))
            return redirect("phongkham:home")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        medical_record_form = MedicalRecordForm()

    return render(request, 'phongkham/medical_record_form.html', context={
        'medical_record_form': medical_record_form,
    })


def create_account(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        patient_form = PatientForm(request.POST)

        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save(commit=False)
            cleaned_data = patient_form.cleaned_data
            user.first_name = cleaned_data.get('first_name')
            user.last_name = cleaned_data.get('last_name')
            BHYT = cleaned_data.get('BHYT')
            user = user_form.save()
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.BHYT = BHYT
            patient.save()
            messages.success(request, "Account was created successfully!, Your ID is "+str(patient.id)+" please remember this !!")
            return redirect("phongkham:home")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        user_form = UserForm()
        patient_form = PatientForm()

    return render(request, 'phongkham/create_account.html', context={
        'user_form': user_form,
        'patient_form': patient_form
    })

def create_medicine(request):
    if request.method == 'POST':
        medicine_form = MedicineForm(request.POST)

        if medicine_form.is_valid():
            medicine = medicine_form.save(commit=False)
            cleaned_data = medicine_form.cleaned_data
            medicine.name = cleaned_data.get('name')
            medicine.category = cleaned_data.get('category')
            medicine.quantity = cleaned_data.get('quantity')
            medicine.date_added = cleaned_data.get('date_added')
            medicine.expiration = cleaned_data.get('expiration')
            medicine.save()
            messages.success(request, "Tạo thuốc mới thành công!")
            return redirect("phongkham:medicine-list")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        medicine_form = MedicineForm()

    return render(request, 'phongkham/create_medicine.html', context={
        'medicine_form': medicine_form,
    })

def create_prescription(request):
    if request.method == 'POST':
        prescription_form = PrescriptionForm(request.POST)

        if prescription_form.is_valid():
            prescription = prescription_form.save(commit=False)
            cleaned_data = prescription_form.cleaned_data
            prescription.medical_record = cleaned_data.get('medical_record')
            prescription.dosage = cleaned_data.get('dosage')
            amount = prescription.dosage.split("/")
            prescription.frequency = cleaned_data.get('frequency')
            prescription.directions = cleaned_data.get('directions')
            prescription.comments = cleaned_data.get('comments')
            prescription.save()
            for medicine in cleaned_data['medication']:
                matching_medicine = Medicine.objects.get(id = medicine.id)
                if(matching_medicine.quantity == 0):
                    messages.success(request,"Thuốc "+str(matching_medicine.get_name())+" hiện đã hết")
                    return redirect("phongkham:create-prescription")
                    break
                else:
                    matching_medicine.quantity -= int(amount[0])
                    matching_medicine.save()
                    prescription.fee += medicine.price * int(amount[0])
                    amount.pop(0)
            messages.success(request, "Tổng số tiền bạn phải thanh toán là "+str(prescription.fee)+" VND")
            return redirect("phongkham:home")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        prescription_form = PrescriptionForm()

    return render(request, 'phongkham/create_prescription.html', context={
        'prescription_form': prescription_form,
    })


def create_appointment(request):
    user = request.user
    mapping_patient = Patient.objects.filter(user = user)
    patient = mapping_patient[0]
    matching_appointment = Appointment.objects.filter(patient = patient)
    if(len(matching_appointment) != 0):
        stt = matching_appointment[0].id
        messages.success(request, "Bạn đã đặt lịch hẹn hôm nay rồi , giới hạn 1 lịch hẹn cho 1 ngày , STT của bạn là "+str(stt))
        return redirect("phongkham:home")
    else:
        if request.method == 'POST':
            appointment_form =  ApppointmentForm(request.POST)
            if appointment_form.is_valid():
                appointment = appointment_form.save(commit=False)
                cleaned_data = appointment_form.cleaned_data
                appointment.patient = patient
                appointment.booked = True
                appointment.save()
                messages.success(request, "Lịch hen đã được đặt thành công! Số thứ tự của bạn là "+str(appointment.id)+".Hãy chụp lại màn hình")
                return redirect("phongkham:home")
            else:
                messages.error(request, "Please correct the error below.")
        else:
            appointment_form = ApppointmentForm()

        return render(request, 'phongkham/create_appointment.html', context={
            'patient' : patient,
            'appointment_form': appointment_form,
        })

class HomeView(TemplateView):
    template_name = 'phongkham/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Phòng Khám Đa Khoa'
        if self.request.user.is_active and self.request.user.is_superuser == False:
            user = self.request.user
            patient = Patient.objects.filter(user = user)
            context['id_patient'] = patient[0].id
        return context



class PatientListView(ListView):
    paginate_by = 20
    template_name = 'phongkham/patient_list.html'
    context_object_name = 'patients'
    queryset = Patient.objects.all()


class PatientDetailView(DetailView):
    template_name = 'phongkham/patient_detail.html'
    context_object_name = 'patient'

    def get_object(self):
        return get_object_or_404(Patient, pk=self.kwargs.get('id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.get_object()

        matching_medical_records = MedicalRecord.objects.filter(
            patient__id=patient.id)
        context['matching_medical_records'] = matching_medical_records
        return context


def patient_search(request):
    template_name = 'phongkham/patient_list.html'

    if 'q' in request.GET and request.GET.get('q') != '':
        query = request.GET.get('q')
        search_key = query
        matching_patients = Patient.objects.filter(
            Q(id__icontains=query , ) ).distinct()
        context = {
            'search_key': search_key,
            'matching_patients': matching_patients
        }
        return render(request, template_name, context)

    return render(request, template_name)
# hereere
# stating from here
class MedicineListView(ListView):
    template_name = 'phongkham/medicine_list.html'
    queryset = Medicine.objects.all()


class MedicineDetailView(DetailView):
    template_name = 'phongkham/medicine_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Medicine,id = id_)

class MedicineUpdateView(UpdateView):
    template_name = 'phongkham/medicine_update.html'
    form_class = MedicineForm
    queryset = Medicine.objects.all()

    def form_valid(self,form):
        return super().form_valid(form)
    
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Medicine,id = id_)

class StaffListView(ListView):
    paginate_by = 20
    template_name = 'phongkham/staff_list.html'
    context_object_name = 'staffs'
    queryset = Staff.objects.all()


class StaffDetailView(DetailView):
    template_name = 'phongkham/staff_detail.html'
    context_object_name = 'staff'

    def get_object(self):
        return get_object_or_404(Staff, pk=self.kwargs.get('id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = self.get_object()

        matching_medical_records = MedicalRecord.objects.filter(
            doctor__id=staff.id)
        context['matching_medical_records'] = matching_medical_records
        return context


class DoctorListView(ListView):
    paginate_by = 20
    template_name = 'phongkham/doctor_list.html'
    context_object_name = 'doctors'
    queryset = Doctor.objects.all()


class AppointmentListView(ListView):
    paginate_by = 20
    template_name = 'phongkham/appointment_list.html'
    context_object_name = 'appointment'
    queryset = Appointment.objects.all()


class DoctorDetailView(DetailView):
    template_name = 'phongkham/doctor_detail.html'
    context_object_name = 'doctor'

    def get_object(self):
        return get_object_or_404(Doctor, pk=self.kwargs.get('id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.get_object()

        matching_medical_records = MedicalRecord.objects.filter(
            doctor__id=doctor.id)
        context['matching_medical_records'] = matching_medical_records
        return context

