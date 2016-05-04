import urllib
import time
import re

from urlparse import urljoin
from bs4 import BeautifulSoup
from time import sleep

# Hardcoding the url for problem statement
url= unicode('https://en.wikipedia.org/wiki/Hugh_of_Saint-Cher')
crawled_links = set() # historic records of url crawled
parent_depth_links = [url] # parent depth links
child_depth_links = [] # Child depth links
key_phrase_list = [] # Only the links Containing the key phrase
count = 2   # Counts the depth of crawl, assuming seed page is depth 1

# soupDefiner uses beautifulsoup library to get the page from the URL

def soupDefiner(url):

    page = urllib.urlopen(url)
    return BeautifulSoup(page.read(),"html.parser")

# Crawls all 1000 unique sites in wikipedia
def crawling_sites(url,count):

    pre_link = unicode("https://en.wikipedia.org") # Pre text for creating proper links
    post_link = ""# Post text got by crawling for creating proper links
    appended_link = unicode("") # Final URL created by adding pre_link and post_link

    # If condition to check if crawled links have totalled 1000, after which the method will stop
    if crawled_links.__len__() < 1000:

        # IF condition to stop any duplicate values in crawled_links
        if parent_depth_links[0] not in crawled_links:
            # crawled_links.append(parent_depth_links[0])
            crawled_links.add(parent_depth_links[0])

        # The below 3 display statements print the current link being crawled,
        # current size of crawled_links and the depth in which we are currently crawling,
        # The size of the child_depth_links and the size of the parent_depth_links
        print "Crawled link:",parent_depth_links[0]
        print "crawled links length:", crawled_links.__len__()," with depth:",count
        print " child length:", child_depth_links.__len__()," parent length:", parent_depth_links.__len__()
        print "starting traversing url: ", url

        # Added a time delay of one second
        # sleep(1)
        #popping out the parent links after they have been crawled
        parent_depth_links.pop(0)

        try:
            soup = soupDefiner(url)

            # If condition to check if depth 5 is reached, else it will crawl the site
            if count > 4 :
                print "depth 5 reached"
            else:
                x =soup.findAll('a',href=True)
                start_loop_time = time.time()   # Start time of the loop which contains all the link
                # for loop to get all the links found in the URL
                for link_followup in x:

                    ## Different condition as per the problem statement and getting valid links
                    if "#" not in unicode(link_followup.get('href')) \
                    and ":" not in unicode(link_followup.get('href')) \
                    and "/wiki/Main_Page" not in unicode(link_followup.get('href'))\
                    and "www." not in unicode(link_followup.get('href'))\
                    and "wikimedia" not in unicode(link_followup.get('href'))\
                    and ".org" not in unicode(link_followup.get('href'))\
                    and "index.php" not in unicode(link_followup.get('href'))\
                    and "None" != unicode(link_followup.get('href'))  :
                        post_link = unicode(link_followup.get('href'))
                        appended_link = pre_link + post_link

                        # Adding the links received in the for loop to child_depth_links list
                        child_depth_links.append(appended_link)
                end_loop_time = time.time() # End time of the for loop

                print "time taken for ending this loop for the url ",url,"  ",end_loop_time-start_loop_time

                # If parent_depth_link is not empty, continue with next  parent link, else copy child_depth_link into parent
                if(parent_depth_links.__len__() != 0 ):
                    appended_link = parent_depth_links[0]
                    crawling_sites(appended_link.encode('utf-8'),count)
                else:
                    print "parent links is 0???"
                    parent_depth_links.extend(list(set(child_depth_links)))
                    print parent_depth_links.__len__(),parent_depth_links
                    del child_depth_links[:] # deletes the child links, to create space for next level
                    appended_link = parent_depth_links[0]
                    crawling_sites(appended_link,count+1)
        except:
            # Try and except handling added for uninterrupted crawling
            print "Error in url",url
            parent_depth_links.pop(0)
            if(parent_depth_links.__len__() != 0 ):
                appended_link = parent_depth_links[0]
                crawling_sites(appended_link.encode('utf-8'),count)
            else:
                print "parent links is 0???"
                parent_depth_links.extend(list(set(child_depth_links)))
                print parent_depth_links.__len__() , parent_depth_links
                del child_depth_links[:]
                appended_link = parent_depth_links[0]
                crawling_sites(appended_link,count+1)


