"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import path
from core import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/test/', views.TestEndpoint.as_view(), name='test_endpoint'),
    path('api/randomize/dic/', views.DICRandomizationView.as_view(), name='randomize_dic'),
    path('api/randomize/dbc/', views.DBCRandomizationView.as_view(), name='randomize_dbc'),
    path('api/randomize/factorial-rcbd/', views.FactorialRCBDView.as_view(), name='randomize_factorial_rcbd'),
    path('api/randomize/latinsquare/', views.LatinSquareRandomizationView.as_view(), name='randomize_latinsquare'),
    path('api/randomize/simple-lattice/', views.SimpleLatticeRandomizationView.as_view(), name='randomize_simple_lattice'),
    path('api/randomize/doubled-lattice/', views.DoubledLatticeRandomizationView.as_view(), name='randomize_doubled_lattice'),
    path('api/randomize/alpha-lattice/', views.AlphaLatticeRandomizationView.as_view(), name='randomize_alpha_lattice'),
    path('api/randomize/factorial-crd/', views.FactorialCRDView.as_view(), name='randomize_factorial_crd'),
    path('api/randomize/factorial-axbxc/', views.FactorialAxBCView.as_view(), name='randomize_factorial_axbxc'),
    path('api/randomize/factorial-axbxc-rcbd/', views.FactorialAxBCRCBDView.as_view(), name='randomize_factorial_axbxc_rcbd'),
    path('api/randomize/split-plot-rcbd/', views.SplitPlotRCBDView.as_view(), name='randomize_split_plot_rcbd'),
    path('api/randomize/split-split-plot-rcbd/', views.SplitSplitPlotRCBDView.as_view(), name='randomize_split_split_plot_rcbd'),
    path('api/randomize/split-plot-crd/', views.SplitPlotCRDView.as_view(), name='randomize_split_plot_crd'),
    path('api/randomize/split-split-plot-crd/', views.SplitSplitPlotCRDView.as_view(), name='randomize_split_split_plot_crd'),
    path('api/randomize/augmented-block-java/', views.AugmentedBlockJavaView.as_view(), name='randomize_augmented_block_java'),
    path('api/experiments/', views.ExperimentListCreateView.as_view(), name='experiment-list-create'),
    path('api/experiments/<int:pk>/', views.ExperimentDetailView.as_view(), name='experiment-detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('api/user/', views.UserProfileView.as_view(), name='user-profile'),    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
