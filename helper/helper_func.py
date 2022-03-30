from fuzzywuzzy import fuzz
import jaro
import pandas as pd
import numpy as np

def create_dataframe(df_rest:pd.DataFrame, df_cuisine:pd.DataFrame):
    """
    DESCRIPTION
    
        Creates the merge dataset between cuisine and restaurant.
    
    INPUT
    
        df_rest: restaurant dataframe 
        df_cuisine: cuisine dataframe
    
    OUTPUT
        
        df_full_restaurant: restaurant and cuisine merged dataframe.
    
    """
    old_vals = ["Hearty ChowClick", "Spicy PalaceClick to check domain availability."]
    new_vals = ["Hearty Chow Click", "Spicy Palace Click"]
    
    df_full_restaurant = pd.merge(df_rest, df_cuisine, how = "inner", left_on = "cuisine_id", right_on = "id")
    df_full_restaurant.rename(columns={"name_x":"name", "name_y": "cuisine"}, inplace = True)
    df_full_restaurant.drop(columns=["cuisine_id", "id"], inplace = True)
    
    df_full_restaurant['name'] = df_full_restaurant['name'].replace(old_vals, new_vals)
    
    return df_full_restaurant

def calFuzzyRatio(word:str, corpus_dataframe:pd.DataFrame):
    """
    DESCRIPTION
        
        This function calculates the Levenshtein Distance Ratio
        between two strings using the fuzzywuzzy module.
        
        Levenshtein algorithm is a measure of the number of edits(
        insertions, deletions and substitutions) needed to convert 
        one string to the other. By default, each type of edit has 
        the same weight.
        
    INPUT
        
        word: Query issued by the user.
        corpus_dataframe: Filtered dataframe if any are supplied.
        re_run: False by default when on the first run.
        
    OUTPUT
    
        results: List of dictionaries containing the relevant fields.
    
    """
    
    result_list = []
    threshold_first = 0.3
    
    for idx,row in corpus_dataframe.iterrows():
        res_dict = {}
        word_ratio = fuzz.token_set_ratio(word, row['name'].lower()) * 0.01
        if word_ratio > threshold_first:
            res_dict.update({"name": row["name"], "rating": row['customer_rating'],
                             "dist": row['distance'], "price": row['price'],
                             "cuisine": row['cuisine'], "score": word_ratio})

            result_list.append(res_dict)

    sorted_list = sorted(result_list, key=lambda k: (k['score'],-k["dist"], k['price'], k['rating']), reverse=True)
        
    return sorted_list

def calcJaroMetric(word:str, corpus_dataframe:pd.DataFrame):
    """
     DESCRIPTION
        
        This function calculates the Jaro-Winkler Distance Ratio
        between two strings.
        
        Jaro-Winkler algorithm is a measure of characters that are in common,
        being no more half the length of the longer string. Special 
        consideration is given to the differences near the start of the string
        are more significant than differences near the end of the string.
        
    INPUT
        
        word: Query issued by the user.
        corpus_dataframe: Filtered dataframe if any are supplied.
        re_run: False by default when on the first run.
        
    OUTPUT
    
        results: List of dictionaries containing the relevant fields.
    
    
    """
    result_list = []
    threshold_first = 0.3
    
    for idx,row in corpus_dataframe.iterrows():
        res_dict = {}
        word_ratio = jaro.original_metric(word, row['name'].lower())
        if word_ratio > threshold_first:
            res_dict.update({"name": row["name"], "rating": row['customer_rating'],
                             "dist": row['distance'], "price": row['price'],
                             "cuisine": row['cuisine'], "score": word_ratio})

            result_list.append(res_dict)
            
    sorted_list = sorted(result_list, key=lambda k: (-k["dist"], k['price'], k['rating']), reverse=True)      
    return sorted_list

