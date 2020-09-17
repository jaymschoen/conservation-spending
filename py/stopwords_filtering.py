import re
import csv
import tqdm
import numpy as np
import pandas as pd


def string_found(string1, string2):
    if re.search(r"\b" + re.escape(string1) + r"\b", string2):
        return True
    return False


output_grants = '/home/psd2120/research/Data/Output/output_grants_v15.csv'
stopwords_csv = '/home/psd2120/research/Data/Stopwords/Stopwords_Alphabetized_v9.csv'
output_filtered = '/home/psd2120/research/Data/Output/output_grants_v15_filtered.csv'

output_data = pd.read_csv(output_grants)
output_data['Stopwords'] = "-"
output_data['Filtered_Categories'] = "-"

stopwords_df = pd.read_csv(stopwords_csv)
stopwords_dict = dict()
for cat in [x.strip() for x in list(stopwords_df)]:
    temp = list(set(stopwords_df[cat].dropna()))
    temp = [x.lower() for x in temp]
    stopwords_dict[cat] = temp
pbar = tqdm.tqdm(total=len(output_data))

for idx in range(len(output_data)):
    class_cats = list(output_data.iloc[idx]['Categories'].split('|'))
    stop_added = []
    flag = False

    for stop_cat in stopwords_dict.keys():
        if stop_cat in class_cats:
            for stopword in stopwords_dict[stop_cat]:
                if string_found(stopword,
                                output_data.iloc[idx]['Description'].lower()):
                    class_cats.remove(stop_cat)
                    stop_added.append(stopword)
                    break
    output_data.loc[idx,'Filtered_Categories'] = '|'.join(list(set(class_cats)))
    if len(stop_added) > 0:
        output_data.loc[idx, 'Stopwords'] = '|'.join(list(set(stop_added)))
    pbar.update(1)
pbar.close()
output_data[output_data.Stopwords != '-']
output_data.to_csv(output_filtered, index=False)
