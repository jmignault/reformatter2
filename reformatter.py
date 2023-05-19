#!/usr/bin/env python
import os
import argparse
import datetime

# converter functions. Must take 2 arguments: filename and output directory.
def wp_to_pdf(fn, pdir):
   cmdstr = 'soffice --convert-to pdf --outdir "' + pdir + '" "' + fn + '"'
   os.system(cmdstr)
  
# dictionary of format conversions: keys are extensions, value is function to call for conversion 
formats = {'.doc':wp_to_pdf, '.docx':wp_to_pdf, '.wp':wp_to_pdf, '.wpd':wp_to_pdf, '.pub':wp_to_pdf, '.txt':wp_to_pdf}

# make a list of extensions
fkeys = list(formats.keys())
# define arguments and parse them
parser = argparse.ArgumentParser(description='Convert a folder of files to pdf format.')
parser.add_argument('infiles', help="Folder containing files to be converted")

args = parser.parse_args()

outpath = os.path.join(os.getcwd(), "processed")
if not (os.path.exists(outpath)):
   os.mkdir(outpath)

tstamp = datetime.date.strftime(datetime.datetime.now(), "%m%d%y%M%S")
dname = os.path.basename(os.path.normpath(args.infiles))
logfn = os.path.join(outpath, f"{tstamp}_{dname}_log.txt")

logf = open(logfn, 'w', encoding="utf-8")

for path, subdir, files in os.walk(args.infiles):

   procdir = os.path.join(outpath, os.path.relpath(path, os.path.dirname(args.infiles)))
   if not(os.path.exists(procdir)):
      os.mkdir(procdir)

   for name in files:
      # get a full path to pass to function
      fn = os.path.join(path, name)
      # get the file extension
      ext = os.path.splitext(fn)[-1].lower()
      # calculate a timestamp for the logfile
      lstamp = datetime.date.strftime(datetime.datetime.now(), "%m-%d-%y:%M:%S")
 
      # does file need conversion?
      if ext in fkeys:
         # yes, print a msg & call function associated with the extension
         try:
            print(f"Converting {fn}")
            formats[ext](fn, procdir)
            logstr = f"{lstamp}: Converted {fn} to pdf\n"
            logf.write(logstr)
         except BaseException as err:
            logf.write(f"{lstamp}:Could not convert {fn}: {err}")
         continue
      # not converting, log that file was skipped
      else:
         logf.write(f"{lstamp}: Skipped {fn}\n")

logf.close()


