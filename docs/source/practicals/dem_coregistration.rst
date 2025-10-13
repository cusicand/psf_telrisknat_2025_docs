..
   Copyright (c) 2025 PSF TelRIskNat 2025 Optical team
   SPDX-License-Identifier: CC-BY-NC-SA-4.0
   author: Diego Cusicanqui (CNES | ISTerre | Univ. Grenoble Alpes)

   This file is part of the “PSF TelRIskNat 2025” workshop documentation.
   Licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0).
   You may share and adapt for non-commercial purposes, with attribution and ShareAlike.
   See: https://creativecommons.org/licenses/by-nc-sa/4.0/

Manual and automatic DEM co-registration
----------------------------------------------------

..
   .. figure:: /_static/Fig0_patience.jpg
      :width: 100%
      :align: center
      :alt: be patient

      Advice from PSF TelRiskNat optical team.


**Diego CUSICANQUI**\ :sup:`1` & **Ruben BASANTES**\ :sup:`2`

\ :sup:`1` Univ. Grenoble Alpes, CNES, CNRS, IRD, Institut des Sciences de la Terre (ISTerre), Grenoble, France.

\ :sup:`2` Universidad Yachay Tech, Escuela de Ciencias de la Tierra, Energía y Ambiente, San Miguel de Urcuquí, Ecuador

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

- Understand the principles of co-registration technique.
- Learn how to apply image co-registration techniques manually and automatically.

.. note::
   For this practice, you will use ASTER derived DEMs produced during the practice of :ref:`dem_generation_page` to study the region of Cordillera Blanca 

Introduction
~~~~~~~~~~~~~~~~~~~~~~~~

As mentioned previously in the practice :ref:`dem_generation_page`, quantification of mass changes is crucial to understand the fundamental processes that trigger mass-wasting events. Thus, a comparison of two or more 3D surfaces (e.g. Digital Elevation Models) could help to quantify these mass changes. However, DEM quality is highly dependent on several parameters, such as camera resolution, height flight, image quality, percentage of stereo coverage, etc., which play a major role in the quality of the DEMs and how they represent the 3D relief. Nowadays, there are several tools to generate DEMs, most of them in an automatic way. Because DEMs are the primary source for mass changes estimations, it is very important to assess the quality of DEMs, to avoid misinterpretations on the results.

During the automatic DEM generation, there are several sources of error that can affect the final DEM, for example translation and/or rational displacements on the spatial reference, as well as scale variations. In this practice, you will focus on the ``co-registration`` procedure used to adjust geometrically a pair of a DEMs. This method fits all DEMs regardless of the technique by which they were generated. For our example, we will use two DEMs automatically generated from ASTER optical images acquired on two different dates. After a brief description of the theoretical basis of the methodology, you will carry on in two hands-on co-registering exercises, the first based on an excel worksheet that will help you understand **how the co-registering works**, and the second will teach you **how you can automate the co-registration procedure** based on the application of Python libraries.

.. _section_coregistration:

About DEM co-registration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Based on the results of the practice :ref:`section_dems_dod`, you may notice that all east- and northeast (southwest)-facing slopes have strong positive (negative) differences in surface elevation :numref:`fig-dod-bias`. This indicates some kind of systematic bias between the two DEMs used to calculate the DEM difference. This type of bias is usually due to slight horizontal (EW or NS) and vertical shifts in one or both of the DEMs :numref:`fig-dod-bias`, which cause misleading elevation changes, especially on steep slopes where you can have strong elevation differences in a few meters. In short, this means that the DEMs are spatially inconsistent.

.. _fig-dod-bias:

.. figure:: /_static/dem_generation/Fig6_dod_2023-2003_example.jpg
   :width: 100%
   :align: center
   :alt: Difference of DEMs (DoD) generated from ASTER images using ASP between 2003 and 2023.
   
   Difference of DEMs (DoD) generated from ASTER images using ASP between 2003 and 2023. Visualized in QGIS.

To ensure a precise xyz alignment between the DEMs, an iterative method called co-registration proposed by :cite:p:`nuth2011` is commonly applied. This method is based on the elevation differences of the two misaligned DEMs, and it assumes that the surface elevation change is a function of the slope and the aspect of the terrain :numref:``.

