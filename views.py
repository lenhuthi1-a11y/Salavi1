from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import PhieuNhap, ChiTietPhieuNhap
from .forms import PhieuNhapForm
from django.views.decorators.csrf import csrf_protect

def nhap_kho_view(request):
    # --- Phần tìm kiếm ---
    ma_phieu = request.GET.get('ma_phieu', '')
    nguon_nhap = request.GET.get('nguon_nhap', '')
    nha_cung_cap = request.GET.get('nha_cung_cap', '')
    tu_ngay = request.GET.get('tu_ngay', '')
    den_ngay = request.GET.get('den_ngay', '')

    danh_sach = PhieuNhap.objects.all().order_by('-ngay_nhap')

    if ma_phieu:
        danh_sach = danh_sach.filter(ma_phieu__icontains=ma_phieu)
    if nguon_nhap:
        danh_sach = danh_sach.filter(nguon_nhap__icontains=nguon_nhap)
    if nha_cung_cap:
        danh_sach = danh_sach.filter(nha_cung_cap__icontains=nha_cung_cap)
    if tu_ngay:
        danh_sach = danh_sach.filter(ngay_nhap__gte=tu_ngay)
    if den_ngay:
        danh_sach = danh_sach.filter(ngay_nhap__lte=den_ngay)

    # --- Phần thêm phiếu ---
    if request.method == 'POST':
        form = PhieuNhapForm(request.POST)
        if form.is_valid():
            phieu = form.save(commit=False)
            phieu.ngay_nhap = timezone.now()  # Lưu thời gian hiện tại
            phieu.save()
            # ✅ Sau khi lưu, load lại danh sách mới nhất
            danh_sach = PhieuNhap.objects.all().order_by('-ngay_nhap')
            return render(request, 'nhapkho.html', {
                'form': PhieuNhapForm(),
                'danh_sach': danh_sach,
                'message': 'Lưu phiếu thành công!'
            })
    else:
        form = PhieuNhapForm()

    return render(request, 'nhapkho.html', {
        'form': form,
        'danh_sach': danh_sach,
    })


def xoa_phieu(request, id):
    phieu = get_object_or_404(PhieuNhap, id=id)
    phieu.delete()
    return redirect('nhapkho')


def sua_phieu(request, id):
    # Chừa để làm sau
    return redirect('nhapkho')


from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import PhieuNhap
from .forms import PhieuNhapForm

# 🟢 TẠO PHIẾU NHẬP MỚI
def tao_phieu_nhap_view(request):
    if request.method == 'POST':
        form = PhieuNhapForm(request.POST)
        if form.is_valid():
            phieu = form.save(commit=False)
            phieu.ngay_tao = timezone.now()
            phieu.save()

            # ✅ Lưu danh sách hàng hóa gửi từ form
            ten_hangs = request.POST.getlist('ten_hang')
            ma_hangs = request.POST.getlist('ma_hang')
            don_vis = request.POST.getlist('don_vi')
            don_gias = request.POST.getlist('don_gia')
            so_luongs = request.POST.getlist('so_luong')
            chiet_khaus = request.POST.getlist('chiet_khau')
            thanh_tiens = request.POST.getlist('thanh_tien')

            for i in range(len(ten_hangs)):
                if ten_hangs[i].strip():  # chỉ lưu dòng có tên hàng
                    # 🔧 Xử lý bỏ dấu phẩy trong giá trị số
                    def clean_num(value):
                        if value:
                            return value.replace(',', '')
                        return 0

                    ChiTietPhieuNhap.objects.create(
                        phieu=phieu,
                        ten_hang=ten_hangs[i],
                        ma_hang=ma_hangs[i],
                        don_vi=don_vis[i],
                        don_gia=clean_num(don_gias[i]),
                        so_luong=clean_num(so_luongs[i]),
                        chiet_khau=clean_num(chiet_khaus[i]),
                        thanh_tien=clean_num(thanh_tiens[i])
                    )

            return redirect('nhapkho')  # sau khi lưu thì quay lại danh sách phiếu
    else:
        form = PhieuNhapForm()

    return render(request, 'tao_phieu_nhap.html', {'form': form})


# 🟣 CHI TIẾT / SỬA PHIẾU NHẬP
@csrf_protect
def chi_tiet_phieu_nhap_view(request, id):
    phieu = get_object_or_404(PhieuNhap, id=id)
    if request.method == 'POST':
        form = PhieuNhapForm(request.POST, instance=phieu)
        if form.is_valid():
            form.save()

            ChiTietPhieuNhap.objects.filter(phieu=phieu).delete()  # ✅ sửa dòng này

            # Lưu lại các chi tiết hàng
            ten_hangs = request.POST.getlist('ten_hang')
            ma_hangs = request.POST.getlist('ma_hang')
            don_vis = request.POST.getlist('don_vi')
            don_gias = request.POST.getlist('don_gia')
            so_luongs = request.POST.getlist('so_luong')
            chiet_khaus = request.POST.getlist('chiet_khau')
            thanh_tiens = request.POST.getlist('thanh_tien')

            for i in range(len(ten_hangs)):
                ChiTietPhieuNhap.objects.create(
                    phieu=phieu,  # ✅ đúng tên field
                    ten_hang=ten_hangs[i],
                    ma_hang=ma_hangs[i],
                    don_vi=don_vis[i],
                    don_gia=don_gias[i],
                    so_luong=so_luongs[i],
                    chiet_khau=chiet_khaus[i],
                    thanh_tien=thanh_tiens[i]
                )

            return redirect('nhapkho')
    else:
        form = PhieuNhapForm(instance=phieu)

    return render(request, 'chi_tiet_phieu_nhap.html', {'form': form, 'phieu': phieu})
