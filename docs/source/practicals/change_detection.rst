..
   Copyright (c) 2025 PSF TelRIskNat 2025 Optical team
   SPDX-License-Identifier: CC-BY-NC-SA-4.0
   author: Diego Cusicanqui (CNES | ISTerre | Univ. Grenoble Alpes)

   This file is part of the “PSF TelRIskNat 2025” workshop documentation.
   Licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0).
   You may share and adapt for non-commercial purposes, with attribution and ShareAlike.
   See: https://creativecommons.org/licenses/by-nc-sa/4.0/

Change detection using optical images
-----------------------------------------
..
   .. figure:: /_static/Fig0_patience.jpg
      :width: 100%
      :align: center
      :alt: be patient

      Content will be soon available. Advice from PSF TelRiskNat optical team.


**Floriane PROVOST**\ :sup:`1`, **Pascal LACROIX**\ :sup:`2` & **Diego CUSICANQUI**\ :sup:`2`

\ :sup:`1` Institut de Physique du Globe de Strasbourg, EOST/Université de Strasbourg, Strasbourg, France

\ :sup:`2` Univ. Grenoble Alpes, CNES, CNRS, IRD, Institut des Sciences de la Terre (ISTerre), Grenoble, France.

.. |copy| unicode:: U+000A9

.. admonition:: Copyright

   *Document version 0.2, Last update: 2025-09-18*
   
   |copy| *PSF TelRIskNat 2025 Optical team (D. Cusicanqui, R. Basantes & P. Lacroix)*.
   This document and its contents are licensed under the Creative Commons Attribution 4.0 International License (`CC BY-NC-SA 4.0 <https://creativecommons.org/licenses/by-nc-sa/4.0/>`_).

   .. image:: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
      :target: https://creativecommons.org/licenses/by-nc-sa/4.0/
      :alt: License: CC BY-NC-SA 4.0

----

Learning objectives:
~~~~~~~~~~~~~~~~~~~~~~~~

- Design a workflow to answer a question
- Learn how to create RGB composite and to compute indexes
- Learn how to create manually a vector file 
- Execute spatial/attribute operations to create a vector file
- Create a map that summarise your results


1. Introduction
~~~~~~~~~~~~~~~~~~~~~~~~

We are going to study the wild fires that impacted California in January 2025. The main goal of our study is to estimate **how many houses/building were destroyed by the 2025 wild fire?**

Regarding the California wild fire event, In 2024, the San Francisco Bay Area experienced several notable wildfires around the region rather than inside the city itself. The **Corral Fire** near Tracy in the Diablo Range burned about 14,168 acres (≈ 57.34 km²) from June 1–6, while Sonoma County's Point Fire scorched ~1,207 acres (≈ 4.88 km²) from June 16–24. More infor in `CallFire <https://www.fire.ca.gov/incidents/2024/6/1/corral-fire>`_.

Smoke from these and other regional fires periodically drifted into San Francisco, prompting Bay Area Air Quality Management District advisories—especially in mid-June and again in August—due to hazy skies and particle pollution concerns :cite:`casey2025`. Overall, impacts in San Francisco were felt mainly through smoke and reduced air quality, while the largest burn areas were in surrounding counties `SFGATE <https://www.sfgate.com/weather/article/bay-area-air-advisory-smoky-skies-21071765.php>`_. More information about large California wildfires in :cite:`keeley2021`

.. _figure_wildfire:

.. figure:: /_static/change_detection/Fig1_wildfires.jpg
   :width: 80%
   :align: center
   :alt: wildfire

   Wildfire in California, USA. Source: `NASA Earth Observatory <https://earthobservatory.nasa.gov/images/153831/the-palisades-fires-footprint>`_.

First of all, try to draft a workflow/diagram describing the logical steps and operations needed to answer the question. For that, answer to these questions:

- What data do you need?
- What information do you need?
- What operation do you need to execute to obtain the results?

Once answered construct the diagram.

2. Raster data
~~~~~~~~~~~~~~~~~~~~~~~~

We need to map the wild fire extent. To do that we are going to use Sentinel-2 images and manipulate the bands in order to easily detect and map the fires.

For this practice, we are going to use `QGIS <https://qgis.org/en/site/>`_ independent of the operating system. If you have not installed QGIS yet, please refer to the practical `Installation <installation.html>`_.

.. tip::
   Download the data using the following link `RENATER <https://filesender.renater.fr/?s=download&token=5d771970-0380-4a37-902c-afc47719b665>`_ (valid until 2025-12-31).


2.1. Sentinel-2 images
^^^^^^^^^^^^^^^^^^^^^^^^^

