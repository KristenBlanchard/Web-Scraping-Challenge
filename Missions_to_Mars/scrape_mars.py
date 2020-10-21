from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

## initiate browser and path
def initiate_browser():
    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = initiate_browser()

    # Create mars_data dictionary to insert into mongo
    mars_data_dict = {}
    
    # NASA Mars News
    url = ('https://mars.nasa.gov/news/')
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text

    mars_data_dict['news_title'] = news_title
    mars_data_dict['news_p'] = news_p

    # JPL Mars Space Images
    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image = soup.find('img', class_='thumb')['src']
    featured_image_url = 'https://jpl.nasa.gov'+image

    mars_data_dict['featured_image_url'] = featured_image_url

    # Mars Facts
    url_3 = 'https://space-facts.com/mars/'
    browser.visit(url_3)

    read_table = pd.read_html(url_3)
    mars_data_df = pd.DataFrame(read_table[0])
    mars_data_df.columns=['Parameter','Values']
    mars_data_df = mars_data_df.set_index('Parameter')
    mars_table = mars_data_df.to_html(classes='mars_table')
    mars_table = mars_table.replace('\n', ' ')

    mars_data_dict['mars facts'] = mars_table

    # Mars Hemispheres
    url_4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_4)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    core_url = soup.find_all('div', class_='item')
    titles = []
    hemisphere_image_urls = []
    base_url = 'https://astrogeology.usgs.gov'

    for i in core_url:
        title = i.find('h3').text
        url = i.find('a')['href']
        hemi_url = base_url+url

        browser.visit(hemi_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hemi_image_ori = soup.find('div', class_='downloads')
        hem_img_url = hemi_image_ori.find('a')['href']

        print(hem_img_url)
        image_dict_info = dict({'title':title, 'image_url':hem_img_url})
        hemisphere_image_urls.append(image_dict_info)

    mars_data_dict['hemisphere_image'] = hemisphere_image_urls

    browser.quit()
    return mars_data_dict