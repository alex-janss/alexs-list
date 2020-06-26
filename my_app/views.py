from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models


BASE_CRAIGSLIST_URL = 'https://phoenix.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'
# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    # add the searh to the database
    models.Search.objects.create(search=search)
    # format the base url and the search term
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    # get the resulting html page
    data = requests.get(final_url).text
    # create beautifulsoup object to parse html response
    soup = BeautifulSoup(data, features='html.parser')
    # find all <li> tags with class=result-title
    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = [(post.find(class_='result-title').text,
                       post.find('a').get('href'),
                       post.find(class_='result-price').text
                       if post.find(class_='result-price')
                       else 'N/A',
                       BASE_IMAGE_URL.format(
                       post.find(class_='result-image').get('data-ids').split(',')[0][2:])
                       if post.find(class_='result-image').get('data-ids')
                       else 'https://craigslist.org/images/peace.jpg')
                      for post in post_listings]
    for post in final_postings:
        print(post[3])


    context = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', context=context)


