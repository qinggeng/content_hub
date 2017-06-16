"""fab_ui_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from apps.api_stat.views import ApiOutline, ApiDetail, ApiHistory, ApiSummary, ApiTestCase, ApiTestRound
from apps.reports.views import Chart

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/outline(?P<api>/.*)', ApiOutline.as_view()),
    url(r'^api/detail', ApiDetail.as_view()),
    url(r'^api/summary', ApiSummary.as_view()),
    url(r'^api/(?P<id>[A-Z0-9a-z-]+)/history', ApiHistory.as_view()),
    url(r'^api/(?P<id>[A-Z0-9a-z-]+)/testcases', ApiTestCase.as_view()),
    url(r'^api/test_round/$', ApiTestRound.as_view()),
    url(r'^api/test_round$', ApiTestRound.as_view()),
    url(r'^api/test_round/(?P<id>[A-Z0-9a-z-]+)', ApiTestRound.as_view()),
    url(r'^report/charts', Chart.as_view()),
]
