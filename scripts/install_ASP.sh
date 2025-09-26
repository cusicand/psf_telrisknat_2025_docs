#!/bin/bash

dir=$HOME/ASP_install

mkdir $dir
cd $dir
wget https://github.com/NeoGeographyToolkit/StereoPipeline/releases/download/3.5.0/StereoPipeline-3.5.0-2025-04-28-x86_64-Linux.tar.bz2
tar -xvf StereoPipeline-3.5.0-2025-04-28-x86_64-Linux.tar.bz2

export PATH=$HOME/ASP_install/StereoPipeline-3.5.0-2025-04-28-x86_64-Linux/bin:$PATH