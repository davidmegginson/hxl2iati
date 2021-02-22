import datetime, dateutil, hashlib, hxl, hxl2iati.writer, re

from hxl2iati.mapping import DAC_SECTOR_INFO, CLUSTER_INFO

class ConversionException (Exception):

    def __init__(self, message):
        super().__init__(message)


class HXL2IATI:
    
    REQUIRED_HASHTAGS = [
        "#org+impl",
        "#sector",
        "#activity",
        "#adm1+name",
        "#date+start",
        "#date+end",
        "#status",
    ]
    """ Required columns to do this processing """

    
    def __init__ (self, output, reporting_org_name, recipient_country_name, recipient_country_code, default_start_date, default_update_datetime):
        self.reporting_org_name = reporting_org_name
        self.recipient_country_name = recipient_country_name
        self.recipient_country_code = recipient_country_code
        self.default_start_date = default_start_date
        self.default_update_datetime = default_update_datetime

        self.xmlout = hxl2iati.writer.XMLWriter(output=output)

        
    def convert (self, url_or_filename, allow_local=False):
        """ Top-level method to convert a HXLated 3W to IATI

        """

        # open the data source (usually a URL)
        source = hxl.data(url_or_filename, allow_local=allow_local)

        # check that the required hashtags are present
        check_hashtags(source, self.REQUIRED_HASHTAGS)

        self.xmlout.start_document()

        self.xmlout.start_block("iati-activities", {
            "generated-datetime": datetime.datetime.now().isoformat(),
            "version": "2.03",
        })

        for row in source:
            self.do_activity(row)

        self.xmlout.end_block("iati-activities")

        self.xmlout.end_document()

        
    def do_activity(self, row):
        """ convert a HXLated 3W row to an iati-activity """

        # TODO send the 3W's actual datetime
        self.xmlout.start_block("iati-activity", {
            "xml:lang": "en",
            "default-currency": "USD",
            "last-updated-datetime": self.default_update_datetime,
            "humanitarian": "1",
        })

        self.xmlout.simple_element("iati-identifier", content=make_identifier(row))

        # TODO make reporting org configurable
        self.do_narrative("reporting-org", {
            "ref": "TODO",
            "type": "TODO",
        }, self.reporting_org_name)

        if row.get("#activity"):
            self.do_narrative("title", {}, row.get("#activity"))
            self.do_narrative("description", {}, row.get("#activity"))

        if row.get("#org+impl"):
            self.do_narrative("participating-org", {
                "role": "4",
                "ref": "TODO",
                "type": "TODO",
            }, row.get("#org+impl"))

        # TODO add org type
        if row.get("#org+prog"):
            self.do_narrative("participating-org", {
                "role": "2",
                "ref": "TODO",
                "type": "TODO",
            }, row.get("#org+prog"))

        if row.get("#org+funding"):
            self.do_narrative("participating-org", {
                "role": "1",
                "ref": "TODO",
                "type": "TODO",
            }, row.get("#org+funding"))

        self.xmlout.simple_element("activity-status", {
            "code": row.get("#status", default=""),
        })

        d = fix_date(row.get("#date+start"), self.default_start_date)
        if d:
            self.xmlout.simple_element("activity-date", {
                "iso-date": d,
                "type": "2",
            })

        d = fix_date(row.get("#date+end"), self.default_start_date)
        if d:
            self.xmlout.simple_element("activity-date", {
                "iso-date": d,
                "type": "4",
            })

        self.do_narrative("recipient-country", {
            "code": self.recipient_country_code,
            "percentage": "100",
        }, self.recipient_country_name)

        if row.get("#sector"):
            info = CLUSTER_INFO.get(row.get("#sector"))
            if info:
                self.do_narrative("sector", {
                    "code": info["code"],
                    "vocabulary": "10",
                }, info["name_en"])
                for dac_code in info["dac_codes"]:
                    dac_info = DAC_SECTOR_INFO[dac_code]
                    self.do_narrative("sector", {
                        "code": dac_code,
                        "vocabulary": "1",
                    }, dac_info["name_en"])

        self.xmlout.end_block("iati-activity")

        
    def do_narrative (self, name, atts={}, content=None):
        if content is None:
            self.xmlout.simple_element(name, atts)
        else:
            self.xmlout.start_block(name, atts)
            self.xmlout.simple_element("narrative", content=content)
            self.xmlout.end_block(name)


# Helper functions

def fix_date (s, default_date=None):
    try:
        return dateutil.parser.parse(s).isoformat()[:10]
    except:
        return default_date


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


# end
