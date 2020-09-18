#Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd

def init_browser():
    executable_path = {'executable_path': '/Users/jayde/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)

    # Create Beautiful Soup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the text of the body
    title = soup.title.text.strip()

    #Find the latest news title and paragraph
    news_title = soup.find("div", class_='content_title').text.strip()
    print(news_title)

    news_paragraph = soup.find("div", class_='rollover_description_inner').text.strip()
    print(news_paragraph)

    #Main URL to retrieve feautured image
    url_1 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_1)

    #HTML object
    html = browser.html



    #Use 'Full Image' link on main page to navigate to feautured image's url and then send a mouse click to open medium image
    #medium_image = browser.links.find_by_partial_text('FULL IMAGE').click()


    #Use 'More Info' link on this page to navigate to the large image URL 
    #large_image = browser.links.find_by_partial_text('more info').click()



    #Use browsers current location to get the URL of the image in large size
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('figure', class_='lede')
    #print(results)


    #Grab partial path of image and then connect to complete URL
    partial_image_path = results[0].a['href']
    #print(partial_image_path)
    featured_image_url = 'https://www.jpl.nasa.gov' + partial_image_path
    print(featured_image_url)



    #Scrape the website for space facts and then create html table string using Pandas
    url_2 = 'https://space-facts.com/mars/'
    spacefacts_table = pd.read_html(url_2)
    #spacefacts_table



    spacefacts_df = spacefacts_table[0]
    spacefacts_df.columns=['description', 'value']
    #spacefacts_df



    #Convert dataframe to HTML table 
    #space_html_table = spacefacts_df.to_html()
    #space_html_table


    #Mars Hemispheres
    url_3 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #Retrieve page with requests module
    response = requests.get(url_3)

    #Create Beautiful Soup object
    soup = BeautifulSoup(response.text, 'html.parser')

    #Get names for the hemispheres
    results = soup.find_all('div', class_="description")
    #print(results)

    #List to contain hemisphere names
    hemisphere_names = []

    # Store each name ('h3' tag) // then append to hemisphere names list:
    hemi_1 = results[0].find('h3').text
    hemisphere_names.append(hemi_1)
    hemi_2 = results[1].find('h3').text
    hemisphere_names.append(hemi_2)
    hemi_3 = results[2].find('h3').text
    hemisphere_names.append(hemi_3)
    hemi_4 = results[3].find('h3').text
    hemisphere_names.append(hemi_4)


    print(hemisphere_names)




    #Get thumbnail links and then add them to main URL for full address
    results_2 = soup.find_all('div', class_="item")

    #Thumbnail array
    thumbnail_link = []

    #main url
    main_url = 'https://astrogeology.usgs.gov'

    thumb_1 = main_url + results_2[0].a['href']
    thumbnail_link.append(thumb_1)
    thumb_2 = main_url + results_2[1].a['href']
    thumbnail_link.append(thumb_2)
    thumb_3 = main_url + results_2[2].a['href']
    thumbnail_link.append(thumb_3)
    thumb_4 = main_url + results_2[3].a['href']
    thumbnail_link.append(thumb_4)

    print(thumbnail_link)



    soup_responses = []

    for link in thumbnail_link:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        soup_responses.append(soup)
   

    #Grab path for full size images
    #Create a list to hold full image URLs
    fullsize_image = []

    results_link1 = soup_responses[0].find('div', class_="wide-image-wrapper")
    full_image1 = results_link1.a['href']
    fullsize_image.append(full_image1)
    #print(full_image1)

    results_link2 = soup_responses[1].find('div', class_="wide-image-wrapper")
    full_image2 = results_link2.a['href']
    fullsize_image.append(full_image2)
    #print(full_image2)

    results_link3 = soup_responses[2].find('div', class_="wide-image-wrapper")
    full_image3 = results_link3.a['href']
    fullsize_image.append(full_image3)
    #print(full_image3)

    results_link4 = soup_responses[3].find('div', class_="wide-image-wrapper")
    full_image4 = results_link4.a['href']
    fullsize_image.append(full_image4)
    #print(full_image4)




    print(fullsize_image)




    # Need to zip all the items together to create the dictionary with tuple
    hemispheres_images_zipped = zip(hemisphere_names,fullsize_image)

    mars_hemi_imgs = []

    for title, img in hemispheres_images_zipped:
        
        # Create Dictionary
        results_dict = {}
        
        #Add 'title' key to dictionary:
        results_dict['title'] = title
        
        # Add image's url to dictionary:
        results_dict['img_url'] = img
        
        # Append list with dictionaries
        mars_hemi_imgs.append(results_dict)
        print(mars_hemi_imgs)
    
    
    





