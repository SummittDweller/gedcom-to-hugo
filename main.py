# gedcom-to-hugo main.py

import config
import os
import sys
import individuals
import family
import argparse
import utils
from ged4py.parser import GedcomReader


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

  # Initialize the command parser
  parser = argparse.ArgumentParser(description='Generate Hugo static site pages from Gedcom .ged export.')
  parser.add_argument("gedfile", type=str, help="Path of the .ged export for processing.")
  parser.add_argument("-o", "--outdir", type=str, help="Path to the directory where page files will be created.", default="../the-Helge-Project/content/individuals/")
  parser.add_argument("-l", "--limit", type=int, help="Limit processing to the first 'limit' individuals.", default=100000)
  parser.add_argument("-s", "--single", type=str, help="Specific ID (lowercase 'i' followed by 5 digits)   of one individual to be processed. All others are ignored.", default=0)
  parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")

  # Parse the command line arguments
  args = parser.parse_args()
  config.args = args

  # Does the .ged file exist?
  if not os.path.exists(args.gedfile):
    sys.exit(f"Sorry, file '{args.gedfile}' was not found.")

  # Create outdir directory if it does not exist
  opath = args.outdir
  if not os.path.exists(opath):
    os.makedirs(opath)
    if args.verbose:
      print(f"The new '{opath}' directory is created!")
  config.opath = opath

  # Open the args.gedfile file to parse...
  with GedcomReader(args.gedfile) as parser:

    # iterate over each INDI record in the gedcom export file
    for i, indi in enumerate(parser.records0("INDI")):
      id = utils.get_id(indi)
      if args.verbose:
        print(f"{id}: {indi.name.format()}")

      # skip if we are above our "limit" unless this individual is specified as the "single" for processing
      if i > args.limit and id != args.single:
        continue;

      # create the individual's .md file and return his/her "ref" data
      iref = individuals.make_individual(opath, i, id, indi)

    # now, iterate over each FAM record in the gedcom export file
    for i, fam in enumerate(parser.records0("FAM")):
      fref = family.process_family(opath, i, fam)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
