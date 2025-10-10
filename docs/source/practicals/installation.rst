..
   Copyright (c) 2025 PSF TelRIskNat 2025 Optical team
   SPDX-License-Identifier: CC-BY-NC-SA-4.0
   author: Diego Cusicanqui (CNES | ISTerre | Univ. Grenoble Alpes)

   This file is part of the “PSF TelRIskNat 2025” workshop documentation.
   Licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0).
   You may share and adapt for non-commercial purposes, with attribution and ShareAlike.
   See: https://creativecommons.org/licenses/by-nc-sa/4.0/

.. _installation:

Installation of necessary software
------------------------------------

For this workshop, we will rely on open-source software, mainly:

- `Ames Stereo Pipeline (ASP) <https://stereopipeline.readthedocs.io/en/latest/introduction.html>`_ (to generate DEMs and correlate images).
- `QGIS <https://qgis.org/en/site/forusers/download.html>`_ (to visualize and analyze geospatial data).
- `Python <https://www.python.org/>`_ (version 3.7 or higher).
- `Jupyter Notebook <https://jupyter.org/>`_ (to run Python code in your browser).
- `Geoutils <https://geoutils.readthedocs.io/en/stable/>`_ (to handle raster and vector geospatial data).
- `xDEM <https://xdem.readthedocs.io/en/stable/>`_ (to handle DEM coregistration and perform DEM differencing).

However, ASP only run in Linux and MacOS. If you are using Windows, you have two options:

a. **Use the Windows Subsystem for Linux (WSL)** to run a Linux environment on your Windows machine.

b. **Set up a virtual machine** with a Linux distribution.

.. _setring_wsl:

Setting up WSL (lightest option if you have Windows 10 or higher)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

a. Enable WSL on your Windows machine by following the instructions in the official `Microsoft documentation: <https://learn.microsoft.com/en-us/windows/wsl/install-manual>`_

b. Restart your computer if prompted.

c. Install a Linux distribution from the Microsoft Store (e.g., Ubuntu). `https://learn.microsoft.com/en-us/windows/wsl/install <https://learn.microsoft.com/en-us/windows/wsl/install>`_.

d. Once installed, launch the Linux distribution and follow the prompts to set up your user account.

.. note::
    In this `Youtube video <https://www.youtube.com/watch?v=zZf4YH4WiZo>`_ you can find a visual guide on how to set up WSL.

Once installed, please follow the instructions in :ref:`install_packages` to install the necessary packages.

.. _setting_vm:

Setting up a virtual machine (more resource-intensive)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Download and install a virtualization software like `VirtualBox <https://www.virtualbox.org/>`_ or `VMware Workstation Player <https://www.vmware.com/products/workstation-player.html>`_.

- Create a new virtual machine and install a Linux distribution (e.g., Ubuntu) on it.

- Once the virtual machine is set up, follow the instructions in :ref:`install_packages` to install the necessary packages.

.. note::
    This option requires more system resources (RAM, CPU) compared to WSL. Ensure your computer meets the requirements for running a virtual machine smoothly.
    You can follow this Youtube video on `How to install Linux distribution on virtual machine <https://www.youtube.com/watch?v=dKJ3Wee8w9w>`_ with more details

.. _install_packages:

Installation of necessary packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

a. First, update the package lists and install the necessary packages by running the following commands in the Linux terminal:

.. code-block:: bash
   
   sudo apt update && sudo apt upgrade -y

b. Then, you need to create a virtual environment with all the necessary packages. We will use ``miniconda`` from the official `Conda website <https://docs.conda.io/en/latest/miniconda.html>`_. Follow the installation instructions for your operating system.

  - Open your terminal and run the following commands:

  .. code-block:: bash

      wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

  .. code-block:: bash

      bash Miniconda3-latest-Linux-x86_64.sh

  - Follow the prompts to complete the installation.

  - Close and reopen your terminal to activate conda.

  Finally, you will install ``mamba`` to make package management faster:

  .. code-block:: bash

      conda install mamba -n base -c conda-forge

c. Third, clone the PSF TelRiskNat 2025 repository. You can do this by running the following command in your terminal:

.. code-block:: bash

    git clone https://github.com/cusicand/psf_telrisknat_2025_docs.git

d. Navigate to the cloned repository:

.. code-block:: bash

    cd psf_telrisknat_2025_docs

e. Now, you will install the Ames Stereo Pipeline (ASP). For this exercise, we provide a ``bash script`` for automatic installation. You can install it using conda with the following command:

.. code-block:: bash

    bash ./scripts/install_ASP.sh

To make ASP commands available in your terminal, you need to add the ASP binary path to your ``.bashrc`` file. You can do this by running the following command:

.. code-block:: bash

    echo 'export PATH=$HOME/ASP_install/StereoPipeline-3.5.0-2025-04-28-x86_64-Linux/bin:$PATH' >> ~/.bashrc && source ~/.bashrc

.. seealso::
    You can find all the instructions in the official `ASP documentation <https://stereopipeline.readthedocs.io/en/latest/installation.html>`_.

f. Verify the installation by running. Execute the ``stereo --help`` command in the terminal. If you see the help message, the installation was successful:

.. code-block:: console

    $ stereo --help
    usage: stereo [options] <images> [<cameras>] <output_file_prefix> [DEM]
        Extensions are automatically added to the output files.
        Camera model arguments may be optional for some stereo
        session types (e.g. isis). Stereo parameters should be
        set in the stereo.default file.
    3.5.0

    options:
    -h, --help            show this help message and exit
    -t SESSION, --session-type SESSION
                            Select the stereo session type to use for processing. Usually the program
                            can select this automatically by the file extension, except for xml
                            cameras. See the doc for options.
    -s STEREO_FILE, --stereo-file STEREO_FILE
                            Explicitly specify the stereo.default file to use. Default:
                            ./stereo.default.
    --corr-seed-mode SEED_MODE
                            Correlation seed strategy. See stereo_corr for options.
    -e ENTRY_POINT, --entry-point ENTRY_POINT
                            Pipeline entry point (an integer from 0-5)
    --stop-point STOP_POINT
                            Stereo Pipeline stop point (an integer from 1-6).
    --sparse-disp-options SPARSE_DISP_OPTIONS
                            Options to pass directly to sparse_disp.
    --threads THREADS     Set the number of threads to use. 0 means use as many threads as there are
                            cores.
    --no-bigtiff          Tell GDAL to not create bigtiffs.
    --tif-compress TIF_COMPRESS
                            TIFF compression method. Options: None, LZW, Deflate, Packbits. Default:
                            LZW.
    -v, --version         Display the version of software.
    --check-mem-usage     Check stereo_corr run time and memory usage.

g. Now, you have create a new conda environment with all the necessary Python packages using the provided ``psf_env.yml`` file:

.. code-block:: bash

    mamba env create -f psf_env.yml

h. Activate the newly created environment:

.. code-block:: bash

    conda activate psf_env

.. hint::
    If the environment is activated, you have successfully installed all the necessary packages. You can now proceed to the practical sessions.

.. _install_qgis:

Installation of QGIS for data visualization (windows or linux independently)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Finally, you need to install QGIS for data visualization. You can download it from the official `QGIS website <https://qgis.org/en/site/forusers/download.html>`_.

a. Make sure to download the version compatible with your operating system (Windows or Linux).
b. Make sure you install SAGA software during the QGIS installation process, as it is required for some geospatial analyses. See this video for more details: `How to install QGIS with SAGA <https://www.youtube.com/watch?v=Erwg2BRLnNA>`_.
