from django.shortcuts import get_object_or_404, render
from .models import Prescription
import qrcode
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

class Index(View):
    template_name = 'prescriptions.html'
    @method_decorator(login_required(login_url='user:login'))
    def get(self, request):
        user = request.user
        prescriptions = Prescription.objects.filter(user=user).order_by('created')
        context = {'prescriptions': prescriptions}
        return render(request, self.template_name, context)

class Generate_qr(View):
    @method_decorator(login_required(login_url='user:login'))
    def get(self, request, data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        response = HttpResponse(content_type="image/png")
        qr_img.save(response, "PNG")
        return response