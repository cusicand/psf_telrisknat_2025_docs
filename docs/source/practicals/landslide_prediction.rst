..
   Copyright (c) 2025 PSF TelRIskNat 2025 Optical team
   SPDX-License-Identifier: CC-BY-NC-SA-4.0
   author: Diego Cusicanqui (CNES | ISTerre | Univ. Grenoble Alpes)

   This file is part of the “PSF TelRIskNat 2025” workshop documentation.
   Licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0).
   You may share and adapt for non-commercial purposes, with attribution and ShareAlike.
   See: https://creativecommons.org/licenses/by-nc-sa/4.0/

.. _landslide_prediction:

Landslide prediction using time series of displacement
------------------------------------------------------------
..
   .. figure:: /_static/Fig0_patience.jpg
      :width: 100%
      :align: center
      :alt: be patient

      Advice from PSF TelRiskNat optical team.


**Pascal LACROIX**\ :sup:`1` & **Diego CUSICANQUI**\ :sup:`1`

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
~~~~~~~~~~~~~~~~~~~~~~~

- Visualize time-series of landslide displacements from different sensors.
- Predict the occurrence time of a landslide failure.
- Understand the notions of uncertainties on landslide displacements.


Introduction
~~~~~~~~~~~~~~~~~~~~~~~

Landslides are a major threat in most mountainous environments of the world provoking almost 10,000 casualties each years. It has been observed that landslides can be preceded by a phase of acceleration, emphasizing the interest for detecting slow motions of the ground, and monitoring their motion though time. Landslide displacement can be measured from a large amounts of techniques, including in situ measurements :cite:`federico2012`, or from remote sensing images :cite:`lacroix2020`.

For this practice, you will study the latest phase of acceleration of 2 landslides before their failure to try to predict their occurrence time, based on two types of measurements:
1. TLS measurements installed in front of the Chambon landslide (France), and
2. Time-series of displacement coming from satellite images over the Achoma landslide (Peru).

About the studied Landslides
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Chambon landslide
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The **Chambon landslide** :numref:`chambon_landslide` : is located in the French Alps along the Chambon artificial lake reservoir, affecting lower Jurassic sedimentary rocks (Lias). The landslide affects the tunnel of the road linking Grenoble to Briançon. The tunnel closed in April 2015 after the emergence of several surface fissures :cite:`desrues2019`. On July a major but incomplete rupture of the landslide occurred. As a consequence, all of the actors of the landslide risk management team decided to increase the lake level to purge the remaining unstable masses. The landslide involved a mass of about 250x100x25 m\ :sup:`3`.

.. _chambon_landslide:

.. figure:: /_static/landslide_prediction/Fig1_chambon_landslide.jpg
   :alt: Chambon landslide
   :width: 100%
   :align: center
   :figclass: align-center

   View of the Chambon landslide (France) in July 2015 after the major rupture. The red arrow indicates the location of the TLS installed in front of the landslide.

.. important::
   For a detailed information on Chambon landslide:

   Desrues, M., Lacroix, P., & Brenguier, O. (2019). Satellite Pre-Failure Detection and In Situ Monitoring of the Landslide of the Tunnel du Chambon, French Alps. Geosciences, 9(7), 313. https://doi.org/10.3390/geosciences9070313 

The Achoma landslide
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The **Achoma landslide** :numref:`achoma_landslide` : is situated in the Colca valley in Peru which is a wide depression filled with lacustrine sediments deposited over the last 1Myr, after a major debris avalanche coming from the Hualca hualca volcanic complex damed the valley. After the breaching of the dam, Colca river started to incise the soft clayey sediments and initiated landsliding in the whole area. The Achoma landslide, of approximate size 500x500x80 m\ :sup:`3` was triggered in June 2020, 2 months after the end of the rainy season. It destroyed cultures and blocked the Colca river, creating a lake, threatening the inhabitants downstream.

.. _achoma_landslide:

.. figure:: /_static/landslide_prediction/Fig2_achoma_landslide.jpg
   :alt: Achoma landslide
   :width: 100%
   :align: center
   :figclass: align-center

   View of the Achoma landslide (Peru) in August 2020 after its triggering.

.. important::
   For a detailed information about landslides in Colca valley:

   Zerathe, S., Lacroix, P., Jongmans, D., Marino, J., Taipe, E., Wathelet, M., Pari, W., Smoll, L. F., Norabuena, E., Guillier, B., and Tatard, L. (2016) Morphology, structure and kinematics of a rainfall controlled slow-moving Andean landslide, Peru. Earth Surf. Process. Landforms, 41: 1477–1493. doi: `10.1002/esp.3913 <https://doi.org/10.1002/esp.3913>`_. 

.. _landslide_occurrence_prediction:

Landslide occurrence time prediction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this section, you will try to predict the occurrence time of the two landslides based on their latest phase of acceleration before rupture. For some landslides, that experience progressive maturation of faults, :cite:`fukuzono1985` found that the logarithm of the landslide acceleration (:math:`\ddot{\eta}`) in its last stage before failure is proportional to the logarithm of its velocity (:math:`\dot{\eta}`), i.e.:

.. math::
   :label: eq-fukuzono

   \ddot{\eta}(t) = a\,\dot{\eta}(t)^{\alpha}

