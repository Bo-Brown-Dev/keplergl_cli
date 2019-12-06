"""Console script for kepler_quickvis."""
import sys
from pathlib import Path

import click
import geopandas as gpd

from keplergl_quickvis import Visualize


@click.command()
@click.option(
    '--reproject',
    is_flag=True,
    default=False,
    show_default=True,
    help=
    'Attempt to reproject source data. This will only work if the source files include metadata on their projection'
)
@click.option(
    '--api_key',
    type=str,
    default=None,
    help=
    'Mapbox API Key. Must be provided on the command line or exist in the MAPBOX_API_KEY environment variable.'
)
@click.option(
    '--style',
    type=str,
    default='mapbox://styles/mapbox/outdoors-v11',
    show_default='mapbox://styles/mapbox/outdoors-v11',
    help=
    'Mapbox Style. For example "mapbox://styles/mapbox/streets-v11".'
)
@click.argument('files', nargs=-1, required=True, type=click.Path(exists=True))
def main(reproject, api_key, style, files):
    """Console script for keplergl_quickvis."""
    vis = Visualize(api_key=api_key, style=style)

    # For each file, try to load data with GeoPandas
    for file_name in files:
        layer_name = Path(file_name).stem
        gdf = gpd.read_file(file_name)
        if reproject:
            gdf = gdf.to_crs(epsg=4326)

        vis.add_data(gdf, layer_name)

    vis.render(open_browser=True, read_only=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
