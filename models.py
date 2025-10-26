from django.db import models
from django.utils import timezone

from django.db import models
from django.utils import timezone

class PhieuNhap(models.Model):
    ma_phieu = models.CharField(max_length=50, unique=True)
    nguon_nhap = models.CharField(max_length=100, blank=True, null=True)
    ma_nguon = models.CharField(max_length=50, blank=True, null=True)
    sdt = models.CharField(max_length=20, blank=True, null=True)
    dia_chi = models.CharField(max_length=255, blank=True, null=True)
    ly_do = models.TextField(blank=True, null=True)
    tong_tien = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ngay_nhap = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.ma_phieu

    class Meta:
        ordering = ['-ngay_nhap']  # 👈 Sắp xếp theo ID tăng dần (phiếu mới ở dưới)

# models.py
class ChiTietPhieuNhap(models.Model):
    phieu = models.ForeignKey(PhieuNhap, on_delete=models.CASCADE, related_name='chitiet')
    ten_hang = models.CharField(max_length=100)
    ma_hang = models.CharField(max_length=50)
    don_vi = models.CharField(max_length=20)
    don_gia = models.DecimalField(max_digits=12, decimal_places=2)
    so_luong = models.IntegerField()
    chiet_khau = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    thanh_tien = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.ten_hang} ({self.phieu.ma_phieu})"