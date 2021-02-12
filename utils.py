import numpy as np
import pandas as pd
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

def isolate(x,y,xlim,ylim):
    '''Gives indices for elements in x,y range.
    Parameters :
    ------------
    x : array-like
    x coordinates of element set.
    y : array-like
    y coordinates of element set.
    xlim : array-like of form :[xlimmin,xlimmax]
    specify maximum and minimum x values for elements to isolate.
    ylim : array-like of form :[ylimmin,ylimmax]
    specify maximum and minimum y values for elements to isolate.
    
    Returns :
    --------
    ind : array-like
    Array containing indices of isolated elements. Can then be easily called, e.g. x-coords : x[ind]'''
    if len(xlim) == 0 or len(ylim) ==0:
        return []
    else:
        ind = np.where(np.logical_and(np.logical_and(y>= ylim[0],y<=ylim[1]),np.logical_and(x <= xlim[1],x>=xlim[0])))
        return ind[0]

def get_ind(arr,val):
    '''Gives index for any specified value from a list. Does not only give the first index with that value.
    Parameters :
    ------------
    arr : array-like.
    1D list
    val : double
    value to search for.
    
    Returns :
    --------
    ind : array-like
    Array containing indices of specific value in array.'''
    ind = []
    for j in range(len(arr)):
        if arr[j]==val:
            ind.append(j)
    return ind

def zero_list(arr,val = 0):
    '''Generates a list of the same shape as the input array, this is for use when the array in question does not have
    a consistent shape so that it can be generated using numpy.
    Parameters :
    ------------
    arr : array-like
    2D list, where the lists in the second dimension are not of the same length. 
    val : double (optional)
    value with which to initialize the array.'''
    nrows = len(arr)
    ncols = []
    zero_arr = []
    for i in range(0,nrows):
        if isinstance(arr[i], int):
            ncols.append(1)
        else:
            ncols.append(len(arr[i]))
    for lencol in ncols:
        zero_arr.append(lencol*[val])
    return zero_arr
                     
def err_min(dx,dy):
    '''TODO INSERT DOCUMENTATION HERE'''
    df = np.sqrt(dx**2 + dy**2)
    return df

def read_data(data_dir,cols):
    '''TODO INSERT DOCUMENTATION HERE'''
    RA = []
    DEC = []
    VLSR = []
    FLUX = []
    DFLUX = []
    data_files = []
    with open(data_dir+'/Fileorder.txt') as f:
        for line in f:
            data_files.append(data_dir + '/'+line[:-1])

    for name in data_files: 
        df = pd.read_csv(name,sep = ',')
        ra,dec,vlsr,flux,dflux = extract_from_df(df,cols)
        RA.append(ra)
        DEC.append(dec)
        VLSR.append(vlsr)
        FLUX.append(flux)
        DFLUX.append(dflux)
    return RA,DEC,VLSR,FLUX,DFLUX
