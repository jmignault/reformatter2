#!/usr/bin/env python
import os
import argparse
import datetime
from glob import glob
from pathlib import PurePath

# converter functions. Must take 2 arguments: filename and output directory.
def tif2pdf(fn, pdir):
    # outf = os.path.join(pdir, os.path.basename(fn) + '.pdf')
    cmd_prefix = 'convert -density 120 -quality 10 -compress jpeg'
    cdir = os.getcwd()
    os.chdir(pdir)
    globs = glob("*.tif")
    globs.sort()
    num_imgs = len(globs)
    if num_imgs < 200:
      cmdstr = f'{cmd_prefix} {" ".join(globs)} ../access/{os.path.basename(fn)}'
      print(f'Combining {len(globs)} files, please wait...')
      os.system(cmdstr)
    else:
      #cut into two slices
      first_set = globs[:num_imgs//2]
      second_set = globs[num_imgs//2:]

      # define filenames for broken-out files
      first_set_fn = f'../access/{os.path.basename(fn)[0:-4]}-1.pdf'
      second_set_fn = f'../access/{os.path.basename(fn)[0:-4]}-2.pdf'

      try:
          # make 2 PDFs
          print(f'Creating {first_set_fn} by combining {len(first_set)} files, please wait')
          first_cmd = f'{cmd_prefix} {" ".join(first_set)} {first_set_fn}'
          os.system(first_cmd)
          print(f'Creating {second_set_fn} by combining {len(second_set)} files, please wait')
          second_cmd = f'{cmd_prefix} {" ".join(second_set)} {second_set_fn}'
          os.system(second_cmd)
      except BaseException as err:
          print(f"{lstamp}:Could not convert {fn}: {err}")
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

for path, subdir, files in os.walk(fname):

    if files:# get a full path to pass to function
        fn = os.path.join(path, files[0])
        # get the file extension
        ext = os.path.splitext(fn)[-1].lower()
        # calculate a timestamp for the logfile
        lstamp = datetime.date.strftime(datetime.datetime.now(), "%m-%d-%y:%M:%S")

    # does file need conversion?
        if ext in fkeys:
            # yes, print a msg & call function associated with the extension
            procdir = os.path.join(os.path.normpath(path), '../access')
            if not(os.path.exists(procdir)):
                os.mkdir(procdir)
            try:
                print(f"Creating access files for {path}")
                # outf = os.path.join(procdir, os.path.basename(fn) + '.pdf')
                pdfpath = PurePath(fn)
                pdffn = os.path.join(procdir, pdfpath.parts[1] + '.pdf')
                formats[ext](pdffn, path)
                logstr = f"{lstamp}: Converted {path} to pdf\n"
                logf.write(logstr)            
            except BaseException as err:
                logf.write(f"{lstamp}:Could not convert {fn}: {err}")
                
            else:
                # not converting, log that file was skipped
                logf.write(f"{lstamp}: Skipped {fn}\n")
logf.close()

