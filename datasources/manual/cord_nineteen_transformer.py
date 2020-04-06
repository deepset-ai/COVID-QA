# Simple script to turn CORD-19 data into .txt files to be added to
# the deepset.ai text annotation tool

# assumes you downbloaded the CORD-19 data: https://pages.semanticscholar.org/coronavirus-research
# On a modern laptop this scrip takes about less tha a minute to run on each CORD-19 subset.

import os
import sys
import pandas as pd
import numpy as np
import json
from tqdm import tqdm

# Individual paths to various CORD-19 subsets
COMM_USE_SUBSET = 'comm_use_subset/comm_use_subset/'
BIORXIV_MEDRXIV = 'biorxiv_medrxiv/biorxiv_medrxiv/'
NONCOMM_USE_SUBSET = 'noncomm_use_subset/noncomm_use_subset/'

# Add your path to the CORD-19 data here.
ROOT = '...ADD-HERE.../CORD-19-research-challenge/'
SUBSET_CORD_DATA = 'Add one of the individual paths from the above subsets here...'

OUTPUT_DIR = 'custom_txt_data/'
METADATA = 'metadata.csv'
COLUMNS = ['sha','title','doi','license','abstract','publish_time','authors','url'] #data to keep


# df of all the SHAs in the metadata.csv
df = pd.read_csv(os.path.join(ROOT, METADATA), usecols = COLUMNS)
print('Total articles found in Metadata are: ', len(df)) #length around 45774 articles

# Get file names for SHAs matching from commercial available dir
dir_to_walk = os.listdir(os.path.join(ROOT,SUBSET_CORD_DATA)) #switch out CORD-19 data subset here
sha_list = []
for item in dir_to_walk:
    sha_list.append(item.split('.')[0]) #strip out '.json'

# Now to extract out the relevant SHA data from metadata
custom_df = df[df['sha'].isin(sha_list)]
# print(len(custom_df)) #might be a count less than the number found in metadata, some SHA cells are empty


# E.g. 850 json docs from COMM_USE_SUBSET are not found in the metadata's SHA column
# thus we will save the missing filenames to a list to look at later
json_docs_not_in_csv = list(set(sha_list) - set(custom_df['sha'].to_list()))
missing_json = 'missing_json_from_metadata.txt'
with open(os.path.join(ROOT,missing_json), 'w') as out_file:
    for row in json_docs_not_in_csv:
        out_file.write(row + '\n')
print("Any missing JSON filenames have been marked and saved to a new file!")


# Let's create .txt files from the known JSON and save them in a dir to upload
# this combines metadata with json textbody data into a newly formatted .txt file
for row in tqdm(custom_df.iterrows()):
    article_text = []
    with open(os.path.join(ROOT, custom_df, row[1].sha + '.json')) as in_file:
        json_data = json.load(in_file)
        for idx in range(len(json_data["body_text"])):
            article_text.append("{}".format(json_data["body_text"][idx]["text"]))
    
    formatted_article_text = '\n\n'.join(article_text)
    
    file_to_write = row[1].sha + '.txt'
    text_to_write = f"{row[1].title}\n\n" \
                        f"{row[1].url}\n\n" \
                        f"SHA: {row[1].sha}\n\n" \
                        f"Authors: {row[1].authors}\n" \
                        f"Date: {row[1].publish_time}\n" \
                        f"DOI: {row[1].doi}\n" \
                        f"License: {row[1].license}\n\n" \
                        f"Abstract: {row[1].abstract}\n\n" \
                        f"Text: {formatted_article_text}"
    
    with open(os.path.join(ROOT, OUTPUT_DIR, file_to_write), 'w') as out_file:
        out_file.write(text_to_write.strip())

print("Processed all known files for the CORD-19 subset choosen and saved .txt files in the custom_txt_data dir!")