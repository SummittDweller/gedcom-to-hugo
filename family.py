# gedcom-to-hugo family.py

import config
import events
import individuals
import utils

def process_family(opath, i, fam):
  if config.args.verbose:
    print(f"Processing family {i}:")

  fid = utils.get_id(fam)

  # Get records for spouses, FAM record contains pointers to INDI
  #   records but sub_tag knows how to follow the pointers and return
  #   the referenced records instead.
  husband, wife = fam.sub_tag("HUSB"), fam.sub_tag("WIFE")
  if husband:
    hid = utils.get_id(husband)
    hname = f"{husband.name.format()}"
    if config.args.verbose:
      print(f" husband: {hname}")
  if wife:
    wid = utils.get_id(wife)
    wname = f"{wife.name.format()}"
    if config.args.verbose:
      print(f" wife: {wname}")

  # Get _value_ of the MARR/DATE tag
  marr_date = fam.sub_tag_value("MARR/DATE")
  if marr_date:
    if config.args.verbose:
      print(f" marriage date: {marr_date}")

  # access all CHIL records, sub_tags method returns list (possibly empty)
  children = fam.sub_tags("CHIL")
  for child in children:
    # print name and date of birth
    if config.args.verbose:
      print(f" child: {child.name.format()}")
    birth_date = child.sub_tag_value("BIRT/DATE")
    if birth_date:
      if config.args.verbose:
        print(f" birth date: {birth_date}")

    cid = utils.get_id(child)
    with utils.open_md(cid, 'a') as md:
      md.write(f"parentsFamily: \n")
      md.write(f"  - id: {fid} \n")

      if wife:
        md.write(f"    mother: \n")
        md.write(f"      id: {wid} \n")
        md.write(f"      name: {wname} \n")

      if husband:
        md.write(f"    father: \n")
        md.write(f"      id: {hid} \n")
        md.write(f"      name: {hname} \n")

      md.write("--- \n")  # write the closing marks for the front matter

  # repeat the children loop this time writing lists of children to the father
  if husband:
    with utils.open_md(hid, 'a') as md:
      md.write(f"children: \n")
      for child in children:
        cid = utils.get_id(child)
        block = individuals.read_individual_ref(cid)
        md.write(block)

      md.write("--- \n")  # write the closing marks for the front matter

  # repeat the children loop this time writing lists of children to the mother
  if wife:
    with utils.open_md(wid, 'a') as md:
      md.write(f"children: \n")
      for child in children:
        cid = utils.get_id(child)
        block = individuals.read_individual_ref(cid)
        md.write(block)

      md.write("--- \n")  # write the closing marks for the front matter
