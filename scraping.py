# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
# Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    data={}
    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)


    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')


    slide_elem = news_soup.select_one('div.list_text')


    slide_elem.find('div', class_='content_title')


    # Use the parent element to find the first a tag and save it as `news_title`
    news_title = slide_elem.find('div', class_='content_title').get_text()
    print("==== News =====")
    print(news_title) 
    print("==========\n ")
    data["news_title"]=news_title
    
    # Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    print("==========")
    print(news_p)
    print("==========\n ")
    data["news_paragraph"]=news_p

    # ### Featured Images
    # 

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')


    # Find the relative image url
    img = img_soup.find('img', class_='fancybox-image').get('src')
   
    img_url_rel = url + "/" + img
    print("==== Image ======")
    print(img_url_rel)
    print("==========\n ")
    data["featured_image"]=img_url_rel

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    img_url

    # # ## Mars Facts

    df = pd.read_html('https://galaxyfacts-mars.com')[0]
    df.head()

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    
    facts = df.to_html()
    print("==========")
    print(facts)
    print("==========\n ")
    data["facts"]=facts

    url = 'https://marshemispheres.com/'    
    browser.visit(url)
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for i in range(4):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[i].click()
        html = browser.html
        hemi_soup = soup(html, "html.parser")
        hemisphere['img_url'] = url + hemi_soup.find("a", text="Sample").get("href")
        hemisphere['title'] = hemi_soup.find("h2", class_="title").get_text()
        hemisphere_image_urls.append(hemisphere)
        browser.back()

    print("==========")
    print(hemisphere_image_urls)
    print("==========\n ")
    data["hemispheres"]=hemisphere_image_urls    

    browser.quit()

    return data

