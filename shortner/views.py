from django.shortcuts import render
from django.views import View
import requests
from django.conf import settings

# Bitly API access token
BITLY_ACCESS_TOKEN = settings.BITLY_ACCESS_TOKEN

# Home Page
class IndexView(View):
    template_name = 'shortner/index.html'

    def get(self, request):
        # Render the index template without any context
        # This will display the form for URL input
        return render(request, self.template_name)
    
    def post(self, request):
        # Get the URL from the form input
        long_url = request.POST.get('urlInput')
        
        # Call the function to shorten the URL
        shortened_url = shorten_url(long_url)
        
        # Create a context dictionary to pass to the template
        if shortened_url.startswith('Error'):
            # If there was an error shortening the URL, handle it accordingly
            context = {
                'error': shortened_url
            }
            return render(request, self.template_name, context)
        context = {
            'shortened_url': shortened_url
        }

        # Render the template with the context
        return render(request, self.template_name, context)


# Method to shorten the URL using Bitly API
def shorten_url(long_url):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    
    headers = {
        'Authorization': f'Bearer {BITLY_ACCESS_TOKEN}',
    }

    data = {
        'long_url': long_url
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['link']
    else:
        return 'Error shortening URL'