..
   Copyright (c) 2025 PSF TelRIskNat 2025 Optical team
   SPDX-License-Identifier: CC-BY-NC-SA-4.0
   author: Diego Cusicanqui (CNES | ISTerre | Univ. Grenoble Alpes)

   This file is part of the “PSF TelRIskNat 2025” workshop documentation.
   Licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0).
   You may share and adapt for non-commercial purposes, with attribution and ShareAlike.
   See: https://creativecommons.org/licenses/by-nc-sa/4.0/

.. _image_correlation:

Feature tracking image correlation
-------------------------------------
..
   .. figure:: /_static/Fig0_patience.jpg
      :width: 100%
      :align: center
      :alt: be patient

      Advice from PSF TelRiskNat optical team.


**Diego CUSICANQUI**\ :sup:`1` & **Pascal LACROIX**\ :sup:`1`

\ :sup:`1` Univ. Grenoble Alpes, CNES, CNRS, IRD, Institut des Sciences de la Terre (ISTerre), Grenoble, France.

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

- Understand the principles of image correlation for measuring surface displacements.
- Learn how to apply image correlation techniques using the ASP software.
- Analyze and interpret displacement fields obtained from image correlation.

.. note::
   This exercise focuses on optical remote sensing data from different sensors at different spatial resolution i.e. Planet (3m) or Sentinel2 (10m) or LandSat8 (15m). These remote sensing datasets have the greatest advantages of being **free and available worldwide**.
   For this practice, we will focus in the **Maca Landslide** in Peru using PlanetScope data.

INTRODUCTION
~~~~~~~~~~~~~~~~~~~~~~~~

Landslides are a major threat in most mountainous areas of the world, causing  nearly 10000 casualties every year. It has been observed that landslides can be preceded by a phase of acceleration, emphasising the interest in detecting slow ground-movements and monitoring their evolution through time. Knowing how the ground moves is essential to understanding the physical mechanisms controlling movement :cite:`lacroix2019`. Landslide displacement can be measured from space by two techniques: first, by Interferometric Synthetic Aperture Radar (InSAR) and then, by feature-tracking image correlation applied either to SAR or optical images :numref:`fig_surf_disp_optic_sar`.

On one hand, surface deformation obtained from InSAR is now being used to measure very small displacements (e.g., < 1 cm) and detect new unstable zones. Although this technique offers the possibility to map very large areas (up to 400 km for Sentinel-1), this kind of data has a complex data processing and encounters different limitations related with the unwrapping of the signal that makes it not fully adapted to small objects like landslides or fast objects like glaciers :cite:`garcia2024`. On the other hand, optical image correlation is an appropriate technique for monitoring large displacements or long-term displacements of small objects :cite:`cusicanqui2021_JGRES`. Although freely available data exist worldwide (Section 2), the main limitations for this data are the presence of snow at the surface, clouds and strong changes in contrast caused by shadows. These two techniques have become the main means of studying natural hazards that produce deformations of the earth's surface on different spatio-temporal scales :cite:`zhu2022`.

.. _fig_surf_disp_optic_sar:

.. figure:: /_static/image_correlation/Fig1_surf_disp_optic_sar.jpg
   :width: 100%
   :align: center
   :alt: Domain of applicability of different techniques and satellite data

   Domain of applicability of different techniques and satellite data as a function of the landslide size and velocity :cite:`lacroix2020` .

.. note::
   In this practice, we will focus only on optical remote sensing data, at different resolutions.

REMOTE SENSING DATA
~~~~~~~~~~~~~~~~~~~~~~~~

There are several possibilities to get freely available optical remote sensing data and many online services which offer access to the data worldwide. In this practice, we won't cover all possible sources, but rather the most popular ones (i.e. Landsat 5/7/8, Sentinel-2 and Planet). For a comprehensive introduction you can see the `Spatialpost <https://www.spatialpost.com/free-satellite-imagery/>` webpage.