## method for crawling with key phrase
def crawling_sites_with_keyphrase(url,count,keyphrase):

    pre_link = unicode("https://en.wikipedia.org") # Pre text for creating proper links
    post_link = ""# Post text got by crawling for creating proper links
    appended_link = unicode("") # Final URL created by adding pre_link and post_link

    # If condition to search keyphrase by crawling thousand sites.
    # If we need at least 1000 relevant sites(which contain keyphrase) or till depth 5,
    # the below if condition will contain key_phrase_list.__len__() < 1000
    if(crawled_links.__len__() < 1000):

        # crawled_links.append(parent_depth_links[0])
        crawled_links.add(parent_depth_links[0])

        # The below 3 display statements print the current link being crawled,
        # current size of crawled_links and the depth in which we are currently crawling,
        # The size of the child_depth_links and the size of the parent_depth_links
        print "starting traversing url: ", url
        print "crawled links length:", crawled_links.__len__()," with depth:",count
        print " child length:", child_depth_links.__len__()," parent length:", parent_depth_links.__len__()

        # Gives the list of keyphrase collected so far
        print "Keyphrase list length:",key_phrase_list.__len__()

        # Added a time delay of one second
        # sleep(1)

        soup = soupDefiner(url)

        # text_line gets the text body of the page, for searching key phrase
        text_line = soup.body.get_text().encode('utf-8')
        pattern1 = re.compile('.*'+keyphrase+'.*', re.IGNORECASE)

        # Below condition checks if the key phrase is present in the text body
        if keyphrase != "" and pattern1.search(text_line) is None:
            print "Not relevant"
        else:
            if url not in key_phrase_list:
                key_phrase_list.append(url)

        parent_depth_links.pop(0)
        try:

            if count > 4 :
                print "depth 5 reached"
            else:
                x =soup.findAll('a')
                start_loop_time = time.time()

                for link_followup in x:
                    if "#" not in unicode(link_followup.get('href')) \
                    and ":" not in unicode(link_followup.get('href')) \
                    and "/wiki/Main_Page" not in unicode(link_followup.get('href'))\
                    and "www." not in unicode(link_followup.get('href'))\
                    and "wikimedia" not in unicode(link_followup.get('href'))\
                    and ".org" not in unicode(link_followup.get('href'))\
                    and "index.php" not in unicode(link_followup.get('href'))\
                    and "None" != unicode(link_followup.get('href')):
                        post_link = unicode(link_followup.get('href'))
                        appended_link = pre_link + post_link

                        ## Added the condition to avoid adding anymore depth 6 links to child, since they wont be searched
                        if (count+1) > 5:
                            continue

                        child_depth_links.append(appended_link)
                end_loop_time = time.time()
                print "time taken for ending this loop for the url ",url,"  ",end_loop_time-start_loop_time
                if(parent_depth_links.__len__() != 0 ):
                    appended_link = parent_depth_links[0]
                    crawling_sites_with_keyphrase(appended_link.encode('utf-8'),count,keyphrase)
                else:
                    print "parent links is 0???"
                    parent_depth_links.extend(list(set(child_depth_links)))
                    print parent_depth_links.__len__(),parent_depth_links
                    del child_depth_links[:]
                    appended_link = parent_depth_links[0]
                    crawling_sites_with_keyphrase(appended_link,count+1,keyphrase)
        except:
            print "Error found in URL"
            parent_depth_links.pop(0)
            if(parent_depth_links.__len__() != 0 ):
                appended_link = parent_depth_links[0]
                crawling_sites_with_keyphrase(appended_link.encode('utf-8'),count,keyphrase)
            else:
                print "parent links is 0???"
                parent_depth_links.extend(list(set(child_depth_links)))
                print parent_depth_links.__len__(),parent_depth_links
                del child_depth_links[:]
                appended_link = parent_depth_links[0]
                crawling_sites_with_keyphrase(appended_link,count+1,keyphrase)

## Main function which needs to be called for executing the program
def main():

    depth_count = 1
    url= 'https://en.wikipedia.org/wiki/Hugh_of_Saint-Cher'
    url_choice_text = "What wikipedia url do you want to start crawling?" \
                       "\n Press \"1\" if you want to start with the url: "+url+\
                       "\n Press \"2\" if you want some other wikipedia url to start with"

    choice = raw_input("Do you want to crawl with or without keyphrase? \n Press \"1\" for with keyphrase"
                       "\n Press \"2\" for without keyphrase")

    if choice == "1":
        url_choice = raw_input(url_choice_text)
        if url_choice != "1":
            url_name = raw_input("Please enter the correct wikipedia url name you want to start crawling with:\n")
            keyphrase = raw_input("Please enter the keyphrase you want to search in the mentioned link:\n")
            print "entering case 1???"
            start = time.time()
            crawling_sites_with_keyphrase(url_name,depth_count,keyphrase)# User defined url and keyphrase
            end = time.time()
        else:
            keyphrase = raw_input("Please enter the keyphrase you want to search in the mentioned link:\n")
            print "entering case 2"
            start = time.time()
            crawling_sites_with_keyphrase(url,depth_count,keyphrase)# default url and user defined keyphrase
            end = time.time()
        print "Key phrase links: ", key_phrase_list
        print "Total time for crawling with keyphrase", end-start
        fob=open('C:/Python27/Crawled_links_focussed.txt','w')## ** Modify Focussed Path **
        for x in key_phrase_list:
            fob.write(x)
            fob.write("\n")
        fob.close()

    else:
        url_choice2 = raw_input(url_choice_text)
        if url_choice2 == "2":

            url_name = raw_input("Please enter the correct wikipedia url name you want to start crawling with:\n")
            print "entering case 3"
            start = time.time()
            crawling_sites(url_name,depth_count)# User defined url, without keyphrase
            end = time.time()
        else:
            print "entering case 4"
            start = time.time()
            crawling_sites(url,depth_count)# Default url without keyphrase
            end = time.time()

        print crawled_links
        print "crawled_links ",crawled_links.__len__()
        fob=open('C:/Python27/Crawled_links.txt','w') ## ** Modify Unfocussed Path **
        for x in crawled_links:
            fob.write(x)
            fob.write("\n")
        fob.close()

    print "Total time for crawling", end-start

main()