from collections import OrderedDict

from django.http import JsonResponse
from django.shortcuts import render
# import schedule as schedule
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models import F
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.views import View
from .forms import *
from .models import *
import time
from django.views.generic import ListView, FormView, TemplateView


# Create your views here.


class BrandCampaignView(View):
    template = 'dashboard/campaign_message.html'

    def get(self, request):
        campaigns = BrandCampaign.objects.filter(brand=request.user).order_by('-id')
        data = {
            'campaigns': campaigns,
            'pageinfo': 'Run New Campaign'
        }
        return render(request, self.template, data)

    def post(self, request):
        if request.method == "POST":
            # try:
            data = OrderedDict()
            title = request.POST.get('title')
            text = request.POST.get('text')

            BrandCampaign.objects.get_or_create(brand=request.user, title=title, text=text)

            return JsonResponse({'message': 'success'})
        else:
            return JsonResponse({'message': 'error'})


class BrandCampaignRunView(View):
    def post(self, request, id):
        campaign = BrandCampaign.objects.get(id=id)
        users = User.objects.filter(email='taimoor@yopmail.com')
        for user in users:
            campaign_email_template_html = 'emails/campaign_email.html'

            sender = '"TailorHustle" <campaign@tailorhustle.com>'
            send_to = [user.email]
            headers = {'Reply-To': 'do-not-reply@tailorhustle.com'}

            mail_subject = f"TailorHustle Campaign Ran By - {campaign.brand.first_name}"

            template_context = {
                'title': campaign.title,
                'description': campaign.text
            }

            html_message = get_template(campaign_email_template_html)
            html_content = html_message.render(template_context)
            email = EmailMultiAlternatives(
                subject=mail_subject, from_email=sender, to=send_to, headers=headers
            )
            email.attach_alternative(html_content, 'text/html')
            email.send()

        return redirect('campaign')


class BrandCampaignDeleteView(View):
    def post(self, request, id):
        BrandCampaign.objects.get(id=id).delete()
        return redirect('campaign')


class UserCampaignView(View):
    template = 'email-list.html'

    def get(self, request):
        user_campaign_list = UserCampaign.objects.filter(campaign__brand=request.user)
        data = {
            'user_campaign_list': user_campaign_list,
            'pageinfo': 'Subscribed Emails List'
        }
        return render(request, self.template, data)
