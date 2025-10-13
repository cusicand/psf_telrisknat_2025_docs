..
   Copyright (c) 2025 PSF TelRIskNat 2025 Optical team
   SPDX-License-Identifier: CC-BY-NC-SA-4.0
   author: Diego Cusicanqui (CNES | ISTerre | Univ. Grenoble Alpes)

   This file is part of the “PSF TelRIskNat 2025” workshop documentation.
   Licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0).
   You may share and adapt for non-commercial purposes, with attribution and ShareAlike.
   See: https://creativecommons.org/licenses/by-nc-sa/4.0/

.. _dem_generation_page:

Automatic generation of Digital Elevation Models using ASTER images
--------------------------------------------------------------------

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
~~~~~~~~~~~~~~~~~~~~~~~

- Download, visualize, and automatically generate digital elevation models (DEMs) from ASTER optical images.
- Compare multiple DEMs and compute volumetric changes (DoD).
- Use open‑source tools—**QGIS**, **GDAL**, and **Ames Stereo Pipeline (ASP)**—for satellite-image processing and analysis.

.. note::
    This exercise focuses on medium‑resolution ASTER imagery (15 m in VNIR). ASTER data are free and globally available, which makes them ideal for teaching and regional studies. For this practice, we will focus in the **Cordillera Blanca** in Peru.

Introduction
~~~~~~~~~~~~~~~~~~~~~~~

In mountainous regions, mass-wasting events can be triggered by several processes.Quantifying terrain change is essential to understand triggers, assess hazards, and support risk reduction :cite:`mergili2018`. Surface elevation change between two (or more) DEMs is a standard approach used widely—for example, to estimate glacier mass balance :cite:`dussaillant2019` and to map the geomorphic imprint of glacier lake outburst floods (GLOFs) :cite:`schneider2014`.

DEMs can be produced from aircraft (airborne photogrammetry), uncrewed aerial vehicles (UAVs), terrestrial cameras, and satellites using passive (e.g., Pléiades, WorldView, ASTER) or active sensors (e.g., SRTM, TanDEM‑X, Sentinel‑1). Each source has trade‑offs in spatial coverage, resolution, cost, and revisit; nevertheless, stereo‑photogrammetry has become a cornerstone of natural‑hazard research. For a quick summary, see Table 1 below. For an accessible overview of photogrammetry's history, see `DariaTech <https://teach.dariah.eu/mod/hvp/view.php?id=860>`_.

.. table:: Characteristics of different types of photogrammetry :cite:`cusicanqui2019_webinar2020`.
    :width: 100%
    :widths: auto

    +------------------+------------------------------------------------------+-------------------+-------------+------------------+------------------+
    |                                                                   PHOTOGRAMMETRY                                                                |
    +------------------+------------------------------------------------------+-------------------+-------------+------------------+------------------+
    |                  | Satellite                                            | Aerial            | UAV         | Terrestrial      | Time-lapse       |
    +==================+======================================================+===================+=============+==================+==================+
    | Revisite period  | 1 jour                                               | 5 – 10 ans        | 2-3 mois    | 1 mois           | < 1 jour         |
    +------------------+------------------------------------------------------+-------------------+-------------+------------------+------------------+
    | Spatial coverage | 100 - 1000 km2                                       | 10-100 km²        | 0.1 - 5 km² | 0.1 - 1 km²                         |
    +------------------+------------------------------------------------------+-------------------+-------------+------------------+------------------+
    | Resolution       | 0.3 (Worldview). 0.5 (Pléiades), 1.5 (SPOT)          | 0.3 – 2m          | 0.1 – 1m    | 0.2 – 2m         | < 1m             |
    +------------------+------------------------------------------------------+-------------------+-------------+------------------+------------------+
    | Georeference     | RCP / GCP                                            | GCP / RTK                       | GCP                                 |
    +------------------+------------------------------------------------------+-------------------+-------------+------------------+------------------+
    | Software         | Automatique : ASP, MicMac.                           | Open-source: OpenCV                                | Private pipeline |
    |                  | Semi-automatique: Erdas Imagine, ENVI, PCI Geomatica | License: Agisoft Metashape, Pix4D, OpenDroneSurvey | USMB/TENEVIA     |
    +------------------+------------------------------------------------------+-------------------+-------------+------------------+------------------+

