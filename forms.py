from django import forms
from .models import PhieuNhap

class PhieuNhapForm(forms.ModelForm):
    class Meta:
        model = PhieuNhap
        fields = ['ma_phieu', 'nguon_nhap', 'ma_nguon', 'sdt', 'dia_chi', 'ly_do', 'tong_tien']
