PSF TelRIskNat 2025 workshop
=============================

This **PSF TelRIskNat 2025** repository contains a set of notebooks to showcase how to handle georeferenced (raster, vector) files for surface velocity estimation using `Ames Stereo Pipeline <https://stereopipeline.readthedocs.io/en/latest/introduction.html>`_, run DEM analysis in Python using `geoutils <https://geoutils.readthedocs.io/en/stable/>`_ and `xDEM <https://xdem.readthedocs.io/en/stable/>`_.

.. image:: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
    :target: https://creativecommons.org/licenses/by-nc-sa/4.0/
    :alt: License: CC BY-NC-SA 4.0

How to install 
----------------------------------------

The examples can be downloaded and run on your computer by installing the necessary packages with conda.
Simply download the content of this repository ("code" button on the top-right or in command-line

.. code-block:: bash
    git clone https://github.com/cusicand/psf_telrisknat_2025_docs.git

Then run the following commands separately:

.. code-block:: bash
    conda env create -f psf_env.yml

.. code-block:: bash
    conda activate psf_env
