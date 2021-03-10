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

    IN_LINES = "IN_CONTACTS"
    IN_POLYGONS = "IN_POLYGONS"
    CLIP_OUTLINE = "CLIP_OUTLINE"
    OUTPUT = "OUTPUT"

    def icon(self):
        return QIcon(':/plugins/qgismappy/mapstyle.png')

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

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.CLIP_OUTLINE, self.tr("Clip outline"),
                defaultValue=True
            ))

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Cleaned Contacts')
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


        clip_outline = self.parameterAsBool(parameters, self.CLIP_OUTLINE, context)

        if clip_outline:

            dpars = {'INPUT': polygons_layer, 'FIELD': [], 'OUTPUT': 'TEMPORARY_OUTPUT'}
            dissolved =  processing.run("native:dissolve", dpars, context=context, feedback=feedback, is_child_algorithm=True)["OUTPUT"]
            # print(dissolved)
            #
            # print(dissolved.featureCount())


            ipars = {'INPUT': lines_layer, 'OVERLAY': dissolved, 'INPUT_FIELDS': [], 'OVERLAY_FIELDS': [],
                    'OVERLAY_FIELDS_PREFIX': '', 'OUTPUT': 'TEMPORARY_OUTPUT'}

            cont = processing.run("native:intersection", ipars, context=context, feedback=feedback, is_child_algorithm=False)["OUTPUT"]
            # print(cont)
            # print(cont.featureCount())


        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            lines_layer.fields(),  # QgsFields() for an empty fields list or source_lines.fields()
            QgsWkbTypes.MultiLineString,
            lines_layer.sourceCrs()
        )


        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        print("going to add the features")


        for feature in cont.getFeatures():
            print("add feature")
            sink.addFeature(feature, QgsFeatureSink.FastInsert)




        return {"OUTPUT": dest_id}

