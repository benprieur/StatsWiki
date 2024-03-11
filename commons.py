                
import requests
from bs4 import BeautifulSoup


'''
    get_commons_image_url
'''
def get_commons_image_url(commons_url):
    response = requests.get(commons_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    original_file_link = soup.find("a", {"class": "internal"}, href=True, title=True)
    
    if original_file_link and 'href' in original_file_link.attrs:
        image_url =  original_file_link['href']
        return image_url
    else:
        return ''
