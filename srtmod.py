#
# Python routine to add an offset to a .srt file.
#
# It's normal to find a subtitle file that doesn't quite have the right timing for a movie.
# This routine allows you to take an existing .srt file and add a time offset.
#
# Written in Python3
#
# Usage:
#		python3 srtmod.py -i <inputfile.srt> -o <outputfile.srt> -t <offset>
#
#		the Offset is in the form HH:MM:SS,mmm
#
# The idea for the general parsing routing taken from a posting by roippi (http://stackoverflow.com/users/2581969/roippi)
#  http://stackoverflow.com/questions/23620423/parsing-a-srt-file-with-regex/23620587#23620587
#
# Licensed under the Creative Commons license (in so far as these are terms on StackOverflow)
#
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Jon Machtynger / Feb 2015
#

from datetime import datetime
from itertools import groupby
from collections import namedtuple
import sys
import getopt

import datetime

def print_usage():
	print("\nsrtmod.py -i <Inputfname.srt> -o <OutputFname.srt> -t 'HH:MM:SS,mmm'\n")
	sys.exit(0)

def strToDateTime(str):
	return datetime.datetime.strptime(str, "%H:%M:%S,%f")

def dateTimeToStr(dateTime):
	return dateTime.strftime("%H:%M:%S,%f")[0:12]	# Return first 12 characters (microseconds screw up the output)


# Who the hell decided on the order of arguments for timedelta. WTF?
# class timedelta( 	[days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]]]]]]])
def timePlusDelta(sourceTime, osTime):
	dt=strToDateTime(sourceTime)
	return dt + datetime.timedelta(0, osTime.second, osTime.microsecond, 0, osTime.minute, osTime.hour)
	
try:
	opts, argo = getopt.getopt(sys.argv[1:],"i:o:t:")
except getopt.GetoptError:
	print_usage()
	
inFile = None
outFile = None
offset = None

for o,a in opts:
	if o == "-o":
		outFile = a
	elif o == "-i":
		inFile = a
	elif o == "-t":
		offset = a

print("inFile = ", inFile)
print("outFile = ", outFile)
print("offset = ", offset)

if inFile is None or outFile is None or offset is None:
	print_usage()

offsetTime = strToDateTime(offset)

# Get each line in (from the input file)
with open(inFile, "r") as f:
	res = [list(g) for b,g in groupby(f, lambda x: bool(x.strip())) if b]

subTitle = namedtuple('subTitle', 'number start end content')
subs = []
for sub in res:
	if len(sub) >= 3: # not strictly necessary, but better safe than sorry
		sub = [x.strip() for x in sub]
		number, start_end, *content = sub # py3 syntax
		start, end = start_end.split(' --> ')
		subs.append(subTitle(number, start, end, content))
f.close()

# Create the destination file
f = open(outFile, "w")

# Now process each line
for i in range(len(subs)):	
	f.write("%s\n" % subs[i].number)						# Subtitle number

	# Now process start and end
	newStart = dateTimeToStr(timePlusDelta(subs[i].start, offsetTime))
	newEnd = dateTimeToStr(timePlusDelta(subs[i].end, offsetTime))

	f.write("%s --> %s\n" % (newStart, newEnd))					# Time subtitle should stay on for
	for l in range(len(subs[i].content)):
		f.write("%s\n" % subs[i].content[l])					# Text of subtitle (may be multiline post conversion)
	f.write("\n")
f.close()


