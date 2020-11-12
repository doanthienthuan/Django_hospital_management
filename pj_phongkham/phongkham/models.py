from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager
)
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
MAX_LENGTH = 200


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=MAX_LENGTH)
    last_name = models.CharField(max_length=MAX_LENGTH)

    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = models.CharField(max_length=1, choices=GENDERS)

    date_of_birth = models.DateField(null=True)
    address = models.CharField(max_length=MAX_LENGTH)
    phone_number = models.CharField(max_length=12)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ['id','first_name', 'last_name']

    def __str__(self):
        return f'{self.id},{self.last_name}, {self.first_name}'

    def get_name(self):
        return f'{self.last_name} {self.first_name}'
    def get_id(self):
        return f'{self.id}'


class Staff(UserInfo):
    def save(self, *args, **kwargs):
        if self.user.is_staff:
            self.is_staff = True
        if self.user.is_superuser:
            self.is_superuser = True
        super(Staff, self).save(*args, **kwargs)

    position = models.CharField(max_length=MAX_LENGTH)
    date_joined = models.DateField()


class Manager(Staff):
    pass


class Doctor(Staff):
    def save(self, *args, **kwargs):
        self.is_doctor = True
        super(Doctor, self).save(*args, **kwargs)

    department = models.CharField(max_length=MAX_LENGTH)


class Patient(UserInfo):
    Type = (
        ('BHYT', 'BHYT'),
        ('KHONG', 'Không có'),
        ('DICHVU', 'Khám dịch vụ'),

    )
    BHYT = models.CharField(max_length=6, choices=Type, default = 'KHONG')


class Medicine(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    category = models.CharField(max_length=MAX_LENGTH)
    quantity = models.PositiveIntegerField()
    date_added = models.DateField()
    expiration = models.DateField()
    price = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return f'{self.id}. {self.name} | Giá : {self.price}VND | Số lượng hiện có : {self.quantity}' 
    def get_quantity(self):
        return f'{self.quantity}'
    def get_name(self):
        return f'{self.name}'
    def get_id(self):
        return f'{self.id}'
    def get_absolute_url(self):
        return reverse("phongkham:medicine-detail",kwargs = {"id":self.id})

class Test(models.Model):
    name = models.TextField(max_length = MAX_LENGTH)
    price = models.PositiveIntegerField()
    def __str__(self):        
        return f'{self.id}. {self.name} | Giá: {self.price}VND'


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    exam_date = models.DateField()
    disease_info = models.TextField(max_length=MAX_LENGTH, blank=True)
    treatment_info = models.TextField(max_length=MAX_LENGTH, blank=True)
    test_info = models.ManyToManyField(Test)
    fee = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.id} - {self.patient.get_name()} - Ngày khám: {self.exam_date}'


class Prescription(models.Model):
    medical_record = models.ForeignKey(MedicalRecord,
                                       null=True,
                                       on_delete=models.CASCADE)
    medication = models.ManyToManyField(Medicine)
    dosage = models.CharField(max_length=MAX_LENGTH)
    frequency = models.CharField(max_length=MAX_LENGTH)
    directions = models.TextField(max_length=MAX_LENGTH)
    comments = models.TextField(max_length=MAX_LENGTH)
    fee = models.PositiveIntegerField()

    def __str__(self):
        return ', '.join(medicine for medicine in self.medication.all())


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    booked = models.BooleanField(default = False)

    def __str__(self):
        return ' patient: {}'.format(
            self.patient.get_name()
        )

    def get_name(self):
        return f'{self.patient.get_name()}'