The Sentinel-2 images are available on the `Copernicus Open Access Hub <https://scihub.copernicus.eu/dhus/#/home>`_ or `AWS <https://registry.opendata.aws/sentinel-2/>`_. For this practical, we provide you two Sentinel-2 images acquired before and after the fire event. The data is located in the two separate folders in ``data/exercise_1_change_detection`` named by their acquisition date.

- ``S2_L1C_T11SLT_20250102T183751`` (before the fire event)
- ``S2_L1C_T11SLT_20250112T183731`` (after the fire event)

.. note:: 
   **Load all the bands on QGIS** and compare them. Do you see the wild fires?

2.2. Sentinel-2 RGB composite
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sentinel-2 images are multispectral images, meaning that they contain several bands acquired at different wavelengths. Visit: `Sentinel Hub <https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/composites/>`_ to determine what RGB is more suitable to map wildfires.

Now, create a RGB composite for both dates (before and after the fire event).
- Open the menu ``Raster > Miscellaneous > Create a Virtual Raster…``
- Define the bands composing the RGB composite.
- Click on ``Place each input file into a separate band``.
- Create the Virtual raster.

.. _figure_rgb:

.. figure:: /_static/change_detection/Fig2_rgb_composite.jpg
   :width: 100%
   :align: center
   :alt: rgb composite

   Sentinel-2 RGB composite.

2.3. Sentinel-2 band math
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As fires are burning the vegetation, another option is to compute the Normalised Different Vegetation index `(NDVI) <https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/ndvi/>`_. This index is a widely used metric for quantifying the health and density of vegetation. Compute the NDVI by opening the function ``Raster > Raster Calculator``. This window should appear as :numref:`figure_ndvi`.

.. _figure_ndvi:

.. figure:: /_static/change_detection/Fig3_ndvi.jpg
   :width: 100%
   :align: center
   :alt: ndvi

   Sentinel-2 NDVI.

- Define the mathematical operation you want to realize (here NDVI). Be careful, select bands of the same date.
- Choose to ``create the raster "on-the-fly"`` or to save it in your project (preferred). If you choose to create the raster on-the-fly, the raster will appear in the project but will not be saved. If you save the project, close it and open it later, the raster will be empty (because it was not saved).
- Repeat the operation for the two dates of acquisition.

.. important:: 
   It’s important that your data are well organised ! Both in your computer and in QGIS. For example, layers can be grouped together to organise the layer browser in QGIS.

.. _figure_ndvi_change:

.. figure:: /_static/change_detection/Fig4_ndvi_change.jpg
   :width: 100%
   :align: center
   :alt: ndvi change

   Sentinel-2 NDVI change.

3. Vector data
~~~~~~~~~~~~~~~~~~~~~~~~

3.1. Manually create a vector file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Vector files can be created manually with the function XXX 
The following window should appear like :numref:`figure_vector_manual`.

a. Choose the name of the file, the extension (shapefile), and set up carefully the geometry (point, line or polygon) and the CRS. Click ``OK`` once all the options have been chosen. The layer should appear in the section ``Layers`` of the GIS environment.
b. To edit the layer, click on the created vector file and on the function ``Toggle Editing`` (pencil icon).
c. Click then on the function ``Add Polygon Feature`` (yellow star icon) to create a new entity.
d. Click on the map to draw the limits of the polygon you want to map.
e. Save the entity by clicking on the function ``Save Layer Edits`` (floppy disk icon) to render the layer non editable.
f. If you want to modify the points/shape of your vector, use the function ``Vertex Tool`` (icon with a point and a line) and move/modify the points.

.. _figure_vector_manual:

.. figure:: /_static/change_detection/Fig5_vector_manual.jpg
   :width: 100%
   :align: center
   :alt: vector manual

   Create a vector file manually.

.. admonition:: Do it yourself

   **Map manually** the fire extent(at least the eastern fire located north of Pasadena).

3.2. Create a vector file from raster data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now, we are going to create a vector file from the NDVI change raster. The idea is to extract the area where the NDVI has decreased significantly (i.e. vegetation has been destroyed by the fire).

a. Determine what operation should be realized to extract the fire extent from the NDVI
raster files. Use the ``Raster Calculator`` to derive a raster with the fire extent.

b. Vectorize the resulting raster using the function ``Raster > Conversion > Raster to Polygon``. You should obtain a new vector layer that looks like :numref:`figure_raster_to_vector`. The spatial domain is correctly sampled into geographical entities but many geographical entities are not of interest for this study.

.. _figure_raster_to_vector:

.. figure:: /_static/change_detection/Fig6_raster_to_vector.jpg
   :width: 100%
   :align: center
   :alt: raster to vector

   Create a vector file from a raster.