def create_filter_query(query:str):
    """
    DESCRIPTION
        
        This function splits the query by the comma value 
        and creates different filter queries depending on the 
        size of the list.
        
    INPUT
    
        query: query submitted by user with filters separated by commmas
        
    OUTPUT
        
        dist(int): distance value provided by user
        rating(int): rating value provided by user
        price(int): price value provided by user
        cuisine(str): cuisine type provided by user
        
    """
    filter_q = ""
    filters = query.split(",")
    
    dist, price, rating, cuisine = "", "", "", "" 
    try:
        if (len(filters) < 2):
            pass

        if (len(filters) == 2):
            dist = int(filters[1]) if filters[1] else 0
            filter_q = "distance <= @dist"
            if dist == 0:
                pass

        if (len(filters) == 3):
            dist = int(filters[1]) if filters[1] else 0
            rating = int(filters[2]) if filters[2] else 0
            if dist == 0 and rating > 0:
                filter_q = "customer_rating >= @rating"
            elif dist > 0 and rating > 0:
                filter_q = "distance <= @dist and customer_rating >= @rating"
            elif dist == 0 and rating == 0:
                pass

        if (len(filters) == 4):
            dist = int(filters[1]) if filters[1] else 0
            rating = int(filters[2]) if filters[2] else 0
            price = int(filters[3]) if int(filters[3]) >= 10 else 0
            if dist > 0 and rating > 0 and price >= 10:
                filter_q = "distance <= @dist and customer_rating >= @rating and price <= @price"
            elif dist == 0 and rating > 0 and price >= 10:
                filter_q = "customer_rating >= @rating and price <= @price"
            elif dist >= 1 and rating == 0 and price >= 10:
                filter_q = "distance <= @dist and price <= @price"
            elif dist == 0 and rating == 0 and price >= 10:
                filter_q = "price <= @price"
            else:
                pass

        if (len(filters) == 5):
            dist = int(filters[1]) if filters[1] else 0
            rating = int(filters[2]) if filters[2] else 0
            price = int(filters[3]) if int(filters[3]) >= 10 else 0
            if filters[4].isnumeric():
                cuisine = None
            else:
                cuisine = filters[4].title() if filters[4] else None
            if dist > 0 and rating > 0 and price >= 10 and cuisine != None:
                filter_q = "distance <= @dist and customer_rating >= @rating and price <= @price and cuisine.str.contains(@cuisine)"
            elif dist == 0 and rating > 0 and price >= 10 and cuisine != None:
                filter_q = "customer_rating >= @rating and price <= @price and cuisine.str.contains(@cuisine)"
            elif dist > 0 and rating == 0 and price >= 10 and cuisine != None:
                filter_q = "distance <= @dist and price <= @price and cuisine.str.contains(@cuisine)"
            elif dist > 0 and rating > 0 and price < 10 and cuisine != None:
                filter_q = "distance <= @dist and customer_rating >= @rating and cuisine.str.contains(@cuisine)"
            elif dist > 0 and rating > 0 and price >= 10 and cuisine == None:
                filter_q = "distance <= @dist and customer_rating >= @rating and price <= @price"
            elif dist == 0 and rating == 0 and price >= 10 and cuisine != None:
                filter_q = "price <= @price and cuisine.str.contains(@cuisine)"
            elif dist > 0 and rating == 0 and price < 10 and cuisine != None:
                filter_q = "distance <= @dist and cuisine.str.contains(@cuisine)"
            else:
                pass
    except ValueError:
        print("Invalid filters provided")
        filter_q = ""
    
    return dist, rating, price, cuisine, filter_q

def displayResults(search_res:list, corpus_dataframe:pd.DataFrame):
    """
    DESCRIPTION
        
        Function controls the display of the printed results
        from the search results.
    
    INPUT
        search_res: Search results from either two metrics
    
    OUTPT
        Pretty display of the results with the restaurant name at the top,
        then the average customer review and cuisine on either side. Finally,
        The distance in miles away and average price per person.
    
    """
    # Get Length of the array to see if to return all documents if length less than 5
    res = search_res
    length_res = len(res)
    number_print = range(5)
    
    if length_res == 0:
        print([])
    elif length_res < 5:
        print("Less than five result, returning entire dataframe:\n")
        print(corpus_dataframe)
    elif length_res >= 5:
        print("\t" + "__" * 40)
        print("\n" + "\t"*5 + "Search Response:\n")
        for j in number_print:
            print("\t"* 3 +"_" * 45)
            print("\n" + "\t"*5 + "{}".format(res[j]["name"]))
            print("\n" + "\t"*3 + "Average Review:{}\t\t {}".format(res[j]["rating"], res[j]['cuisine']))
            print("\n" + "\t"*3 + "Miles Away:{}\t\tPrice/person:${}".format(res[j]['dist'], res[j]['price']))  
            print("\t"* 3 +"_" * 45)
            
def initalUiHeader():
    """
    DESCRIPTION
    
            Creates the intial header to indicate to the user the search application has started
            and they have selected their search metric for similarity.
    
    """
    print("\t"*5 + "Local Restaurant Search\n")
    print("\t"*4 + "-" * 40)
    engine_tuple = ('L', 'J')
    
    print("\t"*3 + "You can use either search metric: Levenshtein or Jaro-Winkler\n")
    srch_eng = str(input("Type L for Levenshtein or J for Jaro-Winkler: "))
        
    if srch_eng.upper() not in engine_tuple:
        print("Defaulting to Levenshtein Distance Metric")
        srch_eng = "L" 
        
    print("There are four filters to use: distance, customer rating, price and cuisine type\n")
    print("Distance, customer rating and price are all integers while cuisine type is a string.\n")
    print("Enter your query in the following manner: 'query,distance,customer rating,price,cuisine type'\n")
    
    return srch_eng