Stereo remote sensing data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are several ways to generate DEMs from optical remote sensing data which have stereo capabilities (Table 1). However, these sources has several limitations, for instance they are commercial datasets (accessibility often requires purchase) or they are limited spatial coverage (Table 1). We demonstrate DEM generation from **ASTER L1A** stereo imagery, the most popular and freely available option for global studies. Commercial very‑high‑resolution sensors (e.g., Pléiades, WorldView) and UAV imagery are beyond the scope of this tutorial.

.. _section_aster_overview:

ASTER L1A overview
^^^^^^^^^^^^^^^^^^^^^^^^

The **Advanced Spaceborne Thermal Emission and Reflection Radiometer (ASTER)** aboard NASA’s **Terra** satellite (launched December 1999) acquires 14 spectral bands from visible to thermal infrared. A backward‑looking VNIR band (3B) paired with the nadir VNIR band (3N) enables stereo DEM generation. Spatial resolution is **15 m** (VNIR), **30 m** (SWIR), and **90 m** (TIR); each scene covers **60 × 60 km**. ASTER acquires up to ~650 scenes per day globally :numref:`fig-aster-clear-scenes`. For technical details, see the `ASTER User Handbook <https://lpdaac.usgs.gov/documents/262/ASTER_User_Handbook_v2.pdf>`_.

.. _fig-aster-clear-scenes:

.. figure:: /_static/dem_generation/Fig1_clear_scenes_aster.png
    :width: 100%
    :align: center
    :alt: Daytime and nighttime maps of the number of clear scenes with a CC of 20% or less over 10 × 10 degree grids in 19.5 years from March 2000 to August 2019.
    
    Daytime and nighttime maps of the number of clear scenes with a CC of 20% or less over 10 × 10 degree grids in 19.5 years from March 2000 to August 2019 :cite:`tonooka2019`.

.. tip::
    Accessing ASTER L1A data (Since 2000, 15m resolution, 16 days revisit time) could be possible though the following link: `https://www.earthdata.nasa.gov/ <https://www.earthdata.nasa.gov/>`_.

About the study site - Cordillera Blanca
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **Cordillera Blanca** (:numref:`fig-cordillera-blanca`) is a 200-km-long tropical mountain range in the Peruvian Andes (8°08'-9°58' S; 77°00'-77°52' W). The Cordillera Blanca is the most extensive tropical ice-covered mountain range in the world and has the largest concentration of ice in Peru. It hosts several >6,000 m peaks and hundreds of glaciers (area ~723 km²). Most glaciers (530) draining westward covering an area of 507.5 km², while 192 glaciers drains eastern convering 215.9 km² :cite:`inaigem2023`. Like other Andean glaciers, it has experienced pronounced 20th-21st century retreat :cite:`hugonnet2021`.

.. _fig-cordillera-blanca:

.. figure:: /_static/dem_generation/Fig2_cordillera_blanca.jpg
    :width: 100%
    :align: center
    :alt: Aerial view of Cordillera Blanca on 24 August 2020.

    Aerial view of Cordillera Blanca on 24 August 2020. Source: `ESA Multimedia <https://www.esa.int/ESA_Multimedia/Images/2014/05/Mount_Huascaran_Peru>`_

.. note::
    In this practice, we will learn how to automatically generate DEM's by using ASTER images. In order to improve the quality of the results, we will use a SRTM DEM as base to improve uncertainties.

.. _Section_3_2:

Download SRTM data
~~~~~~~~~~~~~~~~~~~~

First we need to download SRTM tiles (:numref:`fig-srtm-downloader`). To download SRTM tiles, you need to create an account on the `NASA Earthdata web portal <https://www.earthdata.nasa.gov/>`_. Once you have access to NASA Earthdata, go to the 30-meter SRTM tile downloader and select the tiles you are interested in. Select the tile and click the green download button.

.. _fig-srtm-downloader:

.. figure:: /_static/dem_generation/Fig3_download_srtm_tiles.jpg
    :width: 100%
    :align: center
    :alt: Download SRTM tiles from 30-Meter SRTM Tile Downloader.

    Download SRTM tiles from `30-Meter SRTM Tile Downloader <https://dwtkns.com/srtm30m/>`_.

