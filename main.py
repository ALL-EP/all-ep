#

# read in GTF file
f = open('ref.txt','r')
lines = f.readlines()
f.close()

zero_c = 0
gtf = {}

# parse GTF file and calculate length of coding region for each gene
# ignore introns based on start and stop codons
for line in lines[1:]:
	sl = line.strip().split('\t')
	temp = 0
	if sl[6] == sl[7] and sl[0] not in gtf.keys():
		gtf[sl[0]] = 0
		zero_c += 1
	else:
		estart = sl[9].split(',')
		estop = sl[10].split(',')
		start = int(sl[6])
		stop = int(sl[7])

		for n in range(0,max(len(estart)-1,1)):
			if start >= int(estart[n]) and stop <= int(estop[n]):
				temp = stop - start
			elif (start >= int(estart[n]) and start <= int(estop[n]) and stop >= int(estop[n])):
				temp = temp + int(estop[n]) - int(estart[n])
			elif start < int(estart[n]) and stop >= int(estop[n]):
				temp = temp + int(estop[n]) - int(estart[n])
			elif start < int(estart[n]) and stop <= int(estop[n]) and stop > int(estart[n]):
				temp = temp + stop - int(estart[n])
		# if a longer CDS length is calculated for the same gene, replace it
		if sl[0] in gtf.keys():
			if gtf[sl[0]] < temp:
				gtf[sl[0]] = temp
		else:
			gtf[sl[0]] = temp

# outputs gene name:CDS length
fout = open('output.txt','w')
fout.write(str(gtf))
fout.close()