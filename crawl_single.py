header = '''
#####################################################################################################################
#Program: docbao crawler
#Author: hailoc12
#Version: 1.0.0
#Date: 14/06/2019 
#Repository: http://github.com/hailoc12/docbao_crawler
#File: crawl_single_page.py
#Function: demo crawl single page using firefox browser  
#####################################################################################################################
'''

from lib import *



### CHANGE THIS 
url = 'https://careers.coccoc.com/blogs/newsfeed-recommendation-engine-building-up-its-tech-stack-from-scratch' # crawl page

# set crawl configuration 

webconfig = WebConfig() # object contains crawl configuration for a specific website 
browser = BrowserWrapper() # wrapper to get back reference to Firefox browser created in read_url_source function  

# MAIN CALL HERE !!!

# crawl without browser 
print("Demo crawl without browser")
webconfig.set_config('use_browser', False) # Use Firefox browser to crawl or not 

html = read_url_source(url, webconfig, browser)

# extract data 
if html is not None: #crawl ok
    html_tree = etree.HTML(html) #use lxml to parse HTML to element tree
    title = html_tree.xpath("//title/text()")[0] # extract title tag from page html
    print("Title of page %s is: %s" % (url, title))
    images = html_tree.xpath("//img/@src")
    videos = html_tree.xpath("//video/@src")
    print('image')
    for image in images:
        print('image')
        print(image)
    print('image')
    for video in videos:
        print('video')
        print(video)

# crawl with browser  
print("Demo crawl with browser")

webconfig.set_config('use_browser', True) # Use Firefox browser to crawl or not 
webconfig.set_config('browser_fast_load', True) # use adblock extensions, disable css...to load page faster  
webconfig.set_config('display_browser', False) # note: display_browser=True won't work if program is run through SSH 

html = read_url_source(url, webconfig, browser)

# extract data 
if html is not None: #crawl ok
    html_tree = etree.HTML(html) #use lxml to parse HTML to element tree
    title = html_tree.xpath("//title/text()")[0] # extract title tag from page html
    print("Title of page %s is: %s" % (url, title))
    images = html_tree.xpath("//img")
    print('image')
    images = html_tree.xpath("//img/@src")
    videos = html_tree.xpath("//video/@src")
    print('image')
    for image in images:
        print('image')
        print(image)
    print('video')
    for video in videos:
        print('video')
        print(video)
    
    #print("Title of page %s is: %s" % (url, title))


# quit browser to avoid memory leak: IMPORTANT !
browser.quit()