.. important::
    As the activation of EarthData can take a long time, **we already provide SRTM tiles**. for this excersice  we will use two tiles with codes 'S09W078' and 'S10W078' :numref:`fig-srtm-downloader`. You can find the data in the directory ``DATA/DEM_GENERATION/SRTM_DEM``.

Hands-on
~~~~~~~~~~~~~

Download data for exercise 
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. important::
    Download the data for this exercise from the following commands:

    .. code-block:: bash

        cd ~/psf_telrisknat_2025_docs/data # Change directory

    .. code-block:: bash

        bash ./download_excercise_3_data.sh # Download data for exercise 3

In order to properly use the SRTM tiles as a seed DEM, we need to take some additional steps to prepare them: Extract the files inside the zip files. To do this, use the following commands:

Prepare SRTM data
^^^^^^^^^^^^^^^^^^^

.. code-block:: bash
    
    base_directory="~/psf_telrisknat_2025_docs/data/excercise_3_dems_generation"

.. code-block:: bash

    cd $base_directory/SRTM_DEM/CBLANCA # Change directory to SRTM_DEM/CBLANCA

.. code-block:: bash

    for f in *.zip; do unzip "$f"; done # Unzip zip files using for loop

Once the data extracted, you will notice that the tiles use a **Hierarchical Data Format (HDF)**. You can import the files into any GIS software (QGIS for instance). For this exercise, we need to merge all the ``*.hdf`` files to have a single ``GeoTIFF`` raster file. To do this we will use the `Geospatial Data Abstraction Library <https://gdal.org/index.html>`_, commonly known as **GDAL**. To do this, run the next command:

.. code-block:: bash

    gdal_merge.py *.hgt -o merged_DEM.tif -of GTiff # Merge all hgt files

By default, the merged DEM has the standard **WGS84 georeference**. You need to set it up correctly by using a metric georeference (i.e. WGS84 | UTM 18S for the Cordillera Blanca). To do this, run the next command:

.. code-block:: bash
    
    gdalwarp -s_srs EPSG:4326 -t_srs EPSG:32718 -r bilinear -of GTiff merged_DEM.tif DEM_REF_for_ASP.tif # Merge all hgt files

You can use the command ``gdalinfo`` command to check the results. If you dont feel confortably with comand-line interface, you can import the DEM into QGIS and then look at their properties.

Finally, go back to the base directory.

.. code-block:: bash

    cd $base_directory

Download ASTER data
^^^^^^^^^^^^^^^^^^^^^^^^^^

Now we will know how to download ASTER images. First you need to create an account on the `NASA Earthdata portal <https://www.earthdata.nasa.gov/>`_. Go to the `NASA Earthdata data search portal <https://search.earthdata.nasa.gov/search>`_ and log in. Using the map background, locate your area of interest and place a marker on the map using the tools on the right. Then search for the collection ``ASTER L1A Reconstructed Unprocessed Instrument Data V003`` and click on it (Figure 4). There are several options available on the toolbar, but a single point-marker is sufficient to select our area of interest (:numref:`fig-aster-download`).

Once the collection is open and the marker placed, you have access to the tiles that intersect the marker. You are able to filter the data by granule ID (if you know it previously), date range, cloud cover, and so on. You can now select the image of interest. Once you have selected the images, you can add them to the cue and download them all (green button in :numref:`fig-aster-download`). In the 'Processing Options' section, make sure the data format is set to GeoTIFF. Once the download is started, the EarthData web portal will prepare your data and you will receive an email with the download link.

.. _fig-aster-download:

.. figure:: /_static/dem_generation/Fig4_aster_download.jpg
    :width: 100%
    :align: center
    :alt: Downloading ASTER images from NASA Earthdata portal.

    Download ASTER images from the `NASA Earthdata <https://www.earthdata.nasa.gov/>`_ portal.

    
.. important::
    Depending on the amount of granules selected, data preparation can take a long time. For this practice, **we already provide several pairs of images** over the Cordillera Blanca and Maca region.

Step-by-step automatic DEM generation using ASP
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For this first part of the exercise, you will work using a recent ASTER image acquired on 4th, July 2023. The ASTER sensor has 15 bands in different spectral ranges. Please refer to the `ASTER User Handbook <https://lpdaac.usgs.gov/documents/262/ASTER_User_Handbook_v2.pdf>`_ for more detailed and complete information. You can use QGIS software to visualize each one of these bands by clicking on ``Layer -> Add Raster Layer``.

