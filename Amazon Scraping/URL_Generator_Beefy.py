from bs4 import BeautifulSoup
import requests, time
import sys

# Headers for request
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

# The webpage URL
#URL = 'https://www.amazon.com/Tools-1954889-Fiberglass-General-Purpose/dp/B01HD6N80W/ref=sr_1_3?crid=3746G1GKZGBTI&keywords=hammer&qid=1654616585&sprefix=hammer%2Caps%2C52&sr=8-3'
# breakfast intentional link
#URL = 'https://www.amazon.com/Hamilton-Beach-25475A-Breakfast-Sandwich/dp/B00EI7DPOO/ref=sr_1_1_sspa?keywords=breakfast%2Bsandwich%2Bmaker&qid=1654612462&sprefix=breakfast%2Caps%2C59&sr=8-1-spons&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExVDE2RFJJMzJCNEtFJmVuY3J5cHRlZElkPUExMDQ4MzM0MkVFUUs4T1dXODlBWSZlbmNyeXB0ZWRBZElkPUEwNDQxMzA3MVk3VVdJSDY5S1VRSiZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU&th=1'
# splitter log 4 review page links (small for testing)
#URL = "https://www.amazon.com/SuperHandy-Splitter-Electric-Horizontal-Splitting/dp/B09DFQV9FM/ref=cm_cr_arp_d_product_top?ie=UTF8"
# Random url for testing (blender)
#URL = 'https://www.amazon.com/Vitamix-A3500-Professional-Grade-Container-Stainless/dp/B09TS1KKHV/ref=sr_1_1_sspa?crid=9GZBUFDK1U89&keywords=blender&qid=1655820740&sprefix=blender%2Caps%2C121&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzUEZFWEQxNDhMNUZVJmVuY3J5cHRlZElkPUEwNDUyMTU0RjBWMThLT1VFMjRGJmVuY3J5cHRlZEFkSWQ9QTAwNzcwMDYyMjE2OVlFMkdFSkhIJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=='
# Testing url with 1,800 reviews (Large number of pages) (for debugging generator problems with 10+ review pages)
#URL = 'https://www.amazon.com/Farberware-Dishwasher-Nonstick-Straining-Champagne/dp/B00XADOTDS/ref=sr_1_9?crid=51QFBA2SENEU&keywords=pot&qid=1655824018&sprefix=pot%2Caps%2C259&sr=8-9'

