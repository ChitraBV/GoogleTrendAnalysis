from Google_Trends.TrendAnalysis_Func import *

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df = read_excel_cache('Brand_input.xlsx',
                          sheet_name='Brands_Order')  # can also index sheet by name or fetch all sheets
    # putting all  these into a list
    list_brands = df['Brands'].tolist()

    # calling split_list function to split all the brands into group of 3
    group_size = 3  # group size # we can change give this as input to user to change the group size
    overlap_size = 1  # overlap size # we can change give this as input to user to change the overlap size
    list_split = split_list(list_brands, group_size, overlap_size)

    # calling IOT_brand function to get the interest over time dataframe for all the brands
    df_clean = IOT_brand(list_split)

    # calling normalizing_brand function to normalize the values of the dataframe
    df_write = normalizing_brand(df_clean)

    # writing the dataframe to excel
    writer = pd.ExcelWriter('GoogleTrends.xlsx', engine='xlsxwriter')
    df_write.to_excel(writer, sheet_name='Calculated_IOT')
    writer.save()
