
Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <http://keepachangelog.com/en/1.0.0/>`_
and this project adheres to `Semantic Versioning <http://semver.org/spec/v2.0.0.html>`_.

0.0.2
----------

**Changed**


**Added**

Add ifkast modules for `ur5`, `kuka_kr6_r900`, `abb_irb4600`. `abb_irb4600` test fails some time randomly - need to regenerate its IKfast cpp files (might be the floating point truncation issue).

Include the upstreamed `ur_kinematics commit 6734142 July 2 2019 <https://github.com/ros-industrial/universal_robot/tree/9eccd19077c2e7b853e3a3215bce9f38b77adda5/ur_kinematics>`__
but it seems that the old one works more stably... I will do more tests on this.

**Removed**