# typically amz.txt, is the /dp/BKJSGOJAIG links in file
with open('C:/Users/fosheejm/Fake-Review-Detection/Amazon Scraping/ProductURLs.txt', 'r') as urllist: 
    # time.sleep(2)
    # url_counter for output parsing
    url_counter = 1
    # for loop per url in amz.txt
    for url in urllist.readlines():
        
        print("\n\nread-in url:", url, " ---- url #: ", url_counter)
        
        # HTTP Request
        webpage = requests.get(url, headers=HEADERS)    
        
        # Soup Object containing all data
        soup = BeautifulSoup(webpage.content, "lxml")

        # review link for span class outer moreso
        Review_Links = soup.find("span", {"class": "cr-widget-FocalReviews"})

        # scraping attempt boolean var
        scraping_success = True

        if Review_Links == None:
            # find href link from entire html
            Review_Links = soup.find("a", {"class":"a-link-emphasis a-text-bold"})

            # if specific scrape for exact part of html doesn't work
            if Review_Links == None:
                # review link outmost dp class (noting dp in link for amz scout)
                Review_Links = soup.find("div", {"id": "dp"})

                # if outermost fails
                if Review_Links == None:
                    print("\n |||||||| THIS LINK FAILED ALL THREE HTML SCRAPING ATTEMPTS ||||||||")
                    scraping_success = False
                else:
                    # review link for span class outer moreso
                    Review_Links = Review_Links.find("span", {"class": "cr-widget-FocalReviews"})
                    # find href link inside scraped outer span html
                    Review_Links = Review_Links.find("a", {"class":"a-link-emphasis a-text-bold"})
        else:
            # find href link inside scraped outer span html
            Review_Links = Review_Links.find("a", {"class":"a-link-emphasis a-text-bold"})
        
        if (Review_Links == None):
            if (scraping_success == True):
                print("\n ------ No reviews exist for this link ----- \n")
                url_counter += 1
                continue
            else:
                print("\n ------ scraping failed grab see-all-reviews portion of html even with same format ------ \n")
                url_counter += 1
                sys.exit()
                continue
        Review_Links = 'https://www.amazon.com'+str(Review_Links).lstrip('[<a data-hook="see-all-reviews-link-foot" class="a-link-emphasis a-text-bold" href="').rstrip('reviewerType=all_reviews">See all reviews</a>').rstrip(';')
        print("\nLink to review page:", Review_Links, "\n")
        # end of amz single product scrape

        # # grabs outer div (class) for url for all-reviews page from product page
        # Review_Links = soup.find("div", {"class":"a-row a-spacing-medium"})
        # # boolean attempt_2 taken
        # attempt_2 = False
        # # check if scraped or not
        # if Review_Links == None:
        #     print("\tCouldn't scrape see-all-reviews on product page; class div DNE -- attempt 1")
        #     # attempt 2 scraping outer div
        #     Review_Links = soup.find("a", {"data-hook":"see-all-reviews-link-foot"})
        #     attempt_2 = True

        # if Review_Links == None:
        #     print("\tCouldn't scrape see-all-reviews on product page; class div DNE -- attempt 2")
        # else: 
        #     # grabs hyperlink for see-all-reviews page from class div previously scraped
        #     if (not(attempt_2)):
        #         Review_Links = Review_Links.find("a", {"data-hook":"see-all-reviews-link-foot"})
        #     # check if scraped or not
        #     if (Review_Links == None and not(attempt_2) == True):
        #         print("Couldn't scrape hyperlink from scraped class div")
        #     elif (Review_Links == None and attempt_2 == False):
        #         print("Couldn't scrape hyperlink from attempt 2")

        # populate urls.txt with all-review pages (org + next-page links)
        grabbed_all_reviews = False
        # open urls.txt in write
        # usually is urls.txt below fyi
        file = open("C:/Users/fosheejm/Fake-Review-Detection/Amazon Scraping/ReviewPageURLs.txt", 'a')
        # write original url to opened file
        file.write(Review_Links + "\n")
        # counter for stripped url_links verified page numbers
        counter = 2
        # loop through all pages & extract next-page links / append to urls.txt
        while(not grabbed_all_reviews):
            # create webpage & soup on current review-page
            webpage = requests.get(Review_Links, headers=HEADERS)
            soup = BeautifulSoup(webpage.content, "lxml")

            # grab url for next page
            Review_Links = soup.find("li", {"class", "a-last"})
            # reconstruct amazon.com url & strip extra content
            Review_Links = 'https://www.amazon.com'+str(Review_Links).lstrip('<li class="a-last"><a href="').rstrip('">Next page<span class="a-letter-space"></span><span class="a-letter-space"></span>→</a></li>') # + str(counter)
            # End loop if review_links size == 39; 39 indicates size of a-disabled a-last html code on final page (no future page to scrape)
            try:
                #Changing ; to &
                temp = list(Review_Links)
                temp[len(Review_Links)-13] = '&'
                Review_Links = "".join(temp)
                # differences - next after btm, getr replaces arp
                temp = Review_Links.split("cm_cr_arp_d_paging_btm")
                #To fix links when over 9 pages
                temp[1] = temp[1].replace('&ageNumber', '&pageNumber').replace(';&', '&')
                #To fix links when over 99 pages
                temp[1] = temp[1].replace(';p&geNumber', '&pageNumber')
                # add getr & next after btm
                Review_Links = temp[0] + "cm_cr_getr_d_paging_btm_next" + temp[1]
                # display next_page link if exists
                print("Next Page Link: ", Review_Links, "\n")
                #time.sleep(3)

                # write link to file
                url_to_write = Review_Links + "\n"   # this doesn't work
                file.write(url_to_write)

                # update url page counter
                counter += 1
            except:
                grabbed_all_reviews = True

        # close file buffer
        file.close()
    
        # increment url_counter
        url_counter += 1