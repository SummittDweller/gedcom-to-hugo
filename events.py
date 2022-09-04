# This is example 3 pulled from ged4py-readthedocs-io-en-latest.pdf

import config
import re
import utils
from ged4py.date import DateValueVisitor


class DateFormatter(DateValueVisitor):
  """Visitor class that produces string representation of dates."""

  def visitSimple(self, date):
    return f"{date.date}"

  def visitPeriod(self, date):
    return f"from {date.date1} to {date.date2}"

  def visitFrom(self, date):
    return f"from {date.date}"

  def visitTo(self, date):
    return f"to {date.date}"

  def visitRange(self, date):
    return f"between {date.date1} and {date.date2}"

  def visitBefore(self, date):
    return f"before {date.date}"

  def visitAfter(self, date):
    return f"after {date.date}"

  def visitAbout(self, date):
    return f"about {date.date}"

  def visitCalculated(self, date):
    return f"calculated {date.date}"

  def visitEstimated(self, date):
    return f"estimated {date.date}"

  def visitInterpreted(self, date):
    return f"interpreted {date.date} ({date.phrase})"

  def visitPhrase(self, date):
    return f"({date.phrase})"


def get_events_info(indi):
  event_list = []
  format_visitor = DateFormatter()

  events = indi.sub_tags("BIRT", "CHR", "DEAT", "BURI", "ADOP", "EVEN")
  for event in events:
    place = event.sub_tag_value("PLAC")
    date = event.sub_tag_value("DATE")  # Some event types like generic EVEN can define TYPE tag
    event_type = event.sub_tag_value("TYPE")   # pass a visitor to format the date
    if date:
      d = date.accept(format_visitor)
    else:
      d = "N/A"
    date_str = utils.clean_output(d, "date")
    event_list.append({"tag": event.tag, "date": date_str, "note": utils.return_empty(event_type), "place": utils.return_empty(place)})
    if config.args.verbose:
      print(f"tag: {event.tag} date: {date_str} note: {event_type} place: {place}")

  return event_list


def get_event_date(dict_list, tag):
  for event in dict_list:
    if event["tag"] == tag:
      if event["date"]:
        d = event["date"]
        return utils.clean_output(d, "date")

  return ""

def get_event_place(dict_list, tag):
  for event in dict_list:
    if event["tag"] == tag:
      if event["place"]:
        p = event["place"]
        return re.sub('@.+@', '', p).strip(" ")

  return ""
