from bs4 import BeautifulSoup
import json
import numpy as np
import requests
from requests.models import MissingSchema
import spacy
from bs4 import BeautifulSoup as soup
import trafilatura
""" basic functions"""
import json
import os
"""Scrape metadata from target URL."""
import requests
from bs4 import BeautifulSoup
import pprint


def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def save_dict_to_json(dict_to_save, file_path):
    with open(file_path, 'w') as outfile:
        json.dump(dict_to_save, outfile)

urls = ['https://www.whitehouse.gov/briefing-room/statements-releases/2023/02/20/statement-from-president-joe-biden-on-travel-to-kyiv-ukraine/',
      'https://www.whitehouse.gov/briefing-room/statements-releases/2023/02/15/fact-sheet-biden-harris-administration-announces-new-standards-and-major-progress-for-a-made-in-america-national-network-of-electric-vehicle-chargers/',
      'https://www.whitehouse.gov/briefing-room/statements-releases/2023/02/14/statement-from-president-joe-biden-on-five-years-since-parkland/',
      'https://www.whitehouse.gov/briefing-room/statements-releases/2023/02/14/statement-from-president-joe-biden-on-100th-judicial-confirmation/',
      'https://www.whitehouse.gov/briefing-room/statements-releases/2023/02/14/statement-from-president-joe-biden-on-january-cpi-report/'     ]

"""Scrape metadata from target URL."""
import requests
from bs4 import BeautifulSoup
import pprint


"""Scrape metadata attributes from a requested URL."""

def get_title(html):
    """Scrape page title."""
    title = None
    if html.title.string:
        title = html.title.string
    elif html.find("meta", property="og:title"):
        description = html.find("meta", property="og:title").get('content')
    elif html.find("meta", property="twitter:title"):
        description = html.find("meta", property="twitter:title").get('content')
    elif html.find("h1"):
        title = html.find("h1").string
    elif html.find_all("h1"):
        title = html.find_all("h1")[0].string
    if title:
        title = title.split('|')[0]
    return title

def get_text(html):
    """Scrape all text from page."""
    text = ""
    for tag in html.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'li']):
        try: 
          if tag.name == "a":
              text += tag.get('href') + "\n"
          elif tag.string:
              text += tag.string.strip() + "\n"
        except:
          pass
    return text.strip() 

def get_description_DEPRECATED(html):
    """Scrape page description."""
    description = None
    if html.find("meta", property="description"):
        description = html.find("meta", property="description").get('content')
    elif html.find("meta", property="og:description"):
        description = html.find("meta", property="og:description").get('content')
    elif html.find("meta", property="twitter:description"):
        description = html.find("meta", property="twitter:description").get('content')
    elif html.find('a'):
        description = html.find("p").contents

    return description


def get_image(html):
    """Scrape share image."""
    image = None
    if html.find("meta", property="image"):
        image = html.find("meta", property="image").get('content')
    elif html.find("meta", property="og:image"):
        image = html.find("meta", property="og:image").get('content')
    elif html.find("meta", property="twitter:image"):
        image = html.find("meta", property="twitter:image").get('content')
    elif html.find_all("img", src=True):
        image = html.find_all("img")
        if image:
            image = html.find_all("img")[0].get('src')
    return image


def get_site_name(html, url):
    """Scrape site name."""
    if html.find("meta", property="og:site_name"):
        sitename = html.find("meta", property="og:site_name").get('content')
    elif html.find("meta", property='twitter:title'):
        sitename = html.find("meta", property="twitter:title").get('content')
    else:
        sitename = url.split('//')[1]
        return sitename.split('/')[0].rsplit('.')[1].capitalize()
    return sitename


def get_favicon(html, url):
    """Scrape favicon."""
    if html.find("link", attrs={"rel": "icon"}):
        favicon = html.find("link", attrs={"rel": "icon"}).get('href')
    elif html.find("link", attrs={"rel": "shortcut icon"}):
        favicon = html.find("link", attrs={"rel": "shortcut icon"}).get('href')
    else:
        favicon = f'{url.rstrip("/")}/favicon.ico'
    return favicon


def get_theme_color(html):
    """Scrape brand color."""
    if html.find("meta", property="theme-color"):
        color = html.find("meta", property="theme-color").get('content')
        return color
    return None


def scrape_page_metadata(url):
    """Scrape target URL for metadata."""
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    pp = pprint.PrettyPrinter(indent=4)
    r = requests.get(url, headers=headers)
    html = BeautifulSoup(r.content, 'html.parser')
    metadata = {
        'title': get_title(html),
        'description': get_text(html),
        'image': get_image(html),
        'favicon': get_favicon(html, url),
        'sitename': get_site_name(html, url),
        'color': get_theme_color(html),
        'url': url
        }
    pp.pprint(metadata)
    return metadata

scrape = scrape_page_metadata(urls[1])
directory_path = './data'
create_directory(directory_path)


for idx in range(len(urls)):
  scrape = scrape_page_metadata(urls[idx])
  save_dict_to_json(scrape, f'./{directory_path}/data_{idx}.json')