.. seealso:: Ames Stereo Pipeline (ASP)
    The NASA `Ames Stereo Pipeline (ASP) <https://stereopipeline.readthedocs.io/en/latest/introduction.html>`_ is an open-source photogrammetric software, to generate DEM from either multiple satellite, airborne or ground-based images on the Earth and other planetary bodies (Mars, Moon, etc). This software is designed to produce DEM's using stereo or multiple-stereo pairs of optical images. For more detailed and complete information please refer to NASA ASP web page. Read on Ames Stereo Pipeline: :cite:`beyer2018` & :cite:`shean2016`.

However, for the automatic DEM generation process, we only need the visible and near infrared (VNIR) nadir (Band3N) and backward (Band3B) bands (i.e. stereo pair images). Since processing ASTER images is a common task nowadays, the ASP team has developed several tools that allow us to prepare and process this type of sensor automatically.

Briefly, the steps to generate a DEM using ASP are:

- Prepare the ASTER images using the ``aster2asp`` command.
- Image orthorectification using the ``mapproject`` command.
- Image correlation process using ``stereo`` for dense stereo matching.
- Convert the point cloud into a DEM using the ``point2dem`` command.
- Setting vertical datum (optional).

Prepare ASTER images
'''''''''''''''''''''''''

We will first use the ``aster2asp`` command to prepare the ASTER images. This command takes an input directory of ASTER images and associated metadata, and creates ``GeoTIFF`` and ``XML`` files that can then be passed to ``stereo`` to create a point cloud. The tool can only handle Level 1A ASTER images.

.. code-block:: bash

    cd $base_directory # Change directory

First, we will copy the ASTER images to a new directory called ``RAW_L1A``. This step is important as the ``aster2asp`` command will create several intermediate files in this directory.

.. code-block:: bash

    mkdir RAW_L1A # Create directory called RAW_L1A

.. code-block::bash

    cp IMG_CBLANCA/AST_L1A*20230731* RAW_L1A/ # Copy ASTER images to RAW_L1A directory

Then, you will decompress the files using the following command:

.. code-block:: bash

    cd RAW_L1A # Change directory to RAW_L1A

.. code-block:: bash

    unzip *.zip # Unzip all zip files

Now, you are ready to run the ``aster2asp`` command. This command takes as input the directory where the ASTER images are stored (i.e. ``RAW_L1A``) and creates a new directory with the formatted images. You also need to specify the minimum and maximum height of the area of interest using the parameters ``--min-height`` and ``--max-height``. For the Cordillera Blanca, we will use 100 m and 9000 m, respectively.

.. code-block:: bash

    aster2asp RAW_L1A -o RAW_L1A/out_first --min-height 100 --max-height 9000 # Run aster2asp command

As a result of the previous commands, the ``RAW_L1A`` directory is created. Within this folder, you will find the formatted stereo pair with the following names:
- ``out-Band3B.tif`` & ``out-Band3B.xml``, corresponding to the backward image.
- ``out-Band3N.tif`` & ``out-Band3N.xml``, corresponding to the nadir image.

The process takes a few seconds (~8'') for the current tile (5000x5400 pixels). 

.. attention::
    Pay attention to correctly naming the output files on the parameter ``-o RAW_L1A/out_first``. In this command, you are naming the results as ``out-first`` to distinguish from the rest.

Finally, you can clean the ``RAW_L1A`` directory by removing the unnecessary files (i.e. ``*.txt`` and ``*.tif`` files).

.. code-block:: bash

    rm RAW_L1A/AST_L1A*.txt RAW_L1A/AST_L1A*.tif # Remove unnecessary files

