import datetime, hashlib, hxl

REQUIRED_HASHTAGS = [
    "#org+impl",
    "#sector",
    "#activity",
    "#adm1+name",
    "#date+start",
    "#date+end",
    "#status",
]

class ConversionException (Exception):
    pass

def esc (s):
    """ Escape text for XML content """
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("'", "&apos;").replace('"', "&quot;")

def check_hashtags (source, hashtags):
    """ Check that all the required hashtags are present.
    If not, throw an exception
    """
    missing_columns = []
    for tagspec in hashtags:
      if hxl.model.TagPattern.parse(tagspec).find_column_index(source.columns) is None:
          missing_columns.append(tagspec)
    if missing_columns:
        raise ConversionException("Missing column(s): {}".format(", ".join(missing_columns)))

def make_identifier (row):
    # FIXME not really reliable
    hash = hashlib.md5("|||".join(row.values).encode("utf-8"))
    return "OCHA-3W-SOM-{}".format(hash.hexdigest())

def start_xml (output):
    """ XML frontmatter """
    print("<?xml version=\"1.0\"?>\n\n<iati-activities generated-datetime=\"{}\" version=\"2.03\">".format(datetime.datetime.now().isoformat()), file=output)

def end_xml(output):
    """ XML backmatter """
    print("</iati-activities>", file=output)

def narrative_el(tag, content, output, code=None):
    """ Display a narrative text element, optionally with a code attribute """
    code_string = ""
    if code is not None:
        code_string = " code=\"{}\"".format(esc(str(code)))
    print("    <{tag}{code_string}>\n      <narrative>{content}</narrative>\n    </{tag}>".format(tag=tag, code_string=code_string, content=esc(content)), file=output)

def do_activity(row, output):
    """ convert a HXLated 3W row to an iati-activity """

    # TODO send the 3W's actual datetime
    print("  <iati-activity xml:lang=\"en\" default-currency=\"USD\" last-updated_datetime=\"{}\">".format(esc(datetime.datetime.now().isoformat())), file=output)

    print("    <iati-identifier>{}</iati-identifier>".format(esc(make_identifier(row))), file=output)

    # TODO make reporting org configurable
    narrative_el("reporting-org", "OCHA Somalia", output)

    if row.get("#org+impl"):
        narrative_el("participating-org", row.get("#org+impl"), output, code=4)

    # TODO add org type
    if row.get("#org+prog"):
        narrative_el("participating-org", row.get("#org+prog"), output, code=2)

    if row.get("#org+funding"):
        narrative_el("participating-org", row.get("#org+funding"), output, code=1)

    if row.get("#activity"):
        narrative_el("title", row.get("#activity"), output)

    if row.get("#sector"):
        # TODO add sector code
        narrative_el("sector", row.get("#sector"), output)

    if row.get("#date+start"):
        # TODO check date format
        print("    <activity_date iso_date=\"{}\" code=\"2\"/>".format(esc(row.get("#date+start"))), file=output)

    if row.get("#date+end"):
        # TODO check date format
        print("    <activity_date iso_date=\"{}\" code=\"4\"/>".format(esc(row.get("#date+end"))), file=output)

    # TODO make configurable
    print("    <recipient-country code=\"SO\" percentage=\"100\"/>", file=output)

    print("  </iati-activity>", file=output)

def convert (url_or_filename, output, allow_local=False):
    """ Top-level function to convert HXL to IATI
    """

    # open the data source (usually a URL)
    source = hxl.data(url_or_filename, allow_local=allow_local)

    # check that the required hashtags are present
    check_hashtags(source, REQUIRED_HASHTAGS)

    start_xml(output)

    for row in source:
        do_activity(row, output)

    end_xml(output)
    
