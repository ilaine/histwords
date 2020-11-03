import numpy as np
import os, sys
from multiprocessing import Queue, Process
from argparse import ArgumentParser

tpath = os.path.dirname(os.path.realpath(__file__))
VIZ_DIR=os.path.join(tpath, "web")

ROOT_DIR=tpath
tpath = os.path.abspath(os.path.join(tpath, "../"))

sys.path.append(tpath)
os.chdir(tpath)

from ioutils import load_pickle, write_pickle

def worker(proc_num, queue, dir, count_dir, min_count):
    while True:
        if queue.empty():
            break
        year = queue.get()
        print "Loading data...", year
        print "Path..", "sgns/" + count_dir + str(year) + "-counts.pkl"
#        time.sleep(120 * random.random())
        freqs = load_pickle("sgns/" + count_dir + str(year) + "-counts.pkl")
        iw = []
        with open("sgns/" + dir + str(year) + "/" + str(year) + ".sgns.words.txt") as fp: # seems to correspond to X.counts.words.vocab
            info = fp.readline().split()
            vocab_size = int(info[0])
            dim = int(info[1])
            w_mat = np.zeros((vocab_size, dim))
            for i, line in enumerate(fp):
                line = line.strip().split()
                iw.append(line[0].decode("utf-8"))
                if freqs[iw[-1]] >= 500:
                    w_mat[i,:] = np.array(map(float, line[1:]))
        c_mat = np.zeros((vocab_size, dim))
        with open("sgns/" + dir + str(year) + "/" + str(year) + ".sgns.contexts.txt") as fp: # seems to correspond to X.counts.contexts.vocab >> TEST IN "GROUP"
            fp.readline()
            for i, line in enumerate(fp):
                line = line.strip().split()
                if freqs[line[0]] >= min_count:
                    c_mat[i,:] = np.array(map(float, line[1:]))
        np.save("sgns/" + dir + str(year) + "/" + str(year) + "-w.npy", w_mat)
        np.save("sgns/" + dir + str(year) + "/" + str(year) + "-c.npy", c_mat)
        write_pickle(iw, "sgns/" + dir + str(year) + "/" + str(year) + "-vocab.pkl")

if __name__ == "__main__":
    parser = ArgumentParser("Post-processes SGNS vectors to easier-to-use format. Removes infrequent words.")
    parser.add_argument("dir")
    parser.add_argument("count_dir", help="Directory with count data.")
    parser.add_argument("--workers", type=int, help="Number of processes to spawn", default=20)
    parser.add_argument("--start-year", type=int, default=1860) #
    parser.add_argument("--end-year", type=int, default=2000)
    parser.add_argument("--year-inc", type=int, default=10) #
    parser.add_argument("--min-count", type=int, default=300) #
    args = parser.parse_args()
    years = range(args.start_year, args.end_year + 1, args.year_inc)
    queue = Queue()
    for year in years:
        queue.put(year)
    procs = [Process(target=worker, args=[i, queue, args.dir, args.count_dir, args.min_count]) for i in range(args.workers)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
