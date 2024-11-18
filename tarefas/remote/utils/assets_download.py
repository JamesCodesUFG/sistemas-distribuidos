import pystac

STAC_URL = 'https://data.inpe.br/bdc/stac/v1/'

catalog = pystac.Catalog.from_file(STAC_URL)

print(list(catalog.get_collections()))