Landsat 4/5/7/8 legacy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The landsat program has been mapping earth since the early ~1970's until now. Landsat satellites have continuously acquired space-based images of the Earth's land surface, providing uninterrupted data to help land managers and policymakers make informed decisions about our natural resources and the environment. From a general point of view, this enormous dataset covers earth surface worldwide with a relatively medium spatial resolution 30 m and 15 m for multispectral and panchromatic bands, respectively. Landsat legacy has also a very good radiometric resolution between 5 to 11 bands depending on the landsat mission, as well as a good temporal resolution, one image each 16 days at equator and 2-3 days in the north pole. Landsat tiles cover a large spatial extent, with a 185 kilometres wide footprint. more information on `USGS-landsat mission <https://www.usgs.gov/landsat-missions/landsat-satellite-missions>`_ webpage.

.. info::
   Accessing LandSat7/8 data (Since 1999, 15m resolution, 16 days revisit time) could be possible though the following links:
   
   - `USGS Earth Explorer <https://earthexplorer.usgs.gov/>`_.
   - `Landsat look <https://landsatlook.usgs.gov/viewer.html>`_.

Sentinel-2
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Copernicus SENTINEL-2 mission comprises a constellation of two polar-orbiting satellites placed in the same sun-synchronous orbit, phased at 180° to each other. It aims at monitoring variability in land surface conditions, and its wide swath width (290 km) and high revisit time (10 days at the equator with one satellite, and 5 days with 2 satellites under cloud-free conditions which results in 2-3 days at mid-latitudes) will support monitoring of Earth's surface changes. More technical information though `Copernicus Sentinel-2 <https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2>`_ program.

.. info::
   Accessing Sentinel-2 data (since December 2015, 10m resolution, 5 days revisit time) could be possible though the following links:
   
   - `Copernicus Open Access Hub <https://dataspace.copernicus.eu/data-collections/copernicus-sentinel-data/sentinel-2>`_.

PlanetScope
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PlanetScope, operated by Planet, is a constellation of approximately 130 satellites, able to image the entire land surface of the Earth every day (a daily collection capacity of 200 million km²/day, :numref:`fig_planetscope_revisit_time`). PlanetScope images are approximately 3 metres per pixel resolution with 4 spectral bands Blue, Green, Red and IR bands. The data can be downloaded for free, within a certain quota, on the `Planetscope <https://docs.planet.com/data/imagery/planetscope/>`_ website.

.. info::
   Accessing Planet data (Since ~2016, 3m resolution, ~1day revisit time):

   - `Planet Explorer <https://www.planet.com/explorer/>`_.

.. _fig_planetscope_revisit_time:

.. figure:: /_static/image_correlation/Fig2_planetscope_revisit_time.jpg
   :width: 100%
   :align: center
   :alt: PlanetScope constellation

   Average revisit time between 2 Planet acquisitions (2019-2020), :cite:`roy2021`.

PRACTICE
~~~~~~~~~~~~~

About the study site - Maca Landslide, Peru
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The `Maca landslide <https://goo.gl/maps/LnyEkErxexKkSHRW8>`_ :numref:`fig_maca_landslide` is situated in the Colca valley in Peru which is a wide depression filled with lacustrine sediments deposited over the last 1M yr, after a major debris avalanche coming from the “Hualca Hualca” volcanic complex dammed the valley. After the breaching of the dam, Colca river started to incise the soft clayey sediments and initiated landsliding in the whole area. Its historical activity can be traced back to the 1980's, when the Lari landslide pushed the river down to the Maca side, and started to erode the Maca side. Several large reactivation occurred in 1990's, 2000's, 2012-2013, and 2019-2020 :cite:`lacroix2019`, :cite:`zerathe2016`, :cite:`bontemps2018`. Examples for this practice will be taken during the last stage of reactivation, which produced major damages.

.. _fig_maca_landslide:

.. figure:: /_static/image_correlation/Fig3_maca_landslide.jpg
   :width: 100%
   :align: center
   :alt: Maca Landslide

   Picture of the Maca landslide.

For this practice, landslide motion will be retrieved from correlation of optical images. The specific goal is to be able to produce maps such as the one shown in :numref:`fig_landslide_displacement`.

.. _fig_landslide_displacement:

.. figure:: /_static/image_correlation/Fig4_maca_surf_disp_bontemps.jpg
   :width: 100%
   :align: center
   :alt: Maca Landslide Displacement

   Surface displacement field of the Maca landslide between 2003 and 2013 :cite:`bontemps2018`.

