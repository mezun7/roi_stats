import codecs
import csv

from roi.models import Region, RegionAlias


def import_region_aliases(csv_file):
    reader = csv.DictReader(codecs.iterdecode(csv_file, 'utf-8'))
    region_aliases = []

    for row in reader:
        try:
            region = Region.objects.get(short_name=row['region_name'])
            alias = row['alias']
            region_alias = RegionAlias()
            region_alias.region = region
            region_alias.alias = alias
            region_aliases.append(region_alias)
        except Region.DoesNotExist:
            print(f'Could not find - {row["region_name"]}')

    RegionAlias.objects.bulk_create(region_aliases)
