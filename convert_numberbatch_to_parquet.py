# Converts the text file version of Numberbatch to a Parquet file
# The resulting Parquet file can be loaded by Pandas significantly faster than
# the text file or the HDF5 file 

import pandas as pd

if __name__=='__main__':
    # Note that the first line (the line indicating the size of the matrix)
    # MUST BE MANUALLY DELETED BEFORE RUNNING THIS SCRIPT
    # in order to simplify loading into a DataFrame
    print('Loading text file into DataFrame...')
    df = pd.read_csv('./numberbatch-en-19.08.txt', sep=' ', header=None, index_col=0)
    print('Done.')

    # Changes to make to_parquet happy
    df.columns = df.columns.astype(str) # Convert column names to string
    df.index.name = 'concept'           # Provide an index name

    # index=True because we need the indices (the concept which corresponds to the embedding)
    print('Writing to Parquet file...')
    df.to_parquet('./numberbatch-en-19.08.parquet', index=True)
    print('Done.')

