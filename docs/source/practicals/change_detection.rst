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

.. figure:: /_static/Fig0_patience.jpg
   :width: 100%
   :align: center
   :alt: be patient

   Content will be soon available. Advice from PSF TelRiskNat optical team.

..
   **Floriane PROVOST**\ :sup:`1`, **Pascal LACROIX**\ :sup:`2` & **Diego CUSICANQUI**\ :sup:`2`

   \ :sup:`1` bla bla (EOST), Strasbourg, France.

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

   First of all, try to draft a workflow/diagram describing the logical steps and operations needed to answer the question. For that, answer to these questions:

   - What data do you need?
   - What information do you need?
   - What operation do you need to execute to obtain the results?

   Once answered construct the diagram.

   2. Raster data
   ~~~~~~~~~~~~~~~~~~~~~~~~

   We need to map the wild fire extent. To do that we are going to use Sentinel-2 images and manipulate the bands in order to easily detect and map the fires.

   3.1. Sentinel-2 images
   ^^^^^^^^^^^^^^^^^^^^^^^^^

   Download the Sentinel-2 bands and save/move them in ``SIG_2025/TP/TP3/DATA/Sentinel2/``.Create two folders, one for bands of acquisition 20250102 and one for acquisition 20250112.