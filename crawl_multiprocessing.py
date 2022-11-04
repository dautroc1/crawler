

# IMPORT LIB
from lib import *
import multiprocessing
import os
import time
import sys


def crawler_process(process_name, lock, browser_list, crawl_queue, crawled_data, output_container, unique_container):
    # Function: work as an worker in multiprocessed crawling
    # Input:
    #   lock: to acquire and release shared data
    #   browser_list: a shared queue of browser to release when timeout
    #   crawl_queue: a shared queue of "crawl task"
    #   crawled_data: Queue that contain crawled data
    # Output:
    #   crawled_data: contain new crawled data
    
    print("Crawler %s has been started" % process_name)

    browser = BrowserWrapper()
    lock.acquire()
    browser_list.put(browser)
    lock.release()

    a = True
    while a:
    #try:
        while True:
            print("Crawler %s is running" % process_name)
            # get a web config from crawl_queue
            webconfig = None
            lock.acquire()
            if not crawl_queue.empty(): # have more job 
                webconfig = crawl_queue.get()
                lock.release()
                # crawl data
                print("Crawler %s is crawling page %s" % (process_name, webconfig.get_crawl_url()))
                url = webconfig.get_crawl_url()
                html = utils.read_url_source(url, webconfig, browser)
                html_etree = etree.HTML(html)
                title = html_etree.xpath('//title/text()')[0]
                images = html_etree.xpath("//img/@src")
                videos = html_etree.xpath("//video/@src")
                urls = html_etree.xpath("//div//@href")
                for url in urls:
                    if(url not in unique_container):
                        output_container.append(url)
                        unique_container.append(url)
                crawled_data.put({'title': title, 'image':images, 'video':videos})
                
                
            else:
                lock.release()
                #print("Browser is")
                #print(browser)

                if browser is not None:
                    print("Quit browser in Crawler %s" % process_name)
                    browser.quit()
                print("Crawler %s is putting crawled data to main queues" % process_name)
                print("Crawler %s has finished" % process_name)
                return None
        a= False
    #except:
    #    print("There are some error in crawler %s" % process_name)
    #    if browser is not None:
    #        print("Quit browser in Crawler %s" % process_name)
    #        browser.quit()



### Change this !

unique_data = []
crawl_urls = [{'crawl_url':'https://stackoverflow.com/'}, 
             {'crawl_url':'https://www.geeksforgeeks.org/'}, 
             {'crawl_url':'https://gamek.vn/'},
             {'crawl_url':'https://gamek.vn/'},
             {'crawl_url':'https://gamek.vn/'},
             {'crawl_url':'https://gamek.vn/'},
             {'crawl_url':'https://gamek.vn/'},
             {'crawl_url':'https://gamek.vn/'},
             {'crawl_url':'https://gamek.vn/'}]
max_crawler = 9 # number of maximum Firefox browser can be used to crawl. Depend on server resources  
while (len(crawl_urls) > 8):
# Create Manager Proxy to host shared data for multiprocessed crawled
    with multiprocessing.Manager() as manager:

        # share data between processes
        output_container = manager.list()
        #unique_container = manager.list()
        crawl_queue = manager.Queue() 
        crawled_data = manager.Queue()
        new_blacklists = manager.Queue()
        url_links = manager.Queue()
        browser_list = manager.Queue() # keep all firefox browser to release when timeout
        lock = manager.Lock()
        timeout_flag = manager.Value('i', 0) # shared variable to inform processes if timeout happends

        # Init crawl queue
        number_of_job = 0
        for index in range(0, 9):
            webconfig = WebConfig()
            #webconfig.set_webname(crawl_urls[index]['webname'])
            webconfig.set_config('crawl_url', crawl_urls[index]['crawl_url'])
            webconfig.set_config('use_browser', False)
            # set another config here, see crawl_login_page.py for details
            webconfig.set_config('browser_fast_load', True)
            #webconfig.set_config('browser_profile', 'test_profile')
            webconfig.set_config('display_browser', False) #note: display_browser=True won't work in SSH mode
            
            crawl_queue.put(webconfig)
        '''
        for i in unique_data:
            unique_container.append(i)
        '''
        unique_container = manager.list(unique_data)
        crawl_urls = crawl_urls[9:]


        # Start crawl process
        #time.sleep(1)
        print("%s crawlers are set to be run in parallel" % str(max_crawler))
        crawler_processes = []
        #time.sleep(1)
        print("Init %s crawlers" % str(max_crawler))

        start = time.time()

        for i in range(max_crawler):
            crawler = multiprocessing.Process(target=crawler_process, args=(str(i+1), lock, browser_list, crawl_queue, crawled_data,output_container, unique_container))
            crawler_processes.append(crawler)
            crawler.start()
            crawler.join()
            #time.sleep(1)
            print("Start crawler number %s (pid: %s)" % (str(i+1), crawler.pid))


            running = True
            running_crawler = ""
            count = 0

        while running:
            running = False
            count = 0
            running_crawler = ""
            for crawler in crawler_processes:
                count += 1
                if crawler.is_alive():
                    running_crawler = running_crawler + " %s " % str(count)
                    running = True
            print("Running crawler:")
            print(running_crawler)
            time.sleep(2)

        #time.sleep(1)
        print("Finish crawling")
        #time.sleep(1)
        for i in list(set(output_container)):
            crawl_urls.append({'crawl_url':i})
        unique_data = list(unique_container)
        #unique_data = unique_data + unique_container
        #print(output_container)
    	# Print crawled data 
        print("Crawled data")

        while not crawled_data.empty():
            item = crawled_data.get()
            #print("Page: %s" % item['webname'])
            print("Crawled data: %s" % item['title'])
            print(item)
        print(len(crawl_urls))
        print(len(unique_data))

print("FINISH")

