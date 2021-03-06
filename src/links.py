# This class is for storing and processing asset links.

# Internal imports
from zettels import Zettels

# External imports
import os


class Links:
    def __init__(self):
        # These lists are parallel, except for self.broken.
        self.originals = []  # List of tuples of (zettel path, original asset path). The original asset path is the asset path as it appears in the zettel.
        self.formatted = []  # The asset paths in a modified form that is easier for the program to use.
        self.names = []      # The names of the assets (the last part of the asset paths).
        self.broken = []     # Same as self.originals, but only the tuples with the broken asset paths.

    # Parameter zettel_path must be an abs path.
    def append(self, asset_path, asset_name, zettel_path):
        self.originals.append((zettel_path, asset_path))
        self.names.append(asset_name)
        self.formatted.append(format_link(asset_path, zettel_path))
        # Determine whether the link is broken.
        if not os.path.exists(self.formatted[-1]):
            self.broken.append((zettel_path, asset_path))

    def add(self, links_object):
        for i, _ in enumerate(links_object.originals):
            self.originals.append(links_object.originals[i])
            self.formatted.append(links_object.formatted[i])
            self.names.append(links_object.names[i])
        for link in links_object.broken:
            self.broken.append(link)

    # If all the lists are empty, return True.
    def isEmpty(self):
        if len(self.originals):
            return False
        return True

    # Return a Zettels object of the broken asset links.
    def get_broken(self):
        broken_link_z = Zettels()
        for link in self.broken:
            broken_link_z.append(path=link[0], link=link[1])

        return broken_link_z


# Get the absolute path of an asset.
# asset_path is a relative file path.
# zettel_path is the abs path of the zettel that contains asset_path.
def get_abspath(asset_path, zettel_path):
    zettel_dir = os.path.split(zettel_path)[0]
    abs_asset_path = os.path.join(zettel_dir, asset_path)
    abs_asset_path = os.path.abspath(abs_asset_path)
    if os.path.exists(abs_asset_path):
        return abs_asset_path
    else:
        return asset_path


# Change the form of an asset link to make it easier to use.
# Broken links will not be made absolute.
# zettel_path is the abs path of the zettel that contains asset_path.
def format_link(asset_path, zettel_path):
    # Remove 'file://' from the beginning of any asset links that have it.
    if asset_path.startswith('file://'):
        asset_path = asset_path[7:]
    # Make any relative asset links absolute.
    if not os.path.isabs(asset_path):
        asset_path = get_abspath(asset_path, zettel_path)
    # Replace all instances of '\\' with '/'.
    asset_path = asset_path.replace('\\', '/')

    return asset_path