Download PlanetScope data
'''''''''''''''''''''''''''''

Log on the `Planet server <https://www.planet.com/explorer/>`_, select your area of interest (not too large, typically 4x3km, that includes the landslide and stable areas) and download at least 2 images (you can even select one per year 2017-2022), taken at the same season, without clouds. If possible select images that are not a mosaic of several images but only one single image. The image download is done with the “order scenes” blue button at the bottom left of the browser :numref:`fig_planet_download`.

.. _fig_planet_download:

.. figure:: /_static/image_correlation/Fig5_planet_download.jpg
   :width: 100%
   :align: center
   :alt: Planet download

   Planet download interface centered on Maca landslide.

.. note::
   Since the activation of the Planet account could take long-time, for this practice we already provide a set of images.

Now, open two images (those furthest back in time, 2018-2022). Open both images by clicking on ``Layer -> Add Raster Layer`` play with them by turning them on and off.

.. question:: Questions for discussion
   :collapsible: closed

   - Can you tell if the landslide faced any changes during your period of study?
   - Are you able to track any displacement by eye?

About surface displacements and image correlation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Surface displacements are defined as the movement of the ground surface between two dates. They can be measured in different ways, either in-situ (e.g., GNSS, total station, extensometer, etc.) or remotely (e.g., optical or SAR image correlation, InSAR, LiDAR, etc.). In this practice we will focus on surface displacements measured from optical image correlation.

Surface displacements from image correlation are obtained by tracking the translation of small, textured pixel windows between two accurately co-registered, orthorectified images acquired at different dates. A similarity metric—typically normalized cross-correlation—yields sub-pixel offsets for each window; these offsets are converted to map-plane displacement vectors using pixel size. The method delivers dense 2-D horizontal motion fields (magnitude and direction), with uncertainty controlled by image texture, window size, co-registration accuracy, and radiometric changes :cite:`ayoub2008`. The main principle of image correlation is to divide the first image into small windows (or chips) and then search for the best matching window in the second image. However, modern softwares have implemented different strategies and algorithms to improve the accuracy, robustness and speed of the correlation process.

.. important::
   For the following exercise we will use two different algorithms to compute surface displacements: (1) IMCORR (SAGA-QGIS) and (2) ASP.
   We propose to compare both algorithms and discuss their advantages and limitations.

Compute surface displacements with IMCORR (SAGA-QGIS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This first part of the exercise will be done using QGIS software with the SAGA plugin. This exercise can be done on any operating system (Windows, Linux or MacOS).

.. important::

   Download a pair of Planet images (2018-2021) over the Maca landslide using this `RENATER link <https://filesender.renater.fr/download.php?token=918a226e-0b42-4b88-93dc-f5025228d703&files_ids=60469767>`_.

Once images loaded in QGIS, we will use the SAGA plugin to compute surface displacements with the IMCORR algorithm. If you don't have SAGA installed, please follow the instructions in the :ref:`install_qgis` section of the installation guide.

.. note::
   IMCORR algorithm is on of the first image correlation algorithms developed in the early 90's :cite:`scambos1992`. It is now implemented in the SAGA GIS software and can be used through the QGIS interface. It has been widely used in glaciology to measure glacier surface displacements from optical images :cite:`scambos1992`.
   As this algorithm is no longer maintained, **we will use only for academic purposes**. It is therefore recommended to use more recent algorithms such as the one implemented in the ASP software (see :ref:`compute_surf_disp_asp`).

Prepare the images
'''''''''''''''''''''''''''

IMCORR algorithm accepts **single band images** with the **same number of columns** (``width``) **and lines** (``height``). So, you will need to first extract the red band (band 3) from both Planet images and then clip them to the same extent. As this is a common processing step, we wont detail it here.

.. tip::

   1. For extract single band, you can use ``GDAL -> Raster conversion -> Rearange bands`` within QGIS.
   2. For clipping images you can use the ``Clip Raster by Extent`` tool in QGIS to clip both images to the same extent. Make sure to check the option ``Use Layer Extent`` and select one of your two images as the layer to define the extent.
   3. You can check the number of columns and lines of your images by right-clicking on the layer and selecting ``Properties -> Information`` tab.

Image correlation and outputs
'''''''''''''''''''''''''''''''''''''

Now, in the ``Processing Toolbox`` of QGIS, search for ``IMCORR`` and open the ``Image Correlation (IMCORR)`` tool. Fill the parameters as :numref:`fig_imcorr_parameters` and run the tool.

