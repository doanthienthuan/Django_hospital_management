from django.urls import path

from . import views

app_name = 'phongkham'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('create-account/', views.create_account, name='create-account'),
    path('create-prescription/', views.create_prescription, name='create-prescription'),
    path('create-appointment/',views.create_appointment, name='create-appointment'),
    path('patients/', views.patient_search, name='patient-list'),
    path('patient/<int:id>', views.PatientDetailView.as_view(), name='patient-detail'),
    path('form/medical-record/', views.create_medical_record, name='medical-record-form'),
    path('staffs/', views.StaffListView.as_view(), name='staff-list'),
    path('staffs/<int:id>', views.StaffDetailView.as_view(), name='staff-detail'),
    path('doctors/', views.DoctorListView.as_view(), name='doctor-list'),
    path('doctors/<int:id>', views.DoctorDetailView.as_view(), name='doctor-detail'),
    path('create-medicine/', views.create_medicine, name='create-medicine'),
    path('medicine/', views.MedicineListView.as_view(), name='medicine-list'),
    path('medicine/<int:id>', views.MedicineDetailView.as_view(), name='medicine-detail'),
    path('medicine/<int:id>/update/',views.MedicineUpdateView.as_view(),name = 'medicine-update'),
    path('appointment/', views.AppointmentListView.as_view(), name='appointment-detail')

]