.. question:: Questions for discussion
   :collapsible: closed

   - What entities should be filtered?
   - What attribute/properties do we need to compute to it?

c. Use the function ``Vector > Geometry > add geometrical attributes`` to compute the area and perimeter of each entity of the vector layer ``Vectorized``.

d. Use the attribute table to filter entities with areas smaller than 1,000 m², remove them by editing the table ``Toggle Editing`` (pencil icon) and deleting the selected entities (red garbage).

e. Repeat the operation to remove entities with areas larger than 68,000,000 m².

f. Regroup the entities in one single entity ``fire extent`` by using the function ``Vector > Geoprocessing Tools > Dissolve``. Your final result should look like :numref:`figure_fire_extent`.

.. _figure_fire_extent:

.. figure:: /_static/change_detection/Fig7_fire_extent.jpg
   :width: 100%
   :align: center
   :alt: fire extent

   Fire extent vector file.

g. Create a map showing the extent of the fires in California in January 2025.

4. Quantifying impacts 
~~~~~~~~~~~~~~~~~~~~~~~~

4.1. Count the number of buildings destroyed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To estimate the number of buildings destroyed by the fire, we are going to use a vector file containing the building footprints in California. The file is located in ``data/exercise_1_change_detection/buildings_CA.shp``.


a. Load the vector file ``buildings_CA.shp`` in QGIS.
b. Use the function ``Vector > Geoprocessing Tools > Intersection`` to extract the buildings that intersect the fire extent.
c. Open the attribute table of the resulting vector layer and count.

.. question:: Questions for discussion
   :collapsible: closed

   - How many building were impacted?
   - Estimate the total surface of damaged building by performing an operation on the ``Attribute table``.
   - Estimate the cost of the wildfire (price per square meter in California is ranging from 500$ to 700$).

4.2. Check our mapping
^^^^^^^^^^^^^^^^^^^^^^^

We are now going to use `Open Street Map (OSM) <https://www.openstreetmap.org/>`_ to check our mapping. OSM data is a geographic database feed by a community of mappers that contribute and maintain data about roads, trails. It is therefore possible to download the raw data directly and reuse it as you wish, for cartographic or other purposes. Every week, a complete file called ``planet`` is generated and made available by the OpenStreetMap Foundation. This file is very large and growing fast (20 GB at the end of 2011, 63 GB at the beginning of 2018) because it contains all the data for the entire planet. Extracts by continent, country or region are also available and updated daily by Geofabrik. There are also tools for breaking down a file into smaller geographical areas.

There are several ways of viewing and downloading OSM data:

4.2.1. Viewing the 'static' OSM map
'''''''''''''''''''''''''''''''''''''

The 'static' OSM map represents OSM data in raster form. It is not possible to manipulate the information contained in this layer. However, it allows OSM information to be viewed and can be used as a background map. To download the OSM map into QGIS you need to use the `QuickMapServices <https://plugins.qgis.org/plugins/quick_map_services/>`_ extension. 
Display OSM from WMS layers already installed on your computer. Use the function ``Web > QuickMapServices > OSM > OSM Standard``. Look at the areas affected by the fires. What do you notice?

4.2.2. Download the OSM database for an area of interest
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

You can download OSM data using `QuickOSM plugin <https://plugins.qgis.org/plugins/QuickOSM/>`_ to download the vector data from the OSM base maps.

- Click on the function ``Vector > QuickOSM > QuickOSM`` (green lupe icon).
- Click on ``Theme`` and select the default ``Urban`` theme. Define the geographical extent for which you want to download the data. You can use the ``Canvas extent`` option to download the data for the area currently displayed on your QGIS canvas.

.. important::
   This area must not be too large, as this could create a memory problem in QGIS.

- Click on ``Execute query`` to download the data. Several layers should appear in your ``Layers`` section.

You can also use the ``OSMDownloader`` plugin to download OSM data. This plugin allows you to download OSM data in a specific format (shapefile, geopackage, etc.) and for a specific area of interest.

* Install the plugin `OSMDownloader <https://plugins.qgis.org/plugins/OSMDownloader/>`_ from the QGIS plugin manager.

* Open the plugin from the menu ``OSMDownloader``.

* Define the area of interest by drawing a rectangle.

* Save the data in a specific format (shapefile, geopackage, etc.) and download.

A number of vector layers should appear in your ``Layers`` tab. Manipulate these layers to
display the buildings mapped in OSM and compare with your result.

.. admonition:: Do it yourself

   Draw a diagram that represents all the steps realised to answer the initial question.

5. References
~~~~~~~~~~~~~~~~~~

.. bibliography::
   :cited:
   :style: unsrt