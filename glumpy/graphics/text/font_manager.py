# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
""" Font Manager """
import os
import numpy as np
from glumpy import data
from glumpy.log import log
from glumpy.gloo.atlas import Atlas
from . sdf_font import SDFFont
from . agg_font import AggFont



class FontManager(object):
    """
    Font Manager

    The Font manager takes care of caching already loaded font. Currently, the only
    way to get a font is to get it via its filename. If the font is not available
    on the local data directory, it will be fetched from the font server which
    lives at https://github.com/glumpy/glumpy-font/.
    """

    # Default atlas
    _atlas = None

    # Font cache
    _cache = {}

    # The singleton instance
    _instance = None


    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def get(cls, filename):
        """
        Get a font from the cache, the local data directory or the distant server
        (in that order).
        """

        filename = data.get(filename)
        dirname  = os.path.dirname(filename)
        basename = os.path.basename(filename)
        if basename in FontManager._cache.keys():
            return FontManager._cache[basename]
        FontManager._cache[basename] = SDFFont(filename, FontManager._atlas)
        return FontManager._cache[basename]


    @property
    def atlas(self):
        """ Texture atlas """

        if FontManager._atlas is None:
            FontManager._atlas = np.zeros((1024,1024),np.float32).view(Atlas)
        return FontManager._atlas


    @property
    def cache(self):
        """ Font cache """

        return FontManager._cache
