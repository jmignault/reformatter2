#!/usr/bin/env python
import os
import argparse
import datetime
from glob import glob
from pathlib import PurePath

# converter functions. Must take 2 arguments: filename and output directory.
def tif2pdf(fn, pdir):
   # outf = os.path.join(pdir, os.path.basename(fn) + '.pdf')
   cdir = os.getcwd()
   os.chdir(pdir)
   globs = glob("*.tif")
   globs.sort()
   cmdstr = f'magick -density 120 -quality 10 -compress jpeg {" ".join(globs)} ../access/{os.path.basename(fn)}'
   print(f'Converting {len(globs)} files, please wait...')
   os.system(cmdstr)
   os.chdir(cdir)
   
# dictionary of format conversions: keys are extensions, value is function to call for conversion 
formats = {'.tif':tif2pdf }

# make a list of extensions
fkeys = list(formats.keys())

# define arguments and parse them
fld = os.getcwd()
parser = argparse.ArgumentParser(description='Convert a folder of files to pdf format.')
parser.add_argument('folder', help="Folder containing files to be converted")

aggies = parser.parse_args()

# set up logfile
fname = os.getcwd() if aggies.folder == '.' else aggies.folder
dname = os.path.basename(os.path.normpath(fname))
tstamp = datetime.date.strftime(datetime.datetime.now(), "%y%m%d%M%S")
logfn = os.path.join(os.path.normpath(aggies.folder),'..', f"{tstamp}_{dname}_log.txt")
logf = open(logfn, 'w', encoding="utf-8")

# figure out how to get the right directory to save files to depending
# on whether output is in mirror dir structure or in place.

for path, subdir, files in os.walk(fname):

    if os.path.basename(path) == 'master' and files:
      procdir = os.path.join(os.path.normpath(path), '../access')
      if not(os.path.exists(procdir)):
        os.mkdir(procdir)

      # get a full path to pass to function
      fn = os.path.join(path, files[0])
      # get the file extension
      ext = os.path.splitext(fn)[-1].lower()
      # calculate a timestamp for the logfile
      lstamp = datetime.date.strftime(datetime.datetime.now(), "%m-%d-%y:%M:%S")

      # does file need conversion?
      if ext in fkeys:
         # yes, print a msg & call function associated with the extension
         try:
            print(f"Converting {path}")
            # outf = os.path.join(procdir, os.path.basename(fn) + '.pdf')
            pdfpath = PurePath(fn)
            pdffn = os.path.join(procdir, pdfpath.parts[1] + '.pdf')
            formats[ext](pdffn, path)
            logstr = f"{lstamp}: Converted {path} to pdf\n"
            logf.write(logstr)
         except BaseException as err:
            logf.write(f"{lstamp}:Could not convert {fn}: {err}")
         continue
      # not converting, log that file was skipped
      else:
         logf.write(f"{lstamp}: Skipped {fn}\n")

logf.close()

   
# dictionary of format conversions: keys are extensions, value is function to call for conversion 
formats = {'.tif':tif2pdf }

# make a list of extensions
fkeys = list(formats.keys())

# define arguments and parse them
fld = os.getcwd()
parser = argparse.ArgumentParser(description='Convert a folder of files to pdf format.')
parser.add_argument('folder', help="Folder containing files to be converted")

aggies = parser.parse_args()

# set up logfile
fname = os.getcwd() if aggies.folder == '.' else aggies.folder
dname = os.path.basename(os.path.normpath(fname))
tstamp = datetime.date.strftime(datetime.datetime.now(), "%y%m%d%M%S")
logfn = os.path.join(os.path.normpath(aggies.folder),'..', f"{tstamp}_{dname}_log.txt")
logf = open(logfn, 'w', encoding="utf-8")

# figure out how to get the right directory to save files to depending
# on whether output is in mirror dir structure or in place.

for path, subdir, files in os.walk(fname):

    if os.path.basename(path) == 'master' and files:
      procdir = os.path.join(os.path.normpath(path), '../access')
      if not(os.path.exists(procdir)):
        os.mkdir(procdir)

      # get a full path to pass to function
      fn = os.path.join(path, files[0])
      # get the file extension
      ext = os.path.splitext(fn)[-1].lower()
      # calculate a timestamp for the logfile
      lstamp = datetime.date.strftime(datetime.datetime.now(), "%m-%d-%y:%M:%S")

      # does file need conversion?
      if ext in fkeys:
         # yes, print a msg & call function associated with the extension
         try:
            print(f"Converting {path}")
            # outf = os.path.join(procdir, os.path.basename(fn) + '.pdf')
            pdfpath = PurePath(fn)
            pdffn = os.path.join(procdir, pdfpath.parts[1] + '.pdf')
            formats[ext](pdffn, path)
            logstr = f"{lstamp}: Converted {path} to pdf\n"
            logf.write(logstr)
         except BaseException as err:
            logf.write(f"{lstamp}:Could not convert {fn}: {err}")
         continue
      # not converting, log that file was skipped
      else:
         logf.write(f"{lstamp}: Skipped {fn}\n")

logf.close()
