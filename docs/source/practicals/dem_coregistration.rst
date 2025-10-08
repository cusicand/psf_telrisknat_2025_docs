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

.. figure:: /_static/Fig0_patience.jpg
   :width: 100%
   :align: center
   :alt: be patient

   Advice from PSF TelRiskNat optical team.

..
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

   1. Introduction
   ^^^^^^^^^^^^^^^^

   As mentioned previously in the practice :ref:`dem_generation_page`, quantification of mass changes is crucial to understand the fundamental processes that trigger mass-wasting events. Thus, a comparison of two or more 3D surfaces (e.g. Digital Elevation Models) could help to quantify these mass changes. However, DEM quality is highly dependent on several parameters, such as camera resolution, height flight, image quality, percentage of stereo coverage, etc., which play a major role in the quality of the DEMs and how they represent the 3D relief. Nowadays, there are several tools to generate DEMs, most of them in an automatic way. Because DEMs are the primary source for mass changes estimations, it is very important to assess the quality of DEMs, to avoid misinterpretations on the results.

   During the automatic DEM generation, there are several sources of error that can affect the final DEM, for example translation and/or rational displacements on the spatial reference, as well as scale variations. In this practice, you will focus on the ``co-registration`` procedure used to adjust geometrically a pair of a DEMs. This method fits all DEMs regardless of the technique by which they were generated. For our example, we will use two DEMs automatically generated from ASTER optical images acquired on two different dates. After a brief description of the theoretical basis of the methodology, you will carry on in two hands-on co-registering exercises, the first based on an excel worksheet that will help you understand **how the co-registering works**, and the second will teach you **how you can automate the co-registration procedure** based on the application of Python libraries.

   2. About DEM co-registration
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

   3. Practice
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   3.1. Manual co-registration
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   3.1.1. Data inspection
   ''''''''''''''''''''''''

   For the first part of the exercise, you will use QGIS and Excel as the main softwares.First of all, you will open the ``DoD 2023-2003.tif`` :numref:`fig-dod-bias` into QGIS and you will explore the data by looking at the histogram values of the DoD values :numref:`fig_dod-histogram`. To do this, open the Layer Styling toolbar and click on compute histogram. By analyzing the histogram, you will first note that the values of the DoD raster are concentrated around 0. However, when you zoom on the pic of the histogram, you can see that there is a slight shift of around **~10 m**.

   .. _fig_dod-histogram:

   .. figure:: /_static/dem_coregistration/Fig2_dod_histogram.jpg
      :align: center
      :width: 100%
      :alt: Histogram of the DoD values.

      Histogram of the DoD values ``Diff_2023-2003.tif`` file.

   3.1.2. Aspect and slope calculation
   '''''''''''''''''''''''''''''''''''''''

   In order to be able to use the co-registration procedure, you need first to compute ``slope`` and ``aspect``. To do so in QGIS, please go to the toolbar section and within GDAL tools, you will find ``Aspect`` and ``Slope`` functions respectively. Since you are using the 2023 DEM as reference, for that procedure you will use the DEM corresponding to the 2003. The results should look very similar to :numref:`fig_slope_aspect`.

   .. _fig_slope_aspect:

   .. figure:: /_static/dem_coregistration/Fig3_slope_aspect.jpg
      :align: center
      :width: 100%
      :alt: Slope and aspect maps.

      Slope (left) and aspect (right) maps calculated from the 2003 DEM.

   3.1.3. Random sampling of points
   '''''''''''''''''''''''''''''''''''

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

   3.1.4. Sampling the values of the rasters
   '''''''''''''''''''''''''''''''''''''''''''''

   Once the points are generated, you will have to extract the values of the ``DoD 2023-2003``, ``slope`` and ``aspect`` rasters to the points. To do so, you will use the ``Point Sampling Tools plugin`` in QGIS.  If you don't have this plugin installed, please refer to the section ``Plugin -> Manage and Install Plugins, and type Point Sampling Tool``. This plugin takes one point vector shapefile and several raster files to extract the value of the overlaid pixel, from the selected rasters. More information on the `official webpage <https://plugins.qgis.org/plugins/pointsamplingtool/>`_. You have to select the ``Random_points.shp`` file as well the raster files :numref:`fig_point-sampling-tool`. Once the layers are selected, you can rename the columns to keep the column names clear and short :numref:`fig_point-sampling-tool`. As a result, you will obtain a new shapefile that you will rename as ``Random_points_sample.shp`` but this time, you will find in the attribute table the columns you modified previously containing the pixel values from raster files :numref:`fig_point-sampling-tool`.

   .. _fig_point-sampling-tool:

   .. figure:: /_static/dem_coregistration/Fig6_point_sampling_tool.jpg
      :align: center
      :width: 100%
      :alt: Point Sampling Tool plugin.

      Parameters on point sampling tool in QGIS.

   3.1.5. Filtering point data with null values
   ''''''''''''''''''''''''''''''''''''''''''''''''

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

   3.1.6. Filtering point with glacier outlines
   ''''''''''''''''''''''''''''''''''''''''''''''''''''

   Since the co-registration stage is based on those areas which have not suffered strong geomorphological changes (hereafter called as stable areas), you need to remove those points which are located within those areas which have strongly changed (i.e., glaciers, landslides, etc). So, you need to mask or remove those points within glacier outlines. To do so, you will use Randolph Glacier Inventory (RGI) version 7.0, as the main data source of glacier outlines. Please refer to the `RGI documentation <https://www.glims.org/RGI/>`_ for more details about worldwide glacier inventory.

   Once you have downloaded the shapefile of the glacier outlines, you will open it in QGIS and you will check that the coordinate reference system (CRS) is the same as your other layers. If not, you will have to reproject it to the same CRS (i.e. ``WGS84 UTM Zone 18S``). Then, you will use the ``Select by location`` tool in QGIS to select those points within the glacier outlines :numref:`fig_select_by_location`. In this case, you will select features from ``Random_points_sample.shp`` that intersect with features from ``rgi60_SouthAmerica.shp``. By clicking on ``Run``, QGIS will select all points within the glacier outlines. Finally, you will delete those selected points by editing the layer and clicking on ``Delete selected``. The final result should look like :numref:`fig_select_by_location`.

   .. _fig_select_by_location:

   .. figure:: /_static/dem_coregistration/Fig8_select_by_location.jpg
      :align: center
      :width: 100%
      :alt: Select points within glacier outlines.

      Select points within glacier outlines using the Select by location tool in QGIS.

   3.1.7. Exporting the point data to Excel
   ''''''''''''''''''''''''''''''''''''''''''''

   As a final step, you will export the attribute table of the remaining points. To do so, you will make right click on the layer ``Random_points_sample.shp`` and you will click on ``Save Features As…``. Within the save vector layer menu you will change the format as ``MS Office Open XML spreadsheet [XLSX]``, which is the format excel. Finally, select the desired directory and click on OK; This procedure will export the entire attribute table in format excel.

   .. _fig_export_to_excel:

   .. figure:: /_static/dem_coregistration/Fig9_export_to_excel.jpg
      :align: center
      :width: 100%
      :alt: Exporting point data to Excel.

      Exporting point data to Excel from QGIS.

   3.1.8. Co-registration in Excel
   ''''''''''''''''''''''''''''''''''

   4. Make sure that Excel has ``Solver`` installed. For general instructions on how load the Solver `Add-in in Excel <http://office.microsoft.com/en-us/excel-help/introduction-to-optimization-with-the-excel-solver-tool-HA001124595.aspx>`_.

   5. Then open the ``DEM Co-Registration Excel Tool`` provided by Nuth and Kaab (2011). Can be downloaded here:

   6. Thirdly, open the random point sample excel file. **Remember, for each record an elevation difference, and its corresponding slope and aspect values are mandatory**. Copy the corresponding values and paste them in the columns A, B and C ``INSERT RANDOM SAMPLE HERE``. It might be necessary to adjust the formulas in columns D, E, F and RMSE in cell C6 to account for the size of the sample you have pasted.

   .. _fig_excel_tool:

   .. figure:: /_static/dem_coregistration/Fig10_excel_tool.jpg
      :align: center
      :width: 100%
      :alt: DEM co-registration Excel tool.

      DEM Co-Registration Excel Tool. The blue box shows the columns where the data input should be inserted.

   7. Fourthly, use Solver to determine the co-registration parameters ``a`` in cell ``C3``, ``b`` in cell ``C4``, and ``c`` in cell ``C5``. To do so, set the parameters equal to 1 (initial value).

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

   3.2. Automatic co-registration
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   In this second part of the exercise, you will learn how to apply the co-registration procedure in an automatic way using Python libraries. To do so, you will use the same data as in the previous section. The main advantage of using this method is that it is not necessary to extract random points, filter them, export them to excel, etc. Everything is done in a single script.

   3.2.1. Activation of the conda environment
   ''''''''''''''''''''''''''''''''''''''''''''''

   First of all, you will activate the conda environment that you created in the practice :ref:`dem_generation_page`. To do so, open a terminal and type:

   .. code-block:: bash

      conda activate psf_env

   3.2.2. Get familiar with ``Geoutils`` library
   ''''''''''''''''''''''''''''''''''''''''''''''''

   Before starting with the co-registration procedure, you will get familiar with the ``Geoutils`` library. To do so, you will open a jupyter notebook by typing in the terminal:

   .. code-block:: bash

      jupyter notebook

   This command will open a new tab in your web browser. Open the scrip called ``geoutils_introduction.ipynb`` provided in the data folder. This script will help you to understand how to use the main functions of the ``Geoutils`` library. Please, follow all the steps of the script.

   3.2.3. Co-registration procedure using ``xDEM``
   ''''''''''''''''''''''''''''''''''''''''''''''''

