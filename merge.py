import pandas as pd
import constants
import os

# Load the CSV files
basic_df = pd.read_csv(os.path.join(constants.DATA_LOCATION, constants.BASIC_CSV_FILE))
detailed_df = pd.read_csv(os.path.join(constants.DATA_LOCATION, constants.DETAILED_CSV_FILE))

# Drop the 'package_name' column from detailed_df
detailed_df = detailed_df.drop(columns=['title'])

# Merge the DataFrames on 'package_url'
merged_df = pd.merge(basic_df, detailed_df, on='title_link', how='inner')

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('merged.csv', index=False)