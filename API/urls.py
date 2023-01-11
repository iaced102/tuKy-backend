"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from views.fishPondViews import FishPondRegisterView

from django.urls import path, include
from device.views.fishpond import FishPondRegisterView, FishPondRecordValue, GetFishPondByUser
from device.views.device import DeviceRegisterView, AllDeviceOfFishPond
urlpatterns = [
    path('fishPond/register', FishPondRegisterView.as_view()),
    path('device/device-register', DeviceRegisterView.as_view()),
    path('device/fishpond-get-all-divce', AllDeviceOfFishPond.as_view()),
    path('device/aquatic-information', FishPondRecordValue.as_view()),
    path('device/get-list-device-owner', GetFishPondByUser.as_view())
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
