"""
Example of how to use Medinify's scraping functionality
"""

from medinify.scrapers import WebMDScraper, DrugRatingzScraper, DrugsScraper, EverydayHealthScraper
import pandas as pd
import json

input_list = ["galzin"]

webmd_names_errors = []
everydayhealth_names_errors = []

def main():
    scraper = WebMDScraper()  # non funziona DrugsScraper(), non funziona DrugRatingzScraper(), or EverydayHealthScraper()
    url = ""
    json_aggregrationReviews = {"website" : "webmd.com"}
    json_aggregrationReviews["ratingSystem"] = "stars"
    json_aggregrationReviews["itemsNamesAggregration"] = input_list
    reviewsAggregrate = []
    for i in range(len(input_list)):
        json_reviews = {"name" : input_list[i]}
        try :
            url = scraper.get_url(input_list[i])  # or any other drug name
            scraper.scrape(url)
            dataframe_reviews = pd.DataFrame.from_dict(scraper.reviews)
            json_reviews["averageEffectiveness"] = round(pd.DataFrame.from_records(dataframe_reviews["rating"])["effectiveness"].mean(), 1)
            json_reviews["averageEaseOfUse"] = round(pd.DataFrame.from_records(dataframe_reviews["rating"])["ease of use"].mean(), 1)
            json_reviews["averageSatisfaction"] = round(pd.DataFrame.from_records(dataframe_reviews["rating"])["satisfaction"].mean(), 1)
            json_reviews["minRating"] = round(pd.DataFrame.from_records(dataframe_reviews["rating"])["satisfaction"].min(), 1)
            json_reviews["maxRating"] = round(pd.DataFrame.from_records(dataframe_reviews["rating"])["satisfaction"].max(), 1)
            json_reviews["reviews"] = scraper.reviews
        except :
            print("Could not get "+ input_list[i] + " from webmd website")
            webmd_names_errors.append(input_list[i])
        reviewsAggregrate.append(json_reviews)
    json_aggregrationReviews["aggregrateReviews"] = reviewsAggregrate
    
    with open("webmdresult.json", "w") as f:
        obj = json.dumps(json_aggregrationReviews, indent = 4)
        f.write(obj)
    
    scraper2 = EverydayHealthScraper()
    json_aggregrationReviews = {"website" : "everydayhealth.com"}
    json_aggregrationReviews["ratingSystem"] = "stars"
    json_aggregrationReviews["itemsNamesAggregration"] = input_list
    reviewsAggregrate = []
    for i in range(len(input_list)):
        json_reviews = {"name" : input_list[i]}   
        try :
            url = scraper2.get_url("Adderall")
            print(url)
            scraper2.scrape(url)
            dataframe_reviews = pd.DataFrame.from_dict(scraper2.reviews)
            json_reviews["averageRating"] = round(dataframe_reviews["rating"].mean(),1)
            json_reviews["minRating"] = round(dataframe_reviews["rating"].min(), 1)
            json_reviews["maxRating"] = round(dataframe_reviews["rating"].max(), 1)
            json_reviews["reviews"] = scraper2.reviews
        except :
            print("Could not get "+ input_list[i] + " from everydayhealthscraper website " )
            everydayhealth_names_errors.append(input_list[i])
        reviewsAggregrate.append(json_reviews)
    
    json_aggregrationReviews["aggregrateReviews"] = reviewsAggregrate

    with open("everydayhealth.json", "w") as f:
        obj = json.dumps(json_aggregrationReviews, indent = 4)
        f.write(obj)

    if (len(webmd_names_errors) != 0) :
        print("I could not get from webmd " + str(webmd_names_errors) )
    
    if (len(everydayhealth_names_errors) != 0 ):
        print("I could not get from everydayhealth " + str(everydayhealth_names_errors) )
    
if __name__ == '__main__':
    main()
