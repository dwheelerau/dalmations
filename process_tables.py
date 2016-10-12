#!/usr/bin/python
import sys

noise = 5.0


def cal_percents(count_list):
    """loci,pos,ref,depth,A,C,G,T"""
    depth = float(count_list[3])
    if depth > 0:
        count_list.append(str(100*(int(count_list[4])/depth)))  # perA
        count_list.append(str(100*(int(count_list[5])/depth)))  # perC
        count_list.append(str(100*(int(count_list[6])/depth)))  # perG
        count_list.append(str(100*(int(count_list[7])/depth)))  # perT
    else:
        # div by zero error
        count_list.append('0.0')
        count_list.append('0.0')
        count_list.append('0.0')
        count_list.append('0.0')
    return count_list


def filter_data(data):
    """filter out noise and if greater than noise collect nt call"""
    # ACGT
    ref = data[2]
    choice = ["A", "C", "G", "T"]
    counter = 0
    # if 100% non-ref call will still show ref/alt
    result = []
    for per in data[8:]:
        if float(per) > noise:
            call = choice[counter]
            if call not in result:
                result.append(call)
        else:
            pass
        # modify float in case it will be returned
        data[8+counter] = "%.0f" % (float(per))
        counter += 1
    if len(result) > 1:
        result = "/".join(result)
        data.append(result)
    elif len(result) == 1 and result[0] != ref:
        result = "".join(result)
        data.append(result)
    return data

left = sys.argv[1]
left_h = open(left)
outfile_l = open(left+".table", "w")
header1 = "loci\tpos\tref\tread\tdepth\tA\tC\tG\tT\tA_freq\t"
header2 = "C_freq\tG_freq\tT_freq\tnon_ref\n"
header = header1 + header2

outfile_l.write(header)
for line in left_h:
    bits = line.split("\t")
    bits[4] = bits[4].split(':')[1]
    bits[5] = bits[5].split(':')[1]
    bits[6] = bits[6].split(':')[1]
    bits[7] = bits[7].split(':')[1]
    with_percents = cal_percents(bits[:])  # send copy of list
    # now add var column
    with_var = filter_data(with_percents[:])
    with_var.insert(3, "Fwd")
    outfile_l.write("\t".join(with_var)+"\n")
left_h.close()
outfile_l.close()

# other file
right = sys.argv[2]
outfile_r = open(right+".table", "w")
outfile_r.write(header)
right_h = open(right)
for line in right_h:
    bits = line.split("\t")
    bits[4] = bits[4].split(':')[1]
    bits[5] = bits[5].split(':')[1]
    bits[6] = bits[6].split(':')[1]
    bits[7] = bits[7].split(':')[1]
    with_percents = cal_percents(bits[:])  # send copy of list
    # now add var column
    with_var = filter_data(with_percents[:])
    with_var.insert(3, "Rev")
    outfile_r.write("\t".join(with_var)+"\n")

right_h.close()
outfile_r.close()