.. _fig_nuth2011:

.. figure:: /_static/dem_coregistration/Fig1_nuth2011.jpg
   :align: center
   :width: 100%
   :alt: Systematic slope bias due to misregistration

   Systematic bias in elevation due to slight shifts in one or both DEMs (from :cite:`nuth2011`).

This 3D spatial correction takes the most accurate DEM as a geodetic reference, whereas the second DEM is compared with the reference and co-registered (i.e. shifted) according the follow relationship:

.. math::
   :label: eq-coreg-model

   \frac{dh}{\tan(\alpha)} = a\,\cos\!\bigl(b - \omega\bigr) + c

where ``a`` is the magnitude of the misalignment, ``b`` is the direction of the misalignment, and ``c`` is the mean elevation bias. Then, the  adjustment factors are computed as follow:

.. math::
   :label: eq-coreg-components

   \begin{aligned}
   \Delta x &= a\,\sin(b),\\
   \Delta y &= a\,\cos(b),\\
   \Delta z &= \frac{c}{\tan(\bar{\alpha})}.
   \end{aligned}

where ``Δx``, ``Δy``, and ``Δz`` are the horizontal (East-West and North-South) and vertical shifts, respectively, and ``\bar{\alpha}`` is the mean slope of the terrain. The process is repeated iteratively until the adjustment factors converge to zero (i.e., no further improvement in the alignment). The method assumes that the horizontal shifts are small compared to the pixel size of the DEMs, and that there are no significant elevation changes between the two acquisition dates.

.. important:: 
   For a detailed explanation of the method:

   Nuth, C. and Kääb, A. (2011): Co-registration and bias corrections of satellite elevation data sets for quantifying glacier thickness change, The Cryosphere, 5, 271-290, https://doi.org/10.5194/tc-5-271-2011.

Practice
~~~~~~~~~~~~

Manual co-registration
^^^^^^^^^^^^^^^^^^^^^^^^^

Data inspection
''''''''''''''''''

For the first part of the exercise, you will use **QGIS and Excel** as the main softwares. This practice should be done in a computer with **Windows OS**.

.. important::
   Download the data provided for this practice here `Download data exercise 4 <https://filesender.renater.fr/download.php?token=ea958f24-271a-447d-993a-25e668f9df63&files_ids=60632668>`_.

First of all, you will open the ``DoD 2023-2003.tif`` :numref:`fig-dod-bias` into QGIS and you will explore the data by looking at the histogram values of the DoD values :numref:`fig_dod-histogram`. To do this, open the ``Layer Styling toolbar`` and click on ``compute histogram``. By analyzing the histogram, you will first note that the values of the DoD raster are concentrated around 0. However, when you zoom on the pic of the histogram, you can see that there is a slight shift of around **~10 m**.

.. _fig_dod-histogram:

.. figure:: /_static/dem_coregistration/Fig2_dod_histogram.jpg
   :align: center
   :width: 100%
   :alt: Histogram of the DoD values.

   Histogram of the DoD values ``DoD_2023-2003.tif`` file.

Aspect and slope calculation
''''''''''''''''''''''''''''''

In order to be able to use the co-registration procedure, you need first to compute ``slope`` and ``aspect``. To do so in QGIS, please go to the toolbar section and within GDAL tools, you will find ``Aspect`` and ``Slope`` functions respectively. Since you are using the 2023 DEM as reference, for that procedure you will use the DEM corresponding to the 2003. The results should look very similar to :numref:`fig_slope_aspect`.

.. _fig_slope_aspect:

.. figure:: /_static/dem_coregistration/Fig3_slope_aspect.jpg
   :align: center
   :width: 100%
   :alt: Slope and aspect maps.

   Slope (left) and aspect (right) maps calculated from the 2003 DEM.

