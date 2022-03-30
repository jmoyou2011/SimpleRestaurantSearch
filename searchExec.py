from fuzzywuzzy import fuzz
import jaro
import pandas as pd
import numpy as np
from helper.helper_func import *

# import the csv files and join them by the id.

def getDataframe():
    cuisines_file = "csv/cuisines.csv"
    restaurants_file = "csv/restaurants.csv"

    df_cuisine = pd.read_csv(cuisines_file, dtype={"id": "Int64"})
    df_restaurants = pd.read_csv(restaurants_file, dtype = {"customer_rating":"Int64", "distance":"Int64",
                                                            "price": "Int64", "cuisine_id":"Int64"})

    df_join = create_dataframe(df_restaurants, df_cuisine)
    
    return df_join


def main(df_join, srch_eng):
        user_query = str(input("Enter your query:"))
        engine_tuple = ('L', 'J')
        print("Processing Filter Query for main query:\n")
        dist , rating , price, cuisine, filter_q = create_filter_query(user_query)
        print("Users filter query:{}".format(filter_q))
        
        # First condition: User has supplied a query with a filter query.
        # Treating filter queries similar to how solr treat filter queries i.e. executed before the query word
        if filter_q != "":
            filter_df = df_join.query(filter_q)
            print("Number of searchable documents:{}".format(filter_df.shape[0]))
            if srch_eng == engine_tuple[0]:
                result_user = calFuzzyRatio(user_query[0], filter_df)
                displayResults(result_user, df_join)
            else:
                result_user = calcJaroMetric(user_query[0], filter_df)
                displayResults(result_user, df_join)
        else:
            if srch_eng == engine_tuple[0]:
                result_user = calFuzzyRatio(user_query, df_join)
                displayResults(result_user, df_join)
            else:
                result_user = calcJaroMetric(user_query, df_join)
                displayResults(result_user, df_join)
        
        check = str(input("Do you want to search again or quit, enter y/n:"))
        if check.lower() == "y":
            main(df_join, srch_eng)
        else:
            exit()
            
if __name__ == '__main__':
    df_full = getDataframe()
    search_engine = initalUiHeader()
    main(df_full, search_engine)
    

    