Orthorectify images
'''''''''''''''''''''''''''

The next step is to orthorectify the formatted images to the seed DEM, e.g. the SRTM DEM we downloaded and prepared in :ref:`Section_3_2`. To do this, we will use the ``mapproject`` command within ASP, as shown below, for both nadir and backward images. The ``mapproject`` command takes several arguments such as the rpc session, the georeference option (WGS84 | UTM Zone 18S), the resolution of the map-projected images (i.e. 7.5m), and the seed SRTM DEM.

.. code-block:: bash
    
    mapproject -t rpc --t_srs "+proj=utm +zone=18 +south +units=m +datum=WGS84" --mpp 7.5 SRTM_DEM/CBLANCA/DEM_REF_for_ASP.tif RAW_L1A/out_first-Band3N.tif RAW_L1A/out_first-Band3N.xml RAW_L1A/out_first-Band3N_proj_SRTM.tif

.. code-block:: bash
    
    mapproject -t rpc --t_srs "+proj=utm +zone=18 +south +units=m +datum=WGS84" --mpp 7.5 SRTM_DEM/CBLANCA/DEM_REF_for_ASP.tif RAW_L1A/out_first-Band3B.tif RAW_L1A/out_first-Band3B.xml RAW_L1A/out_first-Band3B_proj_SRTM.tif

Dense stereo matching
'''''''''''''''''''''''''

Run ASP ``stereo`` to compute the point cloud (PC). The ``stereo`` command takes as input the orthorectified images and their associated XML files. This command produces an point cloud image that can be converted into a visualisable mesh or gridded DEM.

.. code-block:: bash

    stereo -t astermaprpc --corr-kernel 7 7 --subpixel-kernel 13 13 \
        --alignment-method none \
        RAW_L1A/out_first-Band3N_proj_SRTM.tif \
        RAW_L1A/out_first-Band3B_proj_SRTM.tif \
        RAW_L1A/out_first-Band3N.xml RAW_L1A/out_first-Band3B.xml \
        ASTER_DEM/out_run SRTM_DEM/CBLANCA/DEM_REF_for_ASP.tif

This process creates a directory called ``ASTER_DEM`` which contains several intermediate files created by ASP. Please refer to the `ASP stereo documentation <https://stereopipeline.readthedocs.io/en/latest/outputfiles.html>`_ for more details. The most important file for this exercise is the one ending in ``*PC.tif``, which contains information about the point cloud created during the dense stereo matching process.

Convert point cloud to DEM
'''''''''''''''''''''''''''''

Finally, we will convert the point cloud into a DEM using the ``point2dem`` command. This command takes as input the point cloud image and creates a gridded DEM. The output DEM will be in ``GeoTIFF`` format.

.. code-block:: bash

    point2dem -r earth --t_srs "+proj=utm +zone=18 +south +units=m +datum=WGS84" \
        --search-radius-factor 1.5 --tr 30. --nodata-value -9999 \
        ASTER_DEM/out_run-PC.tif -o ASTER_DEM/out_run

An intermediate step with GDAL needs to be executed to correctly setup data type to Float32 bits.

.. code-block:: bash

    gdal_translate -ot Float32 ASTER_DEM/out_run-DEM.tif ASTER_DEM/first_DEM.tif

Setting vertical datum (**optional**)
''''''''''''''''''''''''''''''''''''''

By default, the DEM generated by ASP is referenced to the WGS84 ellipsoid. However, for most applications, it is preferable to have the DEM referenced to a vertical datum such as EGM96 or EGM2008. To do this, we will use the ``dem_geoid`` tool to compute the geoid height at each pixel of the DEM.

.. code-block:: bash

    dem_geoid ASTER_DEM/first_DEM.tif --geoid EGM96 -o ASTER_DEM/first_DEM_EGM96 # Setting vertical datum to EGM96

.. code-block:: bash

    gdal_translate -ot Float32 ASTER_DEM/first_DEM_EGM96-adj.tif ASTER_DEM/DEM_20230704.tif # Convert to Float32

Finally, you can clean the ``ASTER_DEM`` directory by removing the unnecessary files (i.e. ``*PC.tif``, ``*DEM.tif``, and ``*DEM-adj.tif`` files).

.. code-block:: bash

    rm ASTER_DEM/out_run* ASTER_DEM/first_DEM*

Visualize the results
''''''''''''''''''''''''

Once the results are generated, you should be able to visualize the results using QGIS. You can also use the ``gdalinfo`` command to check the properties of the generated DEM. Your results should be similar to the one shown in :numref:`fig-aster-dem-example`.

.. _fig-aster-dem-example:

.. figure:: /_static/dem_generation/Fig5_generated_aster_dems.jpg
    :width: 90%
    :align: center
    :alt: DEM generated from ASTER images using ASP.
    
    DEM generated from ASTER images using ASP. Left: DEM visualisation; Right: DEM using hillshade effect; visualized in QGIS.