.. _fig_imcorr_parameters:

.. figure:: /_static/image_correlation/Fig6_imcorr_parameters.png
   :width: 100%
   :align: center
   :alt: IMCORR parameters

   IMCORR parameters in QGIS. 1 and 3) Input images (single band, same size), 2) ``IMCORR`` algorithm, 4) Correlation parameters (Search chip size, Reference chip size, Grid spacing).

.. important::
   The choice of the parameters is crucial to obtain good results. Here are some advices:
   
   ``search chip size (pixels)``: Chip size of search chip, used to find correlating reference chips in the second image. A larger chip size will increase the chance of finding a match, but will also increase computation time. A typical value is 64x64 pixels.

   ``reference chip size (pixels)``: Chip size of reference chip to be found in search chip. used to find correlating search chips in the first image. A larger chip size will increase the chance of finding a match, but will also increase computation time. A typical value is 32x32 pixels. This parameter can be equal or less to the ``search chip size``.

   ``Grid spacing (Map units)``: Spacing between grid points where displacements are calculated. A smaller spacing will give a more detailed displacement field, but will also increase computation time. A typical value is 10 pixels.

The output of the IMCORR tool are two ``vector files``: ``Correlated points`` and ``Displacement vectors``. You can load them in QGIS and visualize them as :numref:`fig_imcorr_outputs`.

* The ``Correlated points`` layer contains all details about the correlation process (i.e. displacemets along columns (EW) and rows (NS), correlation coefficient, pixel coordinates, displacement in pixels, etc) for each grid point :numref:`fig_imcorr_outputs`.
* The ``Displacement vectors`` layer contains only the displacement vectors for each grid point oriented though the direction of the displacement. THe lenght of the vectors is proportional to the displacement amplitude :numref:`fig_imcorr_outputs`.

Within the correlated points, you can visualize the ``DISP`` column that contains the total displacement amplitude (in meters) for each grid point :numref:`fig_imcorr_outputs`. You can also visualize the ``STRENGTH`` column that contains how the correlation is between pixels (greater values means better correlation). In addition to these two important columns, you can also visualize the ``XERR`` and ``YERR`` columns that contain the uncertainty of the displacement along columns (EW) and rows (NS), respectively.

.. tip::
   You can filter the correlated points by the ``STRENGTH``, ``DISP``, ``XERR`` and ``YERR`` columns to keep only the best correlated points (e.g. STRENGTH > 6 or 2 pixels) or those points with low uncertainty (e.g. XERR < 1 or YERR < 1) :numref:`fig_imcorr_outputs`.

.. _fig_imcorr_outputs:

.. figure:: /_static/image_correlation/Fig7_imcorr_outputs.png
   :width: 100%
   :align: center
   :alt: IMCORR outputs

   IMCORR outputs in QGIS: 1) ``Correlated points`` and ``Displacement vectors`` layers. 2) and 3) Important outputs within the ``Correlated points`` layer, 4) ``Correlation points`` coloured by displacements (``DISP`` column). Background image corresponds to Maca landslide in Planet 2021 image.

Interpolation of surface displacements
'''''''''''''''''''''''''''''''''''''''''''''''''

To visualize the displacement field as a raster, you can interpolate the ``DISP`` column of the ``Correlated points`` layer using the ``IDW interpolation`` or ``Heatmap`` tool in QGIS. You can also interpolate the ``DX`` and ``DY`` columns to obtain the displacement along columns (EW) and rows (NS), respectively. The result should be similar to :numref:`fig_imcorr_interpolation`.

.. _fig_imcorr_interpolation:

.. figure:: /_static/image_correlation/Fig8_imcorr_interpolation.png
   :width: 100%
   :align: center
   :alt: IMCORR interpolation

   Interpolation of the ``DISP`` column of the ``Correlated points`` layer using the ``Heatmap`` tool in QGIS. Background image corresponds to Maca landslide in Planet 2021 image.

.. question:: Questions for discussion
   :collapsible: closed

   - What do you think of the results obtained with IMCORR?
   - What are the main patterns of displacement that you can observe?
   - What do you think about the noise-level of the displacement field?
   - What are the main sources of errors?
   - What are the advantages and limitations of the IMCORR algorithm?
   - How would you improve the results obtained with IMCORR?

