from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import Card
from .utils import scrape_history_data, save_history_data, validate_input
from django.contrib import messages

class CardAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'description', 'image_url', 'source_url']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('scrape_history_data/', self.admin_site.admin_view(self.scrape_history_data_view), name='scrape_history_data')
        ]
        print(custom_urls + urls)
        return custom_urls + urls


    def scrape_history_data_view(self, request):
        template_path = 'admin/scrape_history_data.html'
        
        if request.method == 'POST':
            title = request.POST.get('title')
            url = request.POST.get('url')
            print(f'Received data: title={title}, url={url}')
            
            validated_title, title_error = validate_input(title)
            validated_url, url_error = validate_input(url)
            
            error_message = title_error or url_error
            if error_message:
                messages.error(request, error_message)
                return render(request, template_path, {'error': error_message})

            data = scrape_history_data(validated_title, validated_url)
            if data:
                save_history_data(data, validated_title, validated_url)
                messages.success(request, "Data scraped and saved successfully")
            else:
                messages.error(request, "Failed to scrape data")
            
            return render(request, template_path)

        return render(request, template_path)

admin.site.register(Card, CardAdmin)
