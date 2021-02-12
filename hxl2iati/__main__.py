import hxl2iati.convert, sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <url_or_filename>".format(sys.argv[0]), file=sys.stderr)
        sys.exit(2)

    converter = hxl2iati.convert.HXL2IATI(
        output=sys.stdout,
        reporting_org_name="OCHA Somalia",
        recipient_country_name="Somalia",
        recipient_country_code="SO",
        default_start_date="2020-11-01",
        default_update_date="2020-11-30",
    )
    converter.convert(sys.argv[1], allow_local=True)