.. _compute_surf_disp_asp:

Compute surface displacements with ASP
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To measure surface displacements field using Ames Stereo Pipeline (ASP), you will use the different correlator strategies developed in the ASP software. Among them, the classic Block Matching (BM) algorithm and the Normalised Cross Correlation (NCC) cost-function (for correlation quality) are the most commonly used. The process initially requires 2 images as main input data. However, there is several parameters that can be tuned to improve the quality of the results. For instance, the size of the correlation window (or kernel), the type of correlation algorithm (BM, Semi-Global Matching (SGM), etc), the refinement of the correlation function (subpixel-mode). In this practice, we will use the ``parallel_stereo`` command to compute the displacement fields and the ``corr_eval`` command to compute a quality metric (NCC) of the correlation process.

The window size is fixed to 21x21. It can be tuned by using the option --corr-kernel. Other parameters, like the type of correlation algorithm or the refinement of the correlation function, can also be tuned. For instance the refinement mode 2 (Bayes mode) is the slowest one, but also the most precise. If you want a more rapid evaluation of your displacement fields, use subpixel-mode 1 (parabola fitting).

.. seealso:: Ames Stereo Pipeline (ASP)
   The NASA `Ames Stereo Pipeline (ASP) <https://stereopipeline.readthedocs.io/en/latest/introduction.html>`_ is an open-source photogrammetric software, to generate DEM from either multiple satellite, airborne or ground-based images on the Earth and other planetary bodies (Mars, Moon, etc). This software is designed to produce DEM's using stereo or multiple-stereo pairs of optical images. For more detailed and complete information please refer to NASA ASP web page. Read on Ames Stereo Pipeline: :cite:`beyer2018` & :cite:`shean2016`.

Download the data
''''''''''''''''''''''''''

This second part of the exercise will be done using ASP software. This exercise will be run on Linux (e.g. WSL or Virtual Machine) or MAC operating system.

.. important::

   Download a set of Planet images (2018-2025) over the Maca landslide. You can use the provided script located in ``/psf_telrisknat_2025_docs/data/download_excercise_2_data.sh`` as follow:

   1. Open a terminal and navigate to the ``/psf_telrisknat_2025_docs/data/`` directory.

   .. code-block:: bash

      cd ~/psf_telrisknat_2025_docs/data/

   2. Run the following command:

   .. code-block:: bash

      bash download_excercise_2_data.sh

Prepare the images
'''''''''''''''''''''''''''

As for IMCORR, ASP requires **single band images** with the **same number of columns** (``width``) and **lines** (``height``). So, you will need to first extract the red band (band 3) from both Planet images and then clip them to the same extent. As we provide the data ready for processing, we wont provide the details here:

.. code-block:: bash

   gdal_translate -of GTiff -co COMPRESS=None -co NBITS=16 \
   -b 3 <image-input.tif> <image-output-B3.tif>

Image correlation using ``parallel_stereo``
'''''''''''''''''''''''''''''''''''''''''''''''''''''

Now, you can run the ``parallel_stereo`` command with the following parameters:

.. code-block:: bash

   parallel_stereo --correlator-mode --stereo-algorithm asp_bm --subpixel-mode 2 \
   --threads 16 --corr-kernel 21 21 \
   Maca_20180805_B3.tif Maca_20210805_B3.tif run/run-corr-20180805-20210805

The output directory ``run`` contains ``run-corr-20180805-20210805-F.tif`` (3 bands):

- Band 1: **EW** (column) displacement (pixels)
- Band 2: **NS** (row) displacement (pixels)
- Band 3: **GoodPixelMap** (raster mask of valid pixels)

