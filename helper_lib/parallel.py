# -*- coding: utf-8 -*-
"""
Auxiliary functions for parallel image processing

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
from multiprocessing import Process
import time


def _print_progress(procdone, totproc, start):
    """
    Computes and prints out the percentage of the processes that have been completed

    Parameters
    ----------
    procdone : int
        number of processes that have been completed
    totproc : int
        total number of processes
    start : float
        the time when the computation has started   
    """
    donepercent = procdone*100/totproc
    elapse = time.time() - start
    tottime = totproc*1.*elapse/procdone
    left = tottime - elapse
    units = 'sec'
    if left > 60:
        left = left/60.
        units = 'min'
        if left > 60:
            left = left/60.
            units = 'hours'

    print 'done', procdone, 'of', totproc, '(', donepercent, '% ), approx. time left: ', left, units


def run_parallel(process, process_name=None, print_progress=True, **kwargs):
    """
    Apply a given function in parallel to each item from a given list.

    Parameters
    ----------
    process : callable
        The function that will be applied to each item of `kwargs.items`.
        The function should accept the argument `item`, which corresponds to one item from `kwargs.items`.
        An `item` is usually a name of the file that has to be processed or 
            a list of files that have to be combined / convolved /analyzed together.
        The function should not return any output, but the output should be saved in a specified directory.
    process_name : str, optional
        Name of the process, will be printed if `print_progress` is set to True.
        If None, the name of the function given in `process` will be printed.
        Default is None.
    print_progress : bool, optional
        If True, the progress of the computation will be printed.
        Default is True.
    kwargs : key, value pairings
        Arbitrary keyword arguments

    Keyword arguments
    -----------------
    *items* : list
        List of items. For each item, the `process` will be called.
        The value of the `item` parameter of `process` will be set to the value of the current item from the list.
        Remaining keyword arguments will be passed to the `process`
    *max_threads* : int, optional
        The maximal number of processes to run in parallel
        Default is 8

    """

    items = kwargs.pop('items', [])
    max_threads = int(round(kwargs.pop('max_threads', 8)))
    if process_name is None:
        process_name = process.func_name

    if print_progress:
        print 'Run', process_name

    procs = []

    totproc = len(items)
    procdone = 0
    start = time.time()

    if print_progress:
        print 'Started at ', time.ctime()

    for i, cur_item in enumerate(items):

        while len(procs) >= max_threads:
            time.sleep(0.05)
            for p in procs:
                if not p.is_alive():
                    procs.remove(p)
                    procdone +=1
                    if print_progress:
                        _print_progress(procdone, totproc, start)

        cur_args = kwargs.copy()
        cur_args['item'] = cur_item
        p = Process(target=process, kwargs=cur_args)
        p.start()
        procs.append(p)

    while len(procs) > 0:
        time.sleep(0.05)
        for p in procs:
            if not p.is_alive():
                procs.remove(p)
                procdone += 1
                if print_progress:
                 _print_progress(procdone, totproc, start)

    if print_progress:
        print process_name, 'done'














