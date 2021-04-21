from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    #browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    listing = {}

    #Scrap Mars News
    url = "https://redplanetscience.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    #Obtain title and paragraph
    title = soup.find('div', class_='content_title').get_text()
    text = soup.find('div', class_='article_teaser_body').get_text()

    #Scrape JPL Mars Space Images - Featured Image
    space_url = 'https://spaceimages-mars.com/'
    url = space_url + 'image/featured/mars2.jpg'
    browser.visit(space_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #Obtain link
    image = soup.find_all('img')[11]['src']
    featured_image_url = space_url + image

    #Scapre Mars Facts
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    df = tables[1]
    df.columns = ["Facts", "Mars Information"]
    df.set_index('Facts', inplace=True)
    html_table = df.to_html()

    #Scrape Mars Hemispheres
    hemp_url = 'https://marshemispheres.com'
    url = hemp_url + '/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg'
    browser.visit(hemp_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemispheres = soup.find_all('div', class_='item')
    #Loop through each hemisphere pages
    for hemisphere in hemispheres:
        title = hemisphere.find('h3').text
        hemp_titles.append(title)
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        one_url = hemp_url + soup.find('img')['src']
        img_urls.append(one_url)

    # Quit the browser
    browser.quit()

   #Store all values in dictionary
    listing = {
        "title" : title,
        "text" : text,
        "image" : image,
        "featured_image_url" : featured_image_url,
        "mars_fact_table" : html_table, 
        "hemisphere_images" : img_urls
        }

    #Return results
    return listing