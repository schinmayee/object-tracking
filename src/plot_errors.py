#!/usr/bin/env python

import argparse, os
import numpy as np
import pickle
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser("Plot errors")

parser.add_argument('--config', dest='config', type=str, default='config.txt',
                    help='config file containing error directories'
                         'relative to config file')
parser.add_argument('--output', dest='output_dir', type=str,
                    help='Output directory')

args = parser.parse_args()
if not args.output_dir:
    print('Output directory name required')
    parser.print_help()
    exit(1)

if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)
assert(os.path.isdir(args.output_dir))


# read configuration for plot
config_dir = os.path.dirname(os.path.realpath(args.config))
error_names = list()
error_dirs = list()
with open(args.config) as config:
    for line in config.readlines():
        data = line.split()
        if len(data) != 2:
            continue
        error_names.append(data[0])
        error_dirs.append(data[1])

N = len(error_names)

# read errors
mean = list()
dev = list()
for dir_name in error_dirs:
    file_name = os.path.join(config_dir, dir_name, 'position_error')
    assert(os.path.isfile(file_name))
    data = open(file_name)
    errors = pickle.load(data)
    data.close()
    #errors = errors[0:100]
    mean.append(np.mean(errors))
    dev.append(np.std(errors))

#print(mean)
#print(dev)

ind = np.arange(N)  # the x locations for the groups
width = 0.6       # the width of the bars

fig, ax = plt.subplots()
rects = ax.bar(ind, mean, width, color='k', yerr=dev, align='center')

# add some text for labels, title and axes ticks
ax.set_ylabel('Mean error in position estimate')
ax.set_ylim([0.8*min(mean),1.2*max(mean)])
ax.set_title('Error in Position')
ax.set_xticks(ind)
ax.set_xticklabels(error_names)

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%.04f' % height,
                ha='center', va='bottom')

autolabel(rects)

plt.savefig(os.path.join(args.output_dir, 'position_error.png'))


'''
Relative position error does not make much sense as computed below.
'''

'''
# read errors
mean = list()
dev = list()
for dir_name in error_dirs:
    file_name = os.path.join(config_dir, dir_name, 'pos_rel_error')
    assert(os.path.isfile(file_name))
    data = open(file_name)
    errors = pickle.load(data)
    data.close()
    #errors = errors[0:100]
    mean.append(np.mean(errors))
    dev.append(np.std(errors))

#print(mean)
#print(dev)

ind = np.arange(N)  # the x locations for the groups
width = 0.6       # the width of the bars

fig, ax = plt.subplots()
rects = ax.bar(ind, mean, width, color='k', yerr=dev, align='center')

# add some text for labels, title and axes ticks
ax.set_ylabel('Mean Relative Position Error')
ax.set_ylim([0.8*min(mean),1.2*max(mean)])
ax.set_title('Relative Position Error')
ax.set_xticks(ind)
ax.set_xticklabels(error_names)

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%.04f' % height,
                ha='center', va='bottom')

autolabel(rects)

plt.savefig(os.path.join(args.output_dir, 'position_rel_error.png'))
'''
