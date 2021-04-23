# Mappy tutorial

Mappy is a QGIS plugin that simplify some useful operations needed to create geological maps by the point-and-contacts principle.

## Initial setup

Two different layers should be created:
- A line layer (either Line or MultiLine). The associated fields are not mandatory, but you might want to consider adding a couple of fields like ```certainty``` and/or ```type``` to represent the type of contact you are tracing. Keep in mind that more information you add to your vector data, more easy will be to style them later or to reuse them for other purposes.
- A point layer. Here we need at least one field that will be used as unique identifier for each geological unit that will be mapped. Choose for example ```geo_units```.

---
**Note**

Take your time to establish the naming of your fields to be meaningful and readily understandable. The same apply for the layers. It will not influence mappy in any way, but it will help you creating a clean dataset.

---

The type of fields can be freely chosen, but it is highly suggested you try to define beforehand the entries that will be used when populating your map. For example a ```string/char``` field can be used as type for the ```geo-units``` field, but it might be difficult to be consistent when entering those long strings by hand (they could be easily misspelled), thus short names or a code for each unit might be preferable. 

---
**Note**

To avoid mistakes when typing in the name of the geological unit in a string field, you could define them beforehand customizing the [attribute form](https://docs.qgis.org/testing/en/docs/user_manual/working_with_vector/vector_properties.html#attributes-form-properties) used to enter the field's values. An ```Unique Values``` or a ```Value Map``` [widget](https://docs.qgis.org/testing/en/docs/user_manual/working_with_vector/vector_properties.html#edit-widgets) might be used for this task.

---

The layers can be created in any format supported by QGIS (e.g. ESRI Shapefiles), but we suggest organizing your work within a geopackage file. This open format make it possible to store within a single and portable file any number of different vector layers. To create a new geopackage use ```Layer> Create Layer> New Geopackage Layer``` or ```CTRL+SHIFT+N```.

![geopackage](imgs/geopackage.png)
<figcaption> 

Creating a new geopackage layer in QGIS with one point layer named ```points```, with one field ```geo_units```of type ```Text Data```. Once the geopackage is created new layers can be appended to the same file by selecting the same ```Database``` 

</figcaption>  


## Drawing the contacts


