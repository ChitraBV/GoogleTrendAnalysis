from Google_Trends.Trend_Analysis_lib import *


# splitting all the brands into group of 3
# Sublist of list with 3 elements and last element of each sublist will be overlapping with next sublist
def split_list(brands, n, m):
    split_result = [brands[i:i + n] for i in range(0, len(brands), n - m)]
    return split_result


def IOT_brand(passed_list):
    pytrend = TrendReq()
    iot_result = []
    # looping through each sublist
    for i in passed_list:
        pytrend.build_payload(kw_list=i, geo='DE', timeframe=f'2020-01-05 {date.today()}', cat=0)
        # cat=0 means all categories, geo='DE' means Germany, timeframe=f'2020-01-05 {date.today()}' means from
        # 2020-01-05 to today
        interest_over_time_df = pytrend.interest_over_time()
        # above line will return a dataframe with all the keywords and their interest over time
        iot_result.append(interest_over_time_df)
        # above line will append the dataframe to a list
        iot_df = pd.concat(iot_result, axis=1)
    # above line will concatenate all the dataframes in the list to a single dataframe
    iot_df_clean = iot_df.drop('isPartial', axis=1)
    # above line will drop the column isPartial
    return iot_df_clean


def normalizing_brand(clean_df):
    # values which are 0.0 are replaced with 1 for the overlapping brands as while we normalize the brands
    # we will be dividing by these values, and do not want to divide by 0
    for x in range(3, len(clean_df.columns), 3):
        clean_df[clean_df.eq(0.0)] = 1

    # dummy_var will be used to store values replaced with 1 for the overlapping brands
    dummy_var = clean_df.values
    # above line will store the values of the dataframe in a numpy array

    # normalizing the values of the dataframe.
    for x in range(3, len(clean_df.columns), 3):
        clean_df.iloc[:, x:x + 3] = (dummy_var[:, x:x + 3] * dummy_var[:, x - 1, None] / dummy_var[:, x, None])
        # updating the dataframe with the new values and using that for next iteration
        dummy_var = clean_df.values

    # drop duplicates columns from clean_df
    final_df = clean_df.loc[:, ~clean_df.columns.duplicated()]

    # adding the name for index of the dataframe
    final_df.index.name = 'Date'
    return final_df
