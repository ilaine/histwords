# -*- coding: utf-8 -*-

import os, sys
import numpy as np
from argparse import ArgumentParser

tpath = os.path.dirname(os.path.realpath(__file__))

ROOT_DIR=tpath
tpath = os.path.abspath(os.path.join(tpath, "../"))

sys.path.append(tpath)
os.chdir(tpath)

from ioutils import write_pickle, words_above_count, mkdir
from vecanalysis import alignment
from representations.representation_factory import create_representation

def align_years(years, rep_type, in_dir, out_dir, count_dir, min_count, **rep_args):
    first_iter = True
    base_embed = None
    for year in years:
        print "Loading year:", year
        year_embed =  create_representation(rep_type, in_dir + str(year) + "/" + str(year), **rep_args)
        year_words = words_above_count(count_dir, year, min_count)
        year_embed.get_subembed(year_words)
        print "Aligning year:", year
        if first_iter:
            aligned_embed = year_embed
            first_iter = False
        else:
            aligned_embed = alignment.smart_procrustes_align(base_embed, year_embed)
            #~ aligned_embed = alignment.procrustes_align(base_embed, year_embed)
        base_embed = aligned_embed
        print "Writing year:", year
        foutname = out_dir + str(year)
        np.save(foutname + "-w.npy",aligned_embed.m)
        write_pickle(aligned_embed.iw, foutname + "-vocab.pkl")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("dir")
    parser.add_argument("rep_type") # SGNS
    parser.add_argument("count_dir")
    parser.add_argument("--min-count", type=int, default=300)
    parser.add_argument("--start-year", type=int, default=1860) # CHANGED: default 1800
    parser.add_argument("--end-year", type=int, default=2000)
    parser.add_argument("--year-inc", type=int, default=10) # CHANGED: default 1
    args = parser.parse_args()
    years = range(args.start_year, args.end_year + 1, args.year_inc)
    out_dir = args.dir + "/aligned/"
    mkdir(out_dir)
    align_years(years, args.rep_type, args.dir, out_dir, args.count_dir, args.min_count)
