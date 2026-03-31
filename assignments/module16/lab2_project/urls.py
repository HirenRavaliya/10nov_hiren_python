from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('admin/', admin.site.urls),
    path('q5/', TemplateView.as_view(template_name='theory/q5_venv.html'), name='q5_venv'),
    path('q17/', TemplateView.as_view(template_name='theory/q17_github.html'), name='q17_github'),
    path('q1/', include('q1_html.urls')),
    path('q2/', include('q2_css.urls')),
    path('q3/', include('q3_js_val.urls')),
    path('q4/', include('q4_intro.urls')),
    path('q6/', include('q6_doctor.urls')),
    path('q7/', include('q7_mvt.urls')),
    path('q8/', include('q8_admin.urls')),
    path('q9/', include('q9_urls.urls')),
    path('q10/', include('q10_js_reg.urls')),
    path('q11/', include('q11_db.urls')),
    path('q12/', include('q12_orm.urls')),
    path('q13/', include('q13_auth.urls')),
    path('q14/', include('q14_ajax.urls')),
    path('q15/', include('q15_custom_admin.urls')),
    path('q16/', include('q16_payment.urls')),
    path('q19/', include('q19.urls')),
    path('q20/', include('q20_gmaps.urls')),
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)