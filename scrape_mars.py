# imports for web browsing and parsing
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd

def scrape():
    TEST = False

    scraped_data = {}

    # Set up browser with chromedriver executable
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    # Visit first scraping target [NASA Mars News] and set up parser
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    browser.find_by_css(".item_list").first.find_by_tag("a").click()

    news_html = browser.html
    soup = BeautifulSoup(news_html, 'html.parser')

    # Collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later
    news_title = soup.find("h1", {"class": "article_title"}).get_text().strip()
    news_paragraph = soup.find("div", {"class": "wysiwyg_content"}).p.get_text()

    # Test results
    if TEST:
        print(news_title)
        print(news_paragraph)

    # Store results in dict
    scraped_data["news_title"] = news_title
    scraped_data["news_paragraph"] = news_paragraph

    # Visit second scraping target [JPL Mars Space Images - Featured Image]
    images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(images_url)
    browser.find_by_id("full_image").click()

    # Button may not load immediately causing an error, loop until it appears
    while browser.is_element_not_present_by_text("more info     ", wait_time=None):
        pass
    browser.find_by_text("more info     ").click()

    # Select full size image in order to obtain url
    browser.find_by_css(".main_image").click()
    featured_image_url = browser.url

    # Test results
    if TEST:
        print(featured_image_url)

    # Store results in dict
    scraped_data["feat_image_url"] = featured_image_url

    # Visit third scraping target [Mars Weather]
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    # Set up parser
    weather_html = browser.html
    soup = BeautifulSoup(weather_html, 'html.parser')

    # Remove child <a> in order to exclude twitter url
    soup.find("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"}).a.extract()

    # Get weather tweet
    mars_weather = soup.find("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"}).get_text()

    # Test results
    if TEST:
        print(mars_weather)

    # Store results in dict
    scraped_data["weather_tweet"] = mars_weather

    # Visit fourth scraping target [Mars Facts]
    facts_url = "https://space-facts.com/mars/"

    # Parse table with pandas.read_html and export table to a html string
    facts_df = pd.read_html(facts_url, attrs={"id": "tablepress-mars"})[0]
    facts_html = facts_df.to_html(index=False)

    # Test results
    if TEST:
        print(facts_html)

    # Store results in dict
    scraped_data["facts_html_table"] = facts_html

    # Visit fifth scraping target [Mars Hemispheres]
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    link_texts = ["Cerberus Hemisphere Enhanced", "Schiaparelli Hemisphere Enhanced", "Syrtis Major Hemisphere Enhanced", "Valles Marineris Hemisphere Enhanced"]
    hemisphere_image_urls = []
    hemisphere_titles = ["Cerberus Hemisphere", "Schiaparelli Hemisphere", "Syrtis Major Hemisphere", "Valles Marineris Hemisphere"]

    for i, link_text in enumerate(link_texts):
        # Visit each hemisphere's page
        browser.visit(hemispheres_url)
        browser.find_by_text(link_text).click()
        
        # Find and extract URL for each full-size image
        hemisphere_html = browser.html
        soup = BeautifulSoup(hemisphere_html, 'html.parser')
        hemisphere_image_urls.append({"title": hemisphere_titles[i], "img_url": soup.find(string="Sample").findParent()["href"]})
        
    # Test results
    if TEST:
        for url in hemisphere_image_urls:
            for key in url:
                print(key, ":", url[key])

    # Store results in dict
    scraped_data["hemisphere_urls"] = hemisphere_image_urls

    return scraped_data
