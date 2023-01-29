import pickle as pkl

import pandas as pd
from tqdm import tqdm


def process_umls_index_dataset(data_path, data_savename, id2string_savename, headers):
    """
    Generates data file needed to build a UMLS index and a hash table mapping each
    CUI to one canonical concept string. Takes the raw .RRF data file and saves
    a .tsv indec concept file as well as the a .pkl file of cui to concept string
    mappings. Only data marked as English is added to the index data file.
    Arguments:
        data_path (str): path to MRCONSO.RRF UMLS data file
        data_savename (str): path to where .tsv index data will be saved
        id2string_savename (str): path to where .pkl cui to string mapping will
                                  be saved
        headers (list): column lables within MRCONSO.RRF
    """

    print("Loading index data file...")
    df = pd.read_table(data_path, names=headers, index_col=False, delimiter='|')
    id2string = {}

    with open(data_savename, "w") as outfile:
        for idx, row in tqdm(df.iterrows(), total=df.shape[0]):
            # Address incorrectly formatted data
            if type(row["STR"]) != str or "|" in row["STR"]:
                continue

            cui = row["CUI"]
            sent = row["STR"]

            # Removing leading C to convert label string to int
            cui = int(cui[1:])

            # Only keeping english concepts
            if row["LAT"] == "ENG":
                outfile.write(f'{cui}\t{sent}\n')

                # Matching each cui to one canonical string represention
                if cui not in id2string and ":" not in sent:
                    id2string[cui] = sent

    outfile.close()
    pkl.dump(id2string, open(id2string_savename, "wb"))
    print("Finished saving index data and id to concept mapping")
