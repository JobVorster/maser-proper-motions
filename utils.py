import numpy as np
def extract_from_df(df,cols):
    '''Utility function to get specified columns from a dataframe as a list object.
    Parameters :
    ------------
    df : Pandas DataFrame.
    Pandas dataframe to extract data.
    
    Returns : 
    ---------
    allcols : 2D list containing all the specified dataframe columns.'''
    allcols = []
    for col in cols:
        allcols.append(df[col].values)
    return allcols

def isolate(x1,y1,xlim1,ylim1):
    ind = np.where(np.logical_and(np.logical_and(y1> ylim1[0],y1<ylim1[1]),np.logical_and(x1 < xlim1[1],x1>xlim1[0])))
    return ind[0]
