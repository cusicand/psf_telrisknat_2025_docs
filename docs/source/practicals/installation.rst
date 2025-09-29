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

1. Use the Windows Subsystem for Linux (WSL) to run a Linux environment on your Windows machine.

2. Set up a virtual machine with a Linux distribution.

.. _setring_wsl:

Setting up WSL (lightest option if you have Windows 10 or higher)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Enable WSL on your Windows machine by following the instructions in the official `Microsoft documentation: <https://learn.microsoft.com/en-us/windows/wsl/install-manual>`_

2. Restart your computer if prompted.

3. Install a Linux distribution from the Microsoft Store (e.g., Ubuntu). `https://learn.microsoft.com/en-us/windows/wsl/install <https://learn.microsoft.com/en-us/windows/wsl/install>`_.

4. Once installed, launch the Linux distribution and follow the prompts to set up your user account.

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

1. First, update the package lists and install the necessary packages by running the following commands in the Linux terminal:

.. code-block:: bash
   
   sudo apt update && sudo apt upgrade -y

2. Then, you need to create a virtual environment with all the necessary packages. We will use ``miniconda`` from the official `Conda website <https://docs.conda.io/en/latest/miniconda.html>`_. Follow the installation instructions for your operating system.

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

3. Third, clone the PSF TelRiskNat 2025 repository. You can do this by running the following command in your terminal:

.. code-block:: bash

    git clone https://github.com/cusicand/psf_telrisknat_2025_docs.git

4. Navigate to the cloned repository:

.. code-block:: bash

    cd psf_telrisknat_2025_docs

5. Now, you will install the Ames Stereo Pipeline (ASP). For this exercise, we provide a ``bash script`` for automatic installation. You can install it using conda with the following command:

.. code-block:: bash

    bash ./install_ASP.sh

.. seealso::
    You can find all the instructions in the official `ASP documentation <https://stereopipeline.readthedocs.io/en/latest/installation.html>`_.

6. Verify the installation by running. Execute the ``stereo --help`` command in the terminal. If you see the help message, the installation was successful:

.. command-output:: stereo --help

1. Next, create a new conda environment with all the necessary Python packages using the provided ``psf_env.yml`` file:

.. code-block:: bash

    mamba env create -f psf_env.yml

8. Activate the newly created environment:

.. code-block:: bash

    conda activate psf_env

.. hint::
    If the environment is activated, you have successfully installed all the necessary packages. You can now proceed to the practical sessions.

.. _install_qgis:

Installation of QGIS for data visualization (windows or linux independently)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Finally, you need to install QGIS for data visualization. You can download it from the official `QGIS website <https://qgis.org/en/site/forusers/download.html>`_.

1. Make sure to download the version compatible with your operating system (Windows or Linux).
2. Make sure you install SAGA software during the QGIS installation process, as it is required for some geospatial analyses. See this video for more details: `How to install QGIS with SAGA <https://www.youtube.com/watch?v=Erwg2BRLnNA>`_.
