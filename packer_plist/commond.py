#!/usr/bin/python
# -*- coding: utf8 -*-
# import os,sys

import os, sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main(imagedir, outplistdir, plistName, format):
  comend = "/usr/bin/Texturepacker/Texturepacker"#'texturepacker'
  filelist = os.listdir(imagedir)
  
  allImage = ""
  for n in range(len(filelist)):
    if filelist[n] == ".DS_Store":
      continue
    tmp = imagedir + os.sep + filelist[n]
    print tmp
    allImage = allImage + " " + tmp
  cmdtmp = comend

  cmdtmp = cmdtmp + " " + allImage +\
           " --data " + outplistdir + os.sep + plistName + ".plist"\
           " --sheet " + outplistdir + os.sep + plistName + ".pvr.ccz"\
           " --opt " + format + " --dither-fs-alpha"\
           " --size-constraints AnySize"

  os.system(cmdtmp)

if __name__=="__main__":
  argv1 = sys.argv[1]
  argv2 = sys.argv[2]
  argv3 = sys.argv[3]
  argv4 = sys.argv[4]
  print argv1
  print argv2
  print argv3
  print argv4
  
  main(argv1, argv2, argv3, argv4)