.. question:: Questions for discussion
    :collapsible: closed

    Based on your experience in this practice, answer the following questions:

    1. What is the noise level of your dataset ?
    2. What do you think about the white holes in the upper right region?
    3. Can you detect differences between ASTER DEM and SRTM DEM?
    4. What do you think is the main limitation of ASTER images?
    5. What are the advantages of using ASP for DEM generation?

Repeat the process with different ASTER images
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Do it yourself
    
    Repeat the previous steps using another ASTER image acquired on 13th, July 2003 (almost 20 years before). The data are available in the directory ``RAW_L1A/out_second``. Name the output files as ``out_second`` to distinguish from the previous results. **This step is important as we will use this second DEM to compute the difference of DEMs (DoD) in the next section**.

.. _section_dems_dod:

Compute difference of DEMs (DoD)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once the second DEM is processed, you will now compute the **Difference of DEMs (DoD)**. First, as both DEMs have different spatial extents, you need to **homogenize** into a common spatial extent. To do so, we will use the ``gdalwarp`` tool within the GDAL library.

.. code-block:: bash

    cd ASTER_DEM

.. code-block:: bash

    common_extent='168757.0 8940932.0 222493.0 9010173.0' # Define common extent

.. code-block:: bash

    gdalwarp -r bilinear -te $common_extent -of GTiff DEM_20230704.tif DEM_20230704_crop.tif # Cropping first DEM

.. code-block:: bash

    gdalwarp -r bilinear -te $common_extent -of GTiff DEM_20030713.tif DEM_20030713_crop.tif # Cropping second DEM

Then, you will use the module of raster calculator ``gdal_calc.py`` within GDAL to compute the difference of DEMs.

.. code-block:: bash

    gdal_calc.py -A DEM_20030713_crop.tif -B DEM_20230704_crop.tif --outfile DoD_2023-2003.tif --calc="B-A"

The command ``gdal_calc.py`` will generate a new raster file containing the difference between the two generated DEMs. Open this raster in QGIS software. Modify the color scale values ``Min`` and ``Max`` values of the band between -50 and +50. You should obtain something similar to :numref:`fig-dod-2023-2003`.

.. _fig-dod-2023-2003:

.. figure:: /_static/dem_generation/Fig6_dod_2023-2003_example.jpg
    :width: 100%
    :align: center
    :alt: Difference of DEMs (DoD) generated from ASTER images using ASP between 2003 and 2023.
    
    Difference of DEMs (DoD) generated from ASTER images using ASP between 2003 and 2023. Visualized in QGIS.

.. question:: Questions for discussion
    :collapsible: closed

    Based on your experience in this practice, answer the following questions:

    1. What is the noise level of your dataset ?
    2. What do you think about the white holes in the upper right region?
    3. Can you detect differences between ASTER DEM and SRTM DEM?
    4. What do you think is the main limitation of ASTER images?
    5. What are the advantages of using ASP for DEM generation?

To go further (bonus)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As mentioned in Section 3.4, the processing of ``ASTER L1A RAW`` images has become standard in recent years. Together with the ``DEM_GENERATION`` dataset, we provide a bash script called ``make_ASTER-DEM_ASP.sh``, which is used to automatically process multiple `ASTER images <https://github.com/FannyBrun/ASTER_DEM_from_L1A>`_ by running a single script. This is based on the :cite:`brun2017` and :cite:`dussaillant2019` studies and was modified/adapted for this practice. To run this command, first copy all the ASTER tiles you want to process into the same folder (e.g. ``RAW_L1A``). Then go to the parent directory and run the following command indicating the folder where images are stored and the seed DEM:

.. code-block:: bash

    bash ./make_ASTER-DEM_ASP.sh RAW_L1A SRTM_DEM/CBLANCA/DEM_REF_for_ASP.tif

.. admonition:: Do it yourself!!

    **Congratulations!!** Now you have the basic knowledge on how to compute ASTER DEM automatically using ASP. To go further:

    - Replicate the same process using other ASTER images available in the directory ``RAW_L1A``.
    - Replicate the same process for another region. You can use the data provided in the directory ``IMG_MACA``.

References
~~~~~~~~~~~~~~

.. bibliography::
    :cited:
    :style: unsrt