Quality metric (NCC)
'''''''''''''''''''''''''''''''''
To evaluate the quality of the correlation process, estimated by the cross-correlation coefficient (CC), you must run the following command: 

.. code-block:: bash

   corr_eval --kernel-size 21 21 --metric ncc --prefilter-mode 2 --threads 16 \
   Maca_20180805_B3.tif Maca_20210805_B3.tif run/run-corr-20180805-20210805-F.tif run/run-corr-20180805-20210805

This comand creates a raster file named ``run/run-corr-20180805-20210805-ncc.tif`` with values in **[0, 1]**. The NCC files contain a raster where their values are coded between 0 and 1, where values close to 0 have low correlation and values close to 1 have good correlation.

Harmonizing data for better analysis and visualization
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Now you will separate first band and second, which corresponds to ``EW`` and ``NS``. Run the following commands:

.. code-block:: bash

   gdal_translate -of GTiff -co COMPRESS=None -co NBITS=16 -b 1 \
   run/run-corr-20180805-20210805-F.tif EW_20180805_20210805.tif

.. code-block:: bash

   gdal_translate -of GTiff -co COMPRESS=None -co NBITS=16 -b 2 \
   run/run-corr-20180805-20210805-F.tif NS_20180805_20210805.tif

.. code-block:: bash

   mv run/run-corr-20180805-20210805-ncc.tif CC_20180805_20210805.tif

Convert from pixels to metres
'''''''''''''''''''''''''''''''''''''''''

Note that contrary to ``IMCORR`` algorithm, ASP provides surface displacement in pixels. To convert it into meters, you must multiply by the pixel resolution (in this case 3m). You can use the raster calculator of QGIS to do so, or directly with the gdal library. Run the following commands:

.. code-block:: bash

   gdal_calc.py -A EW_20180805_20210805.tif --outfile=EWm_20180805_20210805.tif --calc="A*3"

.. code-block:: bash

   gdal_calc.py -A NS_20180805_20210805.tif --outfile=NSm_20180805_20210805.tif --calc="A*-3"

Once the results are converted, you can use QGIS environments to visualise the results ::numref:`fig_asp_outputs`.

.. _fig_asp_outputs:

.. figure:: /_static/image_correlation/Fig9_asp_outputs.jpg
   :width: 100%
   :align: center
   :alt: ASP outputs

   ASP outputs in QGIS: Left: ``EWm_20180805_20210805.tif``, Right: ``NSm_20180805_20210805.tif``. Background image corresponds to Maca landslide hillshade.

We will now compute the total displacement field (See :eq:`eq-disp`). For that, we will use the output of the previous results using the following formula:

.. :math:`\mathrm{DISP} = \sqrt{\mathrm{EWm}^2 + \mathrm{NSm}^2}`

.. math::
   :label: eq-disp

   \mathrm{d} = \sqrt{\mathrm{EWm}^2 + \mathrm{NSm}^2}

where ``d`` is magnitude displacements in meters, ``NSm`` is raster displacements of the North-Sud component in meters, ``EWm`` is raster displacements of the East-West component in meters.

You can use the raster calculator of QGIS to do so, or directly with the gdal library. Run the following command:

.. code-block:: bash

   gdal_calc.py -A EWm_20180805_20210805.tif -B NSm_20180805_20210805.tif \
   --outfile=DISPm_20180805_20210805.tif --calc="sqrt(A**2 + B**2)"

.. question:: Questions for discussion
   :collapsible: closed

   Load the ``EW_20180805_20210805.tif``, ``NS_20180805_20210805.tif`` and ``CC_20180805_20210805.tif`` files in QGIS to visualize them.

   - What do you think of the results obtained with ASP?
   - What are the main patterns of displacement that you can observe?
   - What do you think about the noise-level of the displacement field?
   - What are the main sources of errors?
   - What are the advantages and limitations of the ASP algorithm?

