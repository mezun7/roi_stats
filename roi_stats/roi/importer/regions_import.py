import codecs
import csv

from roi.models import Region


def import_regions(csv_file):
    reader = csv.DictReader(codecs.iterdecode(csv_file, 'utf-8'))
    regions = []
    for row in reader:
        code = row['code']
        name = row['name']
        short_name = row['short_name']
        try:
            region = Region.objects.get(region_code=code)
            region.short_name = short_name
            region.name = name
            region.save()
        except Region.DoesNotExist:
            region = Region()
            region.name = name
            region.short_name = short_name
            region.region_code = code
            regions.append(region)
    Region.objects.bulk_create(regions)