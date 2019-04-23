# -*- coding: utf-8 -*-
"""
Auxiliary functions for working with files and statistics

:Author:
  `Anna Medyukhina`_
  email: anna.medyukhina@leibniz-hki.de or anna.medyukhina@gmail.com	

:Organization:
  Applied Systems Biology Group, 
  Leibniz Institute for Natural Product Research and Infection Biology - Hans Knöll Institute (HKI)

Copyright (c) 2014-2018, 
Leibniz Institute for Natural Product Research and Infection Biology – 
Hans Knöll Institute (HKI)

Licence: BSD-3-Clause, see ./LICENSE or 
https://opensource.org/licenses/BSD-3-Clause for full details

"""
import os
import pandas as pd
from skimage import io


##########################################################
# global _IMAGE_EXTENSIONS
_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'bmp', 'PNG', 'JPG', 'JPEG', 'BMP', 'tif', 'TIFF', 'tiff', 'TIF']


def _is_in_extensions(filename, extensions):
    """
    Returns True if `filename` has an extension from a specified list.
    
    Parameters
    ----------
    filename : str
        String with a filename.
    extensions : list of str
        List of allowed file extensions.
        
    Returns
    -------
    bool
        True if the `filename` has an extension contained in `extensions`, False otherwise.
    """

    parts = filename.split('.')
    if len(parts) > 1:
        ext = parts[-1]
    else:
        ext = ''

    if ext in extensions or '*' in extensions:
        return True
    else:
        return False


def make_folders(folders):
    """
    Create directories from a given list.

    Parameters
    ----------
    folders : list of str
        List of directory paths that will be created.
    """
    for folder in folders:
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except OSError:
                pass


def list_subfolders(inputfolder, cur_subfolder=None, subfolders=None, extensions=None):
    """
    Returns a list of files in a given directory including subdirectories.

    Parameters
    ----------
    inputfolder : str
        Name of directory where the files will be listed.
    cur_subfolder : str, optional
        Current subdirectory. Auxiliary parameter for recursion.
        Default: None
    subfolders : list of str, optional
        Current list of subdirectories. Auxiliary parameter for recursion.
        Default None 
    extensions : list of str, optional
        List of file extensions to include in the list.
        If None, the list of extensions is specified by the global variable `IMAGE_EXTENSIONS`
        Default: None

    Returns
    -------
    list of str
        list of files the given directory
        
    Examples
    --------
    >>> list_subfolders("test_folder/", extensions=["tiff, 'tif"])
    ['image1.tif', 
    'subfolder1/image2.tiff', 
    'subfolder1/image3.tiff', 
    'subfolder1/subsubfolder1/image4.tif', 
    'subfolder2/image5.tiff']

    """

    if extensions is None:
        # global IMAGE_EXTENSIONS
        extensions = _IMAGE_EXTENSIONS

    if cur_subfolder is None:
        cur_subfolder = ''

    if subfolders is None:
        subfolders = []

    files = os.listdir(inputfolder + cur_subfolder)

    for path in files:
        if os.path.isdir(inputfolder + cur_subfolder + path):
            if path[-1] != '/':
                path = path + '/'
            subfolders = list_subfolders(inputfolder,  cur_subfolder=cur_subfolder + path, subfolders=subfolders,
                                         extensions=extensions)
        else:
            if _is_in_extensions(path, extensions):
                subfolders.append(cur_subfolder + path)

    return subfolders


def combine_statistics(inputfolder, print_progress=False):
    """
    Concatenates all statistic tables from csv files located in a given directory.
    The resulting table will be saved into `inputfolder` + ".csv".
    
    Parameters
    ----------
    inputfolder : str
        Name of directory, where the csv files are located that should be concatenated.
               
    Examples
    --------
    >>> combine_statistics("output/statistics/")  
    # all csv files in the folder "output/statistics/" will be concatenated
    # the result will be saved in the file "output/statistics.csv".
    """

    if os.path.exists(inputfolder):
        subfolders = list_subfolders(inputfolder, extensions=['csv'])
        total_length = len(subfolders)

        if print_progress:
            print 'Combining files started...'
        array = []
        for i, sf in enumerate(subfolders):
            data = pd.read_csv(inputfolder + sf, sep='\t', index_col=0)
            array.append(data)
            if print_progress:
                print i+1, 'out of', total_length, 'is done'
        data = pd.concat(array, ignore_index=True, sort=True)
        data.to_csv(inputfolder[:-1] + '.csv', sep='\t')
        if print_progress:
            print 'Combining files finished'


def imsave(outputfile, img):
    """
    Creates the output directory for the image (if not exists) and saves the image.
    
    Parameters
    ----------
    outputfile : str
        Path string to a filename where the image should be saved.
    img : ndarray
        An MxN or KxMxN array to save as a tif image.
    """
    make_folders([os.path.dirname(outputfile)])
    io.imsave(outputfile, img)

