# srtmod
Modify time offsets for subtitle (srt) files

Python routine to add an offset to a .srt file.

It's normal to find a subtitle file that doesn't quite have the right timing for a movie.
This routine allows you to take an existing .srt file and add a time offset.

Written in Python3

Usage:
               python3 [-h] srtmod.py -i inputfile.srt -o outputfile.srt -t offset [-n]

               the Offset is in the form HH:MM:SS,mmm

               Use '-n' to offset in a negative direction

               '-h' : show srtmod usage
               '-n' : to offset in a negative direction



The idea for the general parsing routing taken from a posting by roippi (http://stackoverflow.com/users/2581969/roippi)
   http://stackoverflow.com/questions/23620423/parsing-a-srt-file-with-regex/23620587#23620587

Licensed under the Creative Commons license (in so far as these are terms on StackOverflow)

http://creativecommons.org/licenses/by-sa/3.0/

Jon Machtynger / Feb 2015