Bias correction in surface displacements
'''''''''''''''''''''''''''''''''''''''''''''''''''

When inspecting the images in QGIS, you may notice that two of them are not perfectly georeferenced due to gyroscope errors on the satellite. There may be a bias of up to 10 m between them. This bias is clearly visible in stable areas where motion should be **close to zero**. However, as can be seen in :numref:`fig_asp_outputs`, this is not the case. To remove this bias, we need to visualise the east-west (EW) and north-south (NS) histograms in QGIS :numref:`fig_asp_bias_correction`, evaluate the value at the peak and subtract it separately for the EW and NS bands.

.. _fig_asp_bias_correction:

.. figure:: /_static/image_correlation/Fig10_asp_bias_correction.jpg
   :width: 100%
   :align: center
   :alt: ASP bias correction

   Surface displacement histograms in QGIS: Left: ``EWm_20180805_20210805.tif``, Right: ``NSm_20180805_20210805.tif``.

In order to correct this bias, you can use either the ``raster calculator`` in QGIS or directly with the gdal library to do this subtraction. Run the following commands:

.. code-block:: bash

   gdal_calc.py -A EWm_20180805_20210805.tif --outfile=EWm_20180805_20210805_bc.tif --calc="A-2.0"

.. code-block:: bash

   gdal_calc.py -A NSm_20180805_20210805.tif --outfile=NSm_20180805_20210805_bc.tif --calc="A+4.6"

Finally, you can compute the total displacement and surface velocity as follows:

.. code-block:: bash

   gdal_calc.py -A EWm_20180805_20210805_bc.tif -B NSm_20180805_20210805_bc.tif \
   --outfile=DISPm_20180805_20210805_bc.tif --calc="sqrt(A**2 + B**2)"

Visualize the displacement field overlayed over a hillshade DEM (if you have one, either over the satellite image in B&W). Adjust the transparency of the displacement ``layer right-clicking on the layer -> Properties``. The results should be similar to :numref:`fig_asp_bias_corrected_outputs`.

.. _fig_asp_bias_corrected_outputs:

.. figure:: /_static/image_correlation/Fig11_asp_bias_corrected_outputs.jpg
   :width: 100%
   :align: center
   :alt: ASP bias corrected outputs

   ASP bias corrected outputs in QGIS: ``DISPm_20180805_20210805_bc.tif``. Background image corresponds to Maca landslide hillshade.

.. tip::
   ASP do not provide the displacement vectors as IMCORR. However, you can create them in QGIS. Take a look `at this tutorial <https://www.youtube.com/watch?v=y2b7URF8lZg>`_.

.. question:: Questions for discussion
   :collapsible: closed

   Load the ``DISPm_20180805_20210805.tif`` and ``DISPm_20180805_20210805_bc.tif`` files in QGIS and compare them.

   - What do you think of the results obtained with ASP after bias correction?
   - What are the main patterns of displacement that you can observe?
   - What do you think about the noise-level of the displacement field?
   - What are the main sources of errors?
   - What are the advantages and limitations of the ASP algorithm?

Evaluation of the data quality
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have obtained the displacement fields with both IMCORR and ASP (or any other algorithm), the questions is **How to evaluate the data quality?**

Some aspects to consider include:

.. tip::

   - **Comparison with ground truth data**: If available, compare the displacement fields with in-situ measurements or other reliable data sources to assess accuracy. For instance on the Maca landslide, 3 permanent GNSS enabled this comparison :numref:`fig_data_quality_evaluation`. This point-to-point evaluation allows us to give confidence to feature tracking results.
   - **Statistical analysis**: Calculate statistics such as mean, median, standard deviation, and interquartile range to quantify the displacement field characteristics. This can be done using **stable areas** where no displacement is expected (e.g., areas with no known ground movement :cite:`cusicanqui2025_LandsatImagery`). However, you should pay attention on how those **stable areas** are defined.
   - **Uncertainty estimation**: Assess the uncertainty associated with the displacement measurements, which can be influenced by factors such as image resolution, correlation window size, and image quality. For instance a standard deviation (STD) of the EW and NS measurements component on a stable area can be used to evaluate the uncertainties.
   - **Visual inspection**: Look for obvious errors, such as unrealistic displacements or patterns that do not make sense given the context of the study area.
   - **Cross-validation**: If multiple displacement fields are available (e.g., from different algorithms or time periods), compare them to identify consistent patterns and potential biases.

.. _fig_data_quality_evaluation:

.. figure:: /_static/image_correlation/Fig12_data_quality_evaluation.jpg
   :width: 100%
   :align: center
   :alt: Data quality evaluation

   Example of data quality evaluation using in-situ GNSS data on the Maca landslide :cite:`lacroix2020`. Time-series of displacement measured by a GNSS installed on the Maca landslide.

To go further
~~~~~~~~~~~~~~~~~~

.. important::
   **Do it yourself!!**
   
   **Congratulations!!** Now you have the basic knowledge on how to compute surface displacement using both IMCORR algorithm in QGIS and ASP. To go further:

   - Replicate the same process using other PlanetScope pair images available in the directory ``data/excercice_2_image_correlation/maca_planet``. For instance, you can use the 2021-2025 pair.

References
~~~~~~~~~~~~~~~~~~

.. bibliography::
   :cited:
   :style: unsrt