Random sampling of points
'''''''''''''''''''''''''''''

Once those results are generated, you will have to generate ``point samples`` from where coregistration will be calculated. To do so, you have to go to ``Vector -> Research Tools -> Random points in Extent``. By using this tool :numref:`fig_random-points_generation`, you will randomly generate 10 000 points shapefile based on the same extent of the Difference of DEM's. The results of this procedure should look like in :numref:`fig_generated_points`.

.. _fig_random-points_generation:

.. figure:: /_static/dem_coregistration/Fig4_random_points_generation.jpg
   :align: center
   :width: 100%
   :alt: Random points generation.

   Random points generation using QGIS.

.. _fig_generated_points:

.. figure:: /_static/dem_coregistration/Fig5_generated_points.jpg
   :align: center
   :width: 100%
   :alt: Generated random points.

   Generated random points over the DoD raster.

Sampling the values of the rasters
'''''''''''''''''''''''''''''''''''''

Once the points are generated, you will have to extract the values of the ``DoD 2023-2003``, ``slope`` and ``aspect`` rasters to the points. To do so, you will use the ``Point Sampling Tools plugin`` in QGIS.  If you don't have this plugin installed, please refer to the section ``Plugin -> Manage and Install Plugins, and type Point Sampling Tool``. This plugin takes one point vector shapefile and several raster files to extract the value of the overlaid pixel, from the selected rasters. More information on the `official webpage <https://plugins.qgis.org/plugins/pointsamplingtool/>`_. You have to select the ``Random_points.shp`` file as well the raster files :numref:`fig_point-sampling-tool`. Once the layers are selected, you can rename the columns to keep the column names clear and short :numref:`fig_point-sampling-tool`. As a result, you will obtain a new shapefile that you will rename as ``Random_points_sample.shp`` but this time, you will find in the attribute table the columns you modified previously containing the pixel values from raster files :numref:`fig_point-sampling-tool`.

.. _fig_point-sampling-tool:

.. figure:: /_static/dem_coregistration/Fig6_point_sampling_tool.jpg
   :align: center
   :width: 100%
   :alt: Point Sampling Tool plugin.

   Parameters on point sampling tool in QGIS.

Filtering point data with null values
'''''''''''''''''''''''''''''''''''''''''

As you may notice in the :numref:`fig_generated_points` and :numref:`fig_point-sampling-tool`, there are several points which are located in empty areas, close to the image borders, for instance. These ``empty points`` or points containing ``missing (null)`` values, must be filtered/removed since they are not useful for the coregistration stage. To do so, you will open the attribute table of the ``Random_points_sample.shp`` and open the ``Select features using an expression tool``. This option allows us to select the features by filling certain conditions (e.g., between a range of values, if values exist or not, etc). For this case, you will search those values with missing or null values inside the three columns (i.e., aspect, slope, dod_23-03). Inside ``Select features`` windows, you can have access to the columns by clicking in the Fields and Values option as well as the ``Operators`` that will be used to meet the searched conditions :numref:`fig_filtering_points`. Inside the box expression type the expression written in :numref:`fig_filtering_points`.

.. code:: sql

   "aspect" is NULL OR "slope" is NULL OR "dod_23-03" is NULL

.. note::
   * ``aspect``, ``slope`` and ``dod_23-03`` = the fields or columns to be evaluated.
   * ``is`` = in the operator/evaluator which compares each row of the columns selected previously.
   * ``NULL`` = is the value of the expression to be fulfilled.
   * ``OR`` = is the logical operator to allow us to select several columns and check if the condition is filled in one column in any column.

.. question:: Questions for discussion
   :collapsible: closed

   Why do we use the ``OR`` operator instead of ``AND``?

By clicking on ``Select features``, QGIS will select all features who meet the conditions for the three columns. The selection returns ~ 3830 points features. Since the point features were generated randomly, the selected points may differ for you. Finally, once you have selected the points, the final step is to delete them. To do so, you will Edit the points features and click on ``Delete selected``. By doing so, we have reduced the initial point sample from 10 000 to 6 100 points. The results must look like :numref:`fig_filtering_points`.

.. _fig_filtering_points:

.. figure:: /_static/dem_coregistration/Fig7_filtering_points.jpg
   :align: center
   :width: 100%
   :alt: Filtering points with null values.

   Filtering points with null values using the expression tool in QGIS.

Filtering point with glacier outlines
'''''''''''''''''''''''''''''''''''''''''

Since the co-registration stage is based on those areas which have not suffered strong geomorphological changes (hereafter called as stable areas), you need to remove those points which are located within those areas which have strongly changed (i.e., glaciers, landslides, etc). So, you need to mask or remove those points within glacier outlines. To do so, you will use Randolph Glacier Inventory (RGI) version 7.0, as the main data source of glacier outlines. Please refer to the `RGI documentation <https://www.glims.org/RGI/>`_ for more details about worldwide glacier inventory.

Once you have downloaded the shapefile of the glacier outlines, you will open it in QGIS and you will check that the coordinate reference system (CRS) is the same as your other layers. If not, you will have to reproject it to the same CRS (i.e. ``WGS84 UTM Zone 18S``). Then, you will use the ``Select by location`` tool in QGIS to select those points within the glacier outlines :numref:`fig_select_by_location`. In this case, you will select features from ``Random_points_sample.shp`` that intersect with features from ``rgi60_SouthAmerica.shp``. By clicking on ``Run``, QGIS will select all points within the glacier outlines. Finally, you will delete those selected points by editing the layer and clicking on ``Delete selected``. The final result should look like :numref:`fig_select_by_location`.

.. _fig_select_by_location:

.. figure:: /_static/dem_coregistration/Fig8_select_by_location.jpg
   :align: center
   :width: 100%
   :alt: Select points within glacier outlines.

   Select points within glacier outlines using the Select by location tool in QGIS.

Exporting the point data to Excel
''''''''''''''''''''''''''''''''''''

As a final step, you will export the attribute table of the remaining points. To do so, you will make right click on the layer ``Random_points_sample.shp`` and you will click on ``Save Features As…``. Within the save vector layer menu you will change the format as ``MS Office Open XML spreadsheet [XLSX]``, which is the format excel. Finally, select the desired directory and click on OK; This procedure will export the entire attribute table in format excel.

.. _fig_export_to_excel:

.. figure:: /_static/dem_coregistration/Fig9_export_to_excel.jpg
   :align: center
   :width: 100%
   :alt: Exporting point data to Excel.

   Exporting point data to Excel from QGIS.

Co-registration in Excel
'''''''''''''''''''''''''''

a. Make sure that Excel has ``Solver`` installed. For general instructions on how load the Solver `Add-in in Excel <http://office.microsoft.com/en-us/excel-help/introduction-to-optimization-with-the-excel-solver-tool-HA001124595.aspx>`_.

b. Then open the ``DEM Co-Registration Excel Tool`` provided by Nuth and Kaab (2011). Can be downloaded here:

c. Thirdly, open the random point sample excel file. **Remember, for each record an elevation difference, and its corresponding slope and aspect values are mandatory**. Copy the corresponding values and paste them in the columns A, B and C ``INSERT RANDOM SAMPLE HERE``. It might be necessary to adjust the formulas in columns D, E, F and RMSE in cell C6 to account for the size of the sample you have pasted.

.. _fig_excel_tool:

.. figure:: /_static/dem_coregistration/Fig10_excel_tool.jpg
   :align: center
   :width: 100%
   :alt: DEM co-registration Excel tool.

   DEM Co-Registration Excel Tool. The blue box shows the columns where the data input should be inserted.

d. Fourthly, use Solver to determine the co-registration parameters ``a`` in cell ``C3``, ``b`` in cell ``C4``, and ``c`` in cell ``C5``. To do so, set the parameters equal to 1 (initial value).

.. _fig_solver_parameters:

.. figure:: /_static/dem_coregistration/Fig11_solver_parameters.jpg
   :align: center
   :width: 100%
   :alt: Solver parameters.

   Solver parameters to be set in the DEM Co-Registration Excel Tool.

   Then, open solver configure the parameters as follows :numref:`fig_solver_configuration`, Set ``Target Cell = C6``, ``Equal to = Min``, By Changing Cells ``C3:C5`` and finally click on ``Solve``.

.. _fig_solver_configuration:

.. figure:: /_static/dem_coregistration/Fig12_solver_configuration.jpg
   :align: center
   :width: 100%
   :alt: Solver configuration.

   Solver configuration to be set in the DEM Co-Registration Excel Tool.

The minimized solution is located in ``C3``, ``C4``, and ``C5``. And the displacement values for geometrically adjustment are in ``K4``, ``K5`` and ``K6``.

.. _fig_solver_results:

.. figure:: /_static/dem_coregistration/Fig13_solver_results.jpg
   :align: center
   :width: 100%
   :alt: Solver results.

   Solver results in the DEM Co-Registration Excel Tool.

Finally, displacement ``x``, ``y``, ``z`` vector of correction is applied to the corner coordinates of the un-registered DEM. To this end you can use any QGIS through the translate tool. As we mention before, this is an iterative process, so repeat all the procedure until the red line fits through the points (:numref:`fig_iteration_process`). A good proxy to choose to stop the iteration is when the ``RMSE`` is improved up to 2% or if the magnitude of the displacement vector is less than 0.5 m.

.. _fig_iteration_process:

.. figure:: /_static/dem_coregistration/Fig14_iteration_process.jpg
   :align: center
   :width: 100%
   :alt: Iteration process.

   Comparison of the elevation difference by the tangent of the slope, before and after coregistration, and the fitted cosine curve (red line). Example of the resulting histograms of the residuals after adjustment for bias.

.. tip:: 
   - Dem co-registration must be applied over stable rocky areas, so unstable areas should be removed.
   - The solution is most well defined for sample points on steeper slopes. Since ``dh/tan(slope)`` cannot be defined flatted areas, zero slopes must be eliminated.
   - A conic structure such as volcanos are perfect because it covers all terrain aspects as long as there is a sufficient amount of elevation difference samples.
   - Usually, less than 10000 samples are sufficient, although for the DEM Co-Registration excel tool it is possible to have up to 65000.
   - Using this tool, convergence is commonly obtained with less than ten iterations, depending the samples (number and distribution) and the fitting algorithm.

Automatic co-registration
^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this second part of the exercise, you will learn how to apply the co-registration procedure in an automatic way using Python libraries. The main advantage of using this method is that it is not necessary to extract random points, filter them, export them to excel, etc. Everything is done in a single script.

.. important::
   Download the data provided for this practice by running the following commands in your terminal:

   Go to the ``/psf_telrisknat_2025_docs/data/`` folder and run:

   .. code-block:: bash
      
      bash ./download_excercise_4_data.sh

Activation of the conda environment
'''''''''''''''''''''''''''''''''''''

First of all, you will activate the conda environment that you created in the practice :ref:`dem_generation_page`. To do so, open a terminal and type:

.. code-block:: bash

   conda activate psf_env

Get familiar with ``Geoutils`` library
''''''''''''''''''''''''''''''''''''''''

Before starting with the co-registration procedure, you will get familiar with the ``Geoutils`` library. To do so, you will open a jupyter notebook by typing in the terminal:

.. code-block:: bash

   jupyter notebook

.. note::
   If you have some problems to open the jupyter notebook or is not installed, just run in your terminal:

   .. code-block:: bash

      mamba install -c conda-forge jupyter

This command will open a new tab in your web browser. Open the scrip called ``geoutils_introduction.ipynb`` provided in the data folder. This script will help you to understand how to use the main functions of the ``Geoutils`` library. Please, follow all the steps of the script.

Co-registration procedure using ``xDEM``
''''''''''''''''''''''''''''''''''''''''''

Now, you will learn how to apply the co-registration procedure using the ``xDEM`` library. For this practice, you will use the same DEMs generated in the practice :ref:`dem_generation_page`. The entire procedure is explained in the jupyter notebook called ``dem_coregistration.ipynb`` provided in the data folder.

Importing libraries and loading data
''''''''''''''''''''''''''''''''''''''''''

First, you should import the necessary libraries.

.. code-block:: python

   import matplotlib.pyplot as plt
   import numpy as np

   import geoutils as gu
   import xdem

   # To avoid interpolation in plt.imshow
   plt.rcParams['image.interpolation'] = 'none'

Then, you will load the DEMs at once, croppping them to the same and reprojecting them to the same CRS.

.. code-block:: python

   fn_dem_2003 = "DEM_20030713.tif"
   fn_dem_2023 = "DEM_20230704.tif"
   fn_ref_dem = "COPDEM_30m.tif"
   dem_2003, dem_2023, ref_dem = gu.raster.load_multiple_rasters([fn_dem_2003, fn_dem_2023, fn_ref_dem], crop=True, ref_grid=1)
   ref_dem.set_nodata(-9999)

You can use the following code to visualize the DEMs.

.. code-block:: python

   fig, axs = plt.subplots(1, 3, figsize=(12, 6))
   dem_2003.plot(ax=axs[0], cmap='terrain', title="DEM 2003")
   dem_2023.plot(ax=axs[1], cmap='terrain', title="DEM 2023")
   ref_dem.plot(ax=axs[2], cmap='terrain', title="Reference DEM")
   plt.show()

.. figure:: /_static/dem_coregistration/Fig15_plots_rasters.png
   :width: 80%
   :align: center
   
   Comparison of the three DEMs showing elevation data.

Then, you will also load and plot the glacier outlines.

.. code-block:: python

   rgi_shpfile = "Glaciares_Peru.shp"
   rgi_outlines = gu.Vector(rgi_shpfile)

You may note that the ``Glaciares_Peru.shp`` layer contains nation-wide glacier inventory. However, glacier inventory uses different projection systems (e.g. WGS84). To solve this, you have to reproject the shapefile. In addition, we are working in the Cordillera Blanca region. So, you have to crop the shapefile to be compatible with the raster extent.

.. code-block:: python

   rgi_outlines.reproject(ref=dem_2023, inplace=True)
   rgi_outlines_crop = rgi_outlines.crop(dem_2023)
   rgi_outlines_crop.plot(color='blue', linewidth=1)

.. figure:: /_static/dem_coregistration/Fig16_glacier_outlines.png
   :width: 80%
   :align: center

   Glacier outlines of the Cordillera Blanca region.

Computting the difference of DEMs (DoD)
''''''''''''''''''''''''''''''''''''''''''

Now, you will calculate the difference of DEMs (DoD) between the two DEMs and plot it.

.. code-block:: python

   dh2023 = dem_2023 - ref_dem

.. code-block:: python

   vmax=30
   plt.figure(figsize=(6, 6))
   ax = plt.subplot(111)
   rgi_outlines.plot(ax=ax, facecolor='none', edgecolor='k', lw=0.5, zorder=2)
   dh.plot(ax=ax, cmap='RdYlBu', vmin=-vmax, vmax=vmax, cbar_title='Elevation change 2012 - 2018 (m)', zorder=1)
   ax.set_title('Cordillera Blanca and surroundings')
   plt.tight_layout()
   plt.show()

.. figure:: /_static/dem_coregistration/Fig17_dod_2023_cop30.png
   :width: 80%
   :align: center

   Difference of DEMs (DoD) between 2023 and 2003.

Generating stable areas mask
''''''''''''''''''''''''''''''''''''''''''

Now, you have to select stable areas to compute the co-registration parameters. The selection os stable areas is done by masking everything that is not stable, i.e., glaciers and steep slopes. Regarding glacier mask, you can use the glacier outlines loaded previously to mask all glaciers.

.. code-block:: python

   gl_mask = rgi_outlines_crop.create_mask(dh)

Regarding slopes, you will use the reference DEM (``COPDEM_30m.tif``) to compute the slopes as it does not contain large voids. In this case, you will mask all slopes larger than 40 degrees.

.. code-block:: python

   slope = xdem.terrain.slope(ref_dem)
   slope_mask = (slope.data < 40).filled(False)
   outlier_mask = (np.abs(dh.data) < 50).filled(False)

Finally, you will combine all masks to get the stable areas.

.. code-block:: python

   inlier_mask = ~gl_mask.data.filled(False) & slope_mask & outlier_mask
   plt.figure(figsize=(8, 8))
   plt.imshow(inlier_mask.squeeze()) # squeeze to remove the singleton dimension??
   plt.show()

.. figure:: /_static/dem_coregistration/Fig18_stable_areas.png
   :width: 80%
   :align: center

   Stable areas (True values) used for the co-registration procedure.

Applying the co-registration
''''''''''''''''''''''''''''''''''''''''''

Now, you are ready to apply the co-registration procedure. For this excercise, you will use Nuth and Kaab (2011):cite:`nuth2011` method implemented in the ``xDEM`` library. First, we need to define the coregistration function. Then we estimate the coregistration needed between our two ASTER DEMs. Finally, we apply that coregistration to the 2003 DEM.

.. code-block:: python

   coreg = xdem.coreg.NuthKaab() + xdem.coreg.VerticalShift(vshift_reduc_func=np.median)
   coreg.fit(dem_2023, dem_2003, inlier_mask, verbose=True)
   dem_2003_coreg = coreg.apply(dem_2003)

You can visualize the results of the co-registration procedure by inspecting metadata of the coreg object.

.. code-block:: python

   print(coreg.pipeline[0]._meta)

.. question:: Questions for discussion
   :collapsible: closed

   - What are the estimated shifts in x, y and z?
   - How many iterations were needed to converge?

Now, you can compute the DoD between the co-registered 2003 DEM and the 2023 DEM and plot it.

.. code-block:: python

   dh_coreg = dem_2023 - dem_2003_coreg

.. code-block:: python

   vmax = 50
   fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6))
   rgi_outlines_crop.plot(ax=ax1, facecolor='none', edgecolor='k', zorder=3)
   dh.plot(ax=ax1, cmap='RdYlBu', vmin=-vmax, vmax=vmax, cbar_title='Elevation change 2012 - 2018 (m)', zorder=1)
   ax1.set_title('Before coregistration')

   rgi_outlines_crop.plot(ax=ax2, facecolor='none', edgecolor='k', zorder=3)
   dh_coreg.plot(ax=ax2, cmap='RdYlBu', vmin=-vmax, vmax=vmax, cbar_title='Elevation change 2012 - 2018 (m)', zorder=1)
   ax2.set_title('After coregistration')

   ax3.set_title('Elevation change distribution')
   ax3.hist(dh.data.compressed(), bins=100, alpha=0.5, label='Before', range=(-vmax, vmax), color='blue')
   ax3.hist(dh_coreg.data.compressed(), bins=100, alpha=0.5, label='After', range=(-vmax, vmax), color='green')
   ax3.set_xlabel('Elevation change (m)')
   ax3.set_ylabel('Frequency')
   ax3.legend()

   plt.tight_layout()
   plt.show()

.. figure:: /_static/dem_coregistration/Fig19_dod_comparison.png
   :width: 100%
   :align: center

   Comparison of the DoD before (left) and after (middle) co-registration, and the histograms of the DoD values (right).

.. question:: Questions for discussion
   :collapsible: closed

   - How has the DoD changed after co-registration?
   - How has the distribution of DoD values changed after co-registration?

Computting statistics on stable areas
''''''''''''''''''''''''''''''''''''''''''

You can also compute some statistics on the stable areas before and after co-registration.

.. code-block:: python

   inlier_orig = dh[inlier_mask]
   nstable_orig, mean_orig = len(inlier_orig), np.mean(inlier_orig)
   med_orig, nmad_orig = np.median(inlier_orig), xdem.spatialstats.nmad(inlier_orig)
   print(f"Number of stable pixels: {nstable_orig}")
   print(f"Before coregistration:\
         \n\tMean dh: {mean_orig:.2f}\
         \n\tMedian dh: {med_orig:.2f}\
         \n\tNMAD dh: {nmad_orig:.2f}")

   inlier_coreg = dh_coreg[inlier_mask]
   nstable_coreg, mean_coreg = len(inlier_coreg), np.mean(inlier_coreg)
   med_coreg, nmad_coreg = np.median(inlier_coreg), xdem.spatialstats.nmad(inlier_coreg)
   print(f"After coregistration:\
         \n\tMean dh: {mean_coreg:.2f}\
         \n\tMedian dh: {med_coreg:.2f}\
         \n\tNMAD dh: {nmad_coreg:.2f}")

Saving the results
''''''''''''''''''''''''''''''''''''''''''

Finally, you can save the co-registered DEM.

.. code-block:: python

   dem_2003_coreg.save("DEM_20230704_coreg.tif")
   dh_coreg.save("DoD_20230704_20030713_coreg.tif")

References
~~~~~~~~~~~~~~~~~~

.. bibliography::
   :cited:
   :style: unsrt
