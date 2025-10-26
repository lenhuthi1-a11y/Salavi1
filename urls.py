from django.urls import path
from . import views

urlpatterns = [
    path('nhapkho/', views.nhap_kho_view, name='nhapkho'),
    path('xoa-phieu/<int:id>/', views.xoa_phieu, name='xoa_phieu'),
    path('chi-tiet-phieu-nhap/<int:id>/', views.chi_tiet_phieu_nhap_view, name='chi_tiet_phieu_nhap'),
    path('tao-phieu-nhap/', views.tao_phieu_nhap_view, name='tao_phieu_nhap'),

]
