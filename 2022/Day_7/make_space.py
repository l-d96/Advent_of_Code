import re
from collections import defaultdict

lines = []
count_ls = 0
count_cd_in_dir_before_ls = 0
with open("./input.txt") as f:
    for line in f:
        if re.match('^\$ ls.*$', line):
            count_ls += 1
            if re.match('^\$ cd[^\.]*$', lines[-1]):
                count_cd_in_dir_before_ls += 1
        lines.append(line.strip())

if count_ls == count_cd_in_dir_before_ls:
    print("ls command is always preceded by a cd into a directory.\n")


def collect_outputs(history):
    outputs = defaultdict(list)
    index = 0
    is_output = 0
    for count, line in enumerate(history):
        if re.match('^\$.*$', line):
            is_output = 0
        if re.match('^\$ ls.*$', line):
            current_dir = history[count-1].split(' ')[2]
            is_output = 1
            index += 1
            continue
        if is_output:
            outputs[current_dir].append(line)

    return outputs


def determine_size(outputs: dict):
    sizes = {}
    for key, values in outputs.items():
        size = 0
        for single_output in values:
            first_part, second_part = single_output.split(' ')
            if first_part == "dir":
                continue
            else:
                size += int(first_part)
        sizes[key] = size

    return sizes


def determine_dirs(outputs: dict):
    dirs = defaultdict(list)
    for key, values in outputs.items():
        for single_output in values:
            first_part, second_part = single_output.split(' ')
            if first_part == "dir":
                dirs[key].append(second_part)
            else:
                continue

    return dirs


outputs = collect_outputs(lines)
sizes = determine_size(outputs)
dirs = determine_dirs(outputs)
sizes_less_than_100K = list(filter(lambda x: x[1] <= 100000, sizes.items()))
sizes_less_than_100K = list(filter(lambda x: x <= 100000, sizes.values()))
print(sum(sizes_less_than_100K))
