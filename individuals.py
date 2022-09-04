# gedcom-to-hugo individuals.py
import os.path

import config
import events
import utils

# read_individual_ref(id)
# This function reads an individual's file and returns the core or 'ref' portion of the data with extra indentation
def read_individual_ref(id):
  capture = False
  block = "  - "
  count = 0

  with utils.open_md(id, 'r') as md:
    line = md.readline()
    while line:
      if capture:
        if line.startswith("  "):
          if count == 0:
            block += line.strip(" ")
          else:
            block += "  " + line
          count += 1
        else:
          break
      else:
        if line.startswith("ref: "):
          capture = True

      line = md.readline()

  return block

# individual_ref(id, indi)
# This function builds and returns the core or 'ref' portion of the data structure for an individual
def individual_ref(id, indi):
  full_name = indi.name.format()  # got the individuals full name
  events_list = events.get_events_info(indi)
  # Get _value_ of the BIRT/DATE tag and DEAT/DATE tags
  birth = events.get_event_date(events_list, "BIRT")
  death = events.get_event_date(events_list, "DEAT")
  # Build a lastnames: record and write it...
  surname = indi.name.surname.format()
  sex = indi.sex

  ref = { "id": id, "name": full_name, "birth": birth, "death": death, "sex": sex, "surname": surname }
  return ref

# formatted_ref(r)
# Given an individual's raw 'ref' record, 'r', return a string suitable for writing with formatting and indentation
def formatted_ref(r):
  text = f"  id: {r['id']} \n  name: {r['name']} \n  birth: {r['birth']} \n  death: {r['death']} \n  sex: {r['sex']} \n  lastnames: \n    - {r['surname']} \n"
  return text


# make_individual(opath, i, id, indi)
def make_individual(opath, i, id, indi):

  # open a file at {opath}/i<id>.md
  ifile = f"{id}.md"
  ipath = opath + ifile

  events_list = events.get_events_info(indi)

  with utils.open_md(id, 'w') as md:
    md.write("--- \n")      # write the opening marks for the front matter
    full_name = indi.name.format()    # got the individuals full name

    # Get _value_ of the BIRT/DATE tag and DEAT/DATE tags
    birth_date = events.get_event_date(events_list, "BIRT")
    death_date = events.get_event_date(events_list, "DEAT")

    # Build a title: record and write it...
    d = f"({birth_date} - {death_date})"
    dates_string = utils.clean_output(d)

    t = f"{full_name} {dates_string}"
    title = t.strip(" ")
    md.write(f"title: {title} \n")

    # Build an id: record and write it...
    md.write(f"id: {id} \n")
    md.write(f"weight: {i+1} \n")

    # Build a url: record and write it...
    md.write(f"url: '/{id}/' \n")

    # Add a categories: individual record and write it...
    md.write(f"categories: \n  - individual \n")

    # Build a lastnames: record and write it...
    surname = indi.name.surname.format()
    md.write(f"lastnames: \n  - {surname} \n")

    sex = indi.sex

    # Build a ref: section record and write it...
    ref = individual_ref(id, indi)
    md.write(f"ref: \n")
    block = formatted_ref(ref)
    md.write(block)

    # Build an events list...
    event_strings = {"BIRT": "Birth", "DEAT": "Death", "BURI": "Burial", "CHR": "Christening", "ADOP": "Adoption", "EVEN": "Event"}

    if events_list:
      md.write(f"events: \n")
      for event in events_list:
        name = event_strings[event['tag']]
        md.write(f"- name: {name} \n")
        md.write(f"  tag: {event['tag']} \n")
        md.write(f"  notes: {event['note']} \n")
        md.write(f"  date: {event['date']} \n")
        if event['place'] != "None":
          md.write(f"  place: {event['place']} \n")

    # Build a list of related media, OBJE values
    objects = indi.sub_tags("OBJE")

    for o, obj in enumerate(objects):
      oid = utils.get_id(obj)
      mpath = obj.sub_tag_value("FILE")
      media_file = os.path.basename(mpath)
      if o == 0:
        md.write(f"primary_image: {media_file} \n")
        md.write(f"media: \n")
      md.write(f"  - {media_file} \n")

    md.write("--- \n")      # write the closing marks for the front matter


