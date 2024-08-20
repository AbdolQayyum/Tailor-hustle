from django.urls import path
from .views import *
urlpatterns = [
    # path('mail-list/', EmailListView.as_view(), name='mail-list'),
    path('campaign/', BrandCampaignView.as_view(), name='campaign'),
    path('dlelet_campaign/<int:id>/', BrandCampaignDeleteView.as_view(), name='delete_campaign'),
    path('run_campaign/<int:id>/', BrandCampaignRunView.as_view(), name='run_campaign'),
    # path('campaign_rerun/<int:id>/', CampaignRerunidView, name='campaign_rerunid'),
    # path('campaign_delete/<int:id>/', CampaignDeletedView, name='campaign_delete'),
    # path('campaign_rerun/', CampaignRerunView.as_view(), name='campaign_rerun'),
    # path('delete/<int:id>/', EmailDeleteView, name='delete_mail')
]