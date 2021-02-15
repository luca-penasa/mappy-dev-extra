# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis import processing
from qgis.PyQt.QtCore import QCoreApplication
from qgis._core import Qgis, QgsProcessingParameterBoolean, QgsProcessingUtils
from qgis.gui import QgsMessageBar
from qgis.core import (QgsProcessing,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink, QgsProcessingParameterDistance, QgsWkbTypes, QgsFeatureSink,
                       QgsProcessingParameterField)


from qgis.utils import iface

from qgis.PyQt.QtGui import QIcon

from ..utils import resetCategoriesIfNeeded


class MapClipDanglesProcessingAlgorithm(QgsProcessingAlgorithm):
    """
    Helper to assign categorized style to a polygonal layer
    """

    def icon(self):
        return QIcon(':/plugins/qgismappy/mapstyle.png')

    IN_LINES = "IN_CONTACTS"
    IN_POLYGONS = "IN_POLYGONS"

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return MapClipDanglesProcessingAlgorithm()

    def name(self):
        return 'clipdangles'

    def displayName(self):
        return self.tr('Remove Dangles')

    def group(self):
        return self.tr('Mapping')

    def groupId(self):
        return 'mapping'



    def shortHelpString(self):
        return self.tr("""Clean input contacts layer to remove overshooted lines""")


    def initAlgorithm(self, config=None):

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.IN_LINES,
                self.tr('Input Contacts'),
                [QgsProcessing.TypeVectorLine]
            )
        )


        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.IN_POLYGONS,
                self.tr('Input Polygons'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )



    def processAlgorithm(self, parameters, context, feedback):
        polygons_layer = self.parameterAsLayer(
            parameters,
            self.IN_POLYGONS,
            context
        )

        lines_layer = self.parameterAsLayer(
            parameters,
            self.IN_LINES,
            context
        )

        for f in lines_layer.getFeatures():
            print(f.geometry())

        # fieldname = self.parameterAsString(parameters, self.CAT_FIELD, context)
        # unassigned = self.parameterAsBool(parameters, self.STYLE_UNASSIGNED, context)
        # feedback.pushInfo(f"field used is {fieldname}")
        # 
        # from ..utils import resetCategoriesIfNeeded
        # resetCategoriesIfNeeded(polygons_layer, fieldname, unassigned=unassigned)
        return {}