Integrating this equations for a :math:`\alpha > 1`, one obtains:

.. math::
   :label: eq-fukuzono-solution

   \dot{\eta}(t) = \left[a\,(\alpha - 1)\,\bigl(t_f - t\bigr)\right]^{-\frac{1}{\alpha - 1}}

In the specific case where :math:`\alpha = 2`, which is a close assumption for the tertiary creep of landslides, the equation reduces to the Saito Formula :cite:`saito1969`:

.. math::
   :label: eq-saito

   \bigl(t_f - t\bigr)\,\dot{\eta}(t) = A

This equation indicates that the time to failure :math:`t_f` in tertiary creep is inversely proportional to the current strain rate or velocity. Plotting the inverse velocity of the landslide as a function of time therefore allows the estimation of the landslide failure, as represented in Figure 3.

.. _fig-inverse-velocity:

.. figure:: /_static/landslide_prediction/Fig3_inverse_velocity.jpg
   :alt: Inverse velocity method
   :width: 60%
   :align: center
   :figclass: align-center

   Linear Fukuzono model application and the corresponding R² value, with a detail of the intersection between the linear regression and the x-axis. From :cite:`segalini2018`.

.. important::
   For a detailed information on the pre-failure landslide accelerations:

   Federico, A., Popescu, M., Elia, G. et al. Prediction of time to slope failure: a general framework. Environ Earth Sci 66, 245–256 (2012). https://doi.org/10.1007/s12665-011-1231-5

Practical work
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Chambon data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A network of 24 of topographic targets was set set up area in in June 2015 by the SAGE society :numref:`fig-chambon-targets`. Seven targets were were located located in around the movement and 17 and on the unstable mass. Planimetric and altimetric displacements were regularly recorded thanks to an automatic theodolite placed in the southern side of the lake in front of the movement. The automatic theodolite placed in the southern side of the lake in front of the movement. The measurement frequency was 1.5 h with a precision of 2 mm, as estimated from the standard deviation calculated on targets located in the stable parts. For this practice you will use the data from the target C15.

.. _fig-chambon-targets:

.. figure:: /_static/landslide_prediction/Fig4_chambon_targets.jpg
   :alt: Chambon targets
   :width: 80%
   :align: center
   :figclass: align-center

   Left: Position of the topographic targets on the Chambon landslide; Right: Cumlative displacements in meters of the selected topographic targets :cite:`desrues2019`.

Achoma data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Year 2020 was one of the wettest rainy season from the last 30 years, that ended up in April 2020. Local inhabitants noted in June 2020 the existence of large fissures, but, after investigations from the Peruvian Geological office no monitoring was set up for different reasons, including the little risk posed to inhabitants (no habitations) and the lack of technical people to take charge of this monitoring during covid lowdown time. Therefore, the geodetical data analyzed in this practice comes from the reanalysis of remote-sensing images. Specifically from the correlation of Planet satellite images. Planet satellites enabled a quasi daily monitoring of the landslide with uncertainties of between 0.5 and 1 m. The interest of satellite images is the possibility of having spatially extended measurements. Here we selected only one point in the most rapid area.

Practice
~~~~~~~~~~~~~

Load the data
^^^^^^^^^^^^^^^^^^^^^
.. important::
   For this practice, you will use ``Excel`` or ``LibreOffice`` to visualize the displacement as a function of the date as a scatter plot.

   The data used in this exercise can be downloaded from:

   - :download:`TP_Achoma.xlsx </_static/landslide_prediction/TP_Achoma.xlsx>`
   - :download:`TP_Chambon.xlsx </_static/landslide_prediction/TP_Chambon.xlsx>`

Plot the data
^^^^^^^^^^^^^^^^^^^^^

Compute the landslide velocity using the ``Excel`` tools. Note the acceleration before the landslide failure.

.. question:: Questions for discussion
   :collapsible: closed
   
   - Is the acceleration progressive?
   - When did it start?

Predict the time of failure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Based on the Fukuzono method :cite:`fukuzono1985`, with :math:`\alpha = 2` (Saito method :cite:`saito1969`, :numref:`fig-inverse-velocity`), applied on the progressively accelerating part of the displacement curve (see :eq:`eq-saito` in Section :ref:`landslide_occurrence_prediction`), predict the time-to-failure of each landslide. Reiterate this process by removing the last point(s) of the time-series before the failure. Draw the estimated date of your failure prediction as a function of your last measurements.

Discussion
^^^^^^^^^^^^^^^^^^^^^

.. question:: Questions for discussion
   :collapsible: closed

   - How long in advance could have been predicted the landslide occurrence with a 1 day uncertainty? With a 2 day uncertainty? With a 1 week uncertainty
   - Discuss the pro and the cons of the satellite and in situ measurements?
   - Do you think satellite measurements could be used as a operational tool for  landslide prediction?
   - How would you improve this approach for operational landslide risk management?

.. note:: 
   You can download the solution for the practice in the following links:

   - :download:`TS_Chambon_C15.xlsx </_static/landslide_prediction/TS_Chambon_C15.xlsx>`

References
~~~~~~~~~~~~~~~~~~~~~~~

.. bibliography::
   :cited:
   :style: unsrt
