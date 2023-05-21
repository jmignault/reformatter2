# Reformatter 2 #

Python script to convert files in place in a folder. The script walks
the folder looking for subfolders containing files. When it finds one
it creates a folder one level up called 'access' and writes converted
files to it. A timestamped logfile is written to the directory from
which the script is run.

The script itself can be in any directory, but must be run from the
directory containing the directory to convert:

`c:\Documents> python c:\reformatter2.py testtiffs`

for example.

The script requires that the `convert` command line tool which is part
of the `Imagemagick` graphics software package be installed.
`convert` is a headless executable which is part of the default
installation of [Imagemagick.](https://www.imagemagick.org
"Imagemagick site")

Once installed convert needs to be on the executable path. This is
done by appending its directory to the PATH environment
variable. 

The script requires Python 3 and uses only standard Python 3
libraries. It was developed and tested using Python 3.7.3.
