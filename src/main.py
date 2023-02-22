import sys,os
sys.path.append('.')
import config 
from fastScrapper import scrape_page_metadata, save_dict_to_json, create_directory
urls = config.urls

if __name__ == '__main__':
    scrape = scrape_page_metadata(urls[1])
    directory_path = './data'
    create_directory(directory_path)
    for idx in range(len(urls)):
        scrape = scrape_page_metadata(urls[idx])
        save_dict_to_json(scrape, f'./{directory_path}/data_{idx}.json')