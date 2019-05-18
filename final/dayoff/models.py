from django.contrib.auth.models import User
from django.db import models

class Dayoff(models.Model):
    create_by = models.ForeignKey(User,models.CASCADE)
    reason = models.TextField(null=False)
    TYPES = (
        ('PL', 'ลากิจ'),
        ('SL', 'ลาป่วย')
    )
    type = models.CharField(null=False, choices=TYPES, max_length=2, default='PL')
    date_start = models.DateField(null=False)
    date_end = models.DateField(null=False)
    STATUS = (
        ('0', 'ไม่อนุมัติ'),
        ('1', 'อนุมัติ'),
        ('2', 'รอการอนุมัติ')
    )
    approve_status = models.CharField(null=False, choices=STATUS, max_length=1, default='2')
