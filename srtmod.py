#!/usr/bin/env python3
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

import sys
import datetime
import argparse
from itertools import groupby
from collections import namedtuple

subTitle = namedtuple('subTitle', 'number start end content')

def parseArgs():
	parser = argparse.ArgumentParser(prog='srtmod.py',description='SRT Subtitles Modifier')
	parser.add_argument(
		'-i',
		'--input-file',
		metavar='input_file',
		required=True
	)
	parser.add_argument(
		'-o',
		'--output-file',
		metavar='output_file',
		required=True
	)
	parser.add_argument(
		'-t',
		'--timeskip',
		metavar='timeskip',
		required=True
	)
	parser.add_argument(
		'-n',
		'--negative-timeskip',
		action='store_true',
		required=False
	)
	return parser.parse_args()

def strToDateTime(str):
	return datetime.datetime.strptime(str, "%H:%M:%S,%f")

def dateTimeToStr(dateTime):
	return dateTime.strftime("%H:%M:%S,%f")[0:12]	# Return first 12 characters (microseconds screw up the output)

def timePlusDelta(sourceTime, osTimeDelta):
	return strToDateTime(sourceTime) + osTimeDelta

def timeMinusDelta(sourceTime, osTimeDelta):
	return strToDateTime(sourceTime) - osTimeDelta

def extractSub(sub):
	sub = [x.strip() for x in sub]
	number, start_end, *content = sub # py3 syntax
	start, end = start_end.split(' --> ')
	return subTitle(number, start, end, content)

def writeSubs(opTimeDelta,subs,f,offsetTime):
	for i in range(len(subs)):
		f.write("%s\n" % subs[i].number)						# Subtitle number

		# Who the hell decided on the order of arguments for timedelta. WTF?
		# class timedelta( 	[days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]]]]]]])
		offsetTimeDelta = datetime.timedelta(
			0,
			offsetTime.second,
			offsetTime.microsecond,
			0,
			offsetTime.minute,
			offsetTime.hour
		)
		# Now process start and end
		newStart = dateTimeToStr(timePlusDelta(subs[i].start, offsetTimeDelta))
		newEnd = dateTimeToStr(timePlusDelta(subs[i].end, offsetTimeDelta))

		f.write("%s --> %s\n" % (newStart, newEnd))					# Time subtitle should stay on for
		for l in range(len(subs[i].content)):
			f.write("%s\n" % subs[i].content[l])					# Text of subtitle (may be multiline post conversion)
		f.write("\n")

def main():
	args = parseArgs()

	print('inFile = {}'.format(args.input_file))
	print('outFile = {}'.format(args.output_file))
	print('offset = {}'.format(args.timeskip))
	print('NegativeTimeSkip = {}'.format(args.negative_timeskip))

	opTimeDelta = timePlusDelta
	if args.negative_timeskip:
		opTimeDelta = timeMinusDelta
	offsetTime = strToDateTime(args.timeskip)

	# Get each line in (from the input file)
	with open(args.input_file, "r") as f:
		res = [list(g) for b,g in groupby(f, lambda x: bool(x.strip())) if b]

	subs = []
	for sub in res:
		if len(sub) < 3: # not strictly necessary, but better safe than sorry
			continue
		subs.append(extractSub(sub))

	# Create the destination file
	with open(args.output_file, "w") as f:
		# Now process each line
		writeSubs(opTimeDelta,subs,f,offsetTime)

if __name__ == '__main__':
	main()


