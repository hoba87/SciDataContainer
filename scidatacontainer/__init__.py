##########################################################################
# Copyright (c) 2023 Reinhard Caspary                                    #
# <reinhard.caspary@phoenixd.uni-hannover.de>                            #
##########################################################################
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##########################################################################
#
# This package provides the Scientific Data Container as class Container
# which may be stored as a ZIP package containing items (files). Based
# on their file extension, the following item types are supported:
#
# .bin:  Raw bytes data file
# .txt:  Encoded text file (default encoding: UTF-8)
# .log:  Encoded text file (default encoding: UTF-8)
# .pgm:  Encoded text file (default encoding: UTF-8)
# .json: JSON file
# .png:  PNG image (requires Python module cv2)
#
# Users may register other file extensions to file conversion classes
# using the function register(). See package fileimage as an example for
# such a conversion class.
#
##########################################################################

from .filebase import FileBase, TextFile, JsonFile
from .container import DataContainer, timestamp

suffixes = {
    "json": JsonFile,
    "bin": FileBase,
    "txt": TextFile,
    "log": TextFile,
    "pgm": TextFile,
    }

# Try to import image file formats requiring the Python module cv2
try:
    from .fileimage import PngFile
    suffixes["png"] = PngFile
except:
    pass


def register(suffix, fclass):

    """ Register a suffix to a conversion class. """

    # Suffix json is immutable
    if suffix == "json":
        raise RuntimeError("Suffix 'json' is immutable!")
    
    # Simple sanity check for the class interface
    for method in ("encode", "decode", "hash"):
        if not hasattr(fclass, method) or not callable(getattr(fclass, method)):
            raise RuntimeError("No method %s() in class for suffix '%s'!" \
                               % (method, suffix))

    # Register suffix
    suffixes[suffix] = fclass


# Inject certain known file formats into the container class
class Container(DataContainer):

    """ Scientific data container. """

    _suffixes = suffixes


