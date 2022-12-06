
# Description: Scrapes Reviews and stores in dataframe, writes to file for model input
# Input: review page urls in txt file, one url per line
# Output: csv of reviews storing a dataframe

# import statements
import requests, time
from time import sleep
from bs4 import BeautifulSoup 
import pandas as pd
import sys

### Getter Functions
# Extracts titles of reviews
def get_review_titles(soup):
    Review_Title = soup.findAll("a", {"class" : "a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold"})
    Name = soup.findAll("div", {"data-hook" : "genome-widget"})
    Title = []
    for i in range(0,len(Name)):
        Title.append(Review_Title[i].get_text())
    # Remove the '\n' from before and after of every Review Title
    Title[:] = [i.lstrip('\n').rstrip('\n') for i in Title]
    return Title  

# Extracts names of reviewers from each review
def get_reviewer_names(soup):
    Name = soup.findAll("div", {"data-hook" : "genome-widget"}) 
    Reviewer = []
    for i in range(2,len(Name)):
        Reviewer.append(Name[i].get_text())
    return Reviewer

# Extracts star rating of each review
def get_review_ratings(soup):
    Star_Rating = soup.findAll("i", {"class" : "review-rating"}) 
    Rating = []
    for i in range(0, len(soup.findAll("div", {"class" : "a-section celwidget"}))):     
        Rating.append(Star_Rating[i].get_text())
    return Rating

    # Extracts whether a review has a verified purchase tag
def get_verified_purchase(soup):
    VP = soup.findAll("span", {"data-hook" : "avp-badge" }) 
    Verified_Purchase = []
    for i in range(0,len(VP)):
        print(VP[i].get_text())
        Verified_Purchase.append(VP[i].get_text())
    return Verified_Purchase

# Extracts body of each review
def get_review_text(soup):
    Review_Text = soup.findAll("span", {"class" : "review-text"})
    Description = []
    for i in range(0,len(Review_Text)):
        Description.append(Review_Text[i].get_text())
    # We will remove the '\n' from before and after of every Review Desciption
    Description[:] = [i.lstrip('\n').rstrip('\n') for i in Description]
    #To remove the images from the scraped text
    Description[:] = [i.replace('The media could not be loaded', '').replace('.\n', '').replace('\n\n\n\n', '') for i in Description]
    #Strips the text of all extra trailing and leading white space
    Description[:] = [i.strip() for i in Description]

    return Description

# Extracts date & country of each review
def get_date_and_country(soup):
    Review_Info = soup.findAll("span", {"data-hook":"review-date"})
    #print('Review Info: ' , Review_Info)
    Country_And_Date = []
    for i in range(0,len(Review_Info)):
        Country_And_Date.append(Review_Info[i].get_text())
    Country_And_Date[:] = [i.lstrip('Reviewed in the ').split(" on ") for i in Country_And_Date]
    Country, Date = map(list, zip(*Country_And_Date))

    return Date, Country

# Extracts product_name of each review
def get_product_name(soup):
    Product = soup.find("title")
    Name = []
    for i in range (0, len(soup.findAll("span", {"class" : "review-text"}))):
        Name.append(Product.get_text())
    Name[:] = [i.lstrip('Amazon.com: Customer reviews: ') for i in Name]
    return Name

# Headers for request library interfacing with browsers
HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})

### Main Code
# input to open statement is txt file with review-page-urls one per line
with open("C:/Users/fosheejm/Fake-Review-Detection/Amazon Scraping/ReviewPageURLs.txt",'r') as urllist:
    
    #create large data frame
    allReviews = pd.DataFrame()
    counter = 1

    # vars for ASIN extraction from url
    substr = "/product-reviews/"
    len_ASIN = len("B09HTZFH4L")

    # iterate over each url & scrape reviews + populate in interior df to concat exterior df
    for url in urllist.readlines():
        #request call for each url in the file
        webpage = requests.get(url.rstrip("\n"), headers=HEADERS)
 
        # Soup Object containing all data
        soup = BeautifulSoup(webpage.content, "lxml")

        # string logic extract ASIN from url to store in reviewData df
        starting_index = url.find(substr) + len(substr)
        ending_index = starting_index + len_ASIN
        ASIN_in_list = [url[starting_index:ending_index]] *10

        #create pandas data frame & assign scrapable data - ASIN & product_name & rating & text
        #reviewData = pd.DataFrame(columns=['Product', 'Reviewer Name', 'Rating', 'Text', 'Date', 'Country','asin', 'Verified_Purchase'])
        reviewData = pd.DataFrame(columns=['Product', 'Reviewer Name', 'Rating', 'Text', 'Date', 'Country','asin'])
        product_name_list = get_product_name(soup)
        product_reviewer_name_list = get_reviewer_names(soup)
        product_rating_list = get_review_ratings(soup)
        product_review_list = get_review_text(soup)
        product_date_country_list = product_date_list, product_country_list = get_date_and_country(soup)
        #product_verified_purchase_list = get_verified_purchase(soup)
        for i in range(len(product_name_list)):
            #list_row = [product_name_list[i], product_reviewer_name_list[i], product_rating_list[i], product_review_list[i], product_date_list[i], product_country_list[i], ASIN_in_list[i], product_verified_purchase_list[i]]
            list_row = [product_name_list[i], product_reviewer_name_list[i], product_rating_list[i], product_review_list[i], product_date_list[i], product_country_list[i], ASIN_in_list[i]]
            reviewData.loc[len(reviewData)] = list_row 


        # display reviews & scraping progress
        print(" ------- url #:", counter, " -------\n")
        if not(reviewData.empty):
            print(reviewData)

            #updated how to join together dataframes due to pandas version update
            reviewData.to_csv("C:/Users/fosheejm/Fake-Review-Detection/Amazon Scraping/ReviewData.csv", mode ='a', index = False, header =False)

            # update url counter for output parsing
            counter += 1
        else: 

            sys.exit() 
