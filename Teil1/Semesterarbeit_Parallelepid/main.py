"""
Created on: 21.10.2024
Author: Tobias Gasche
Description: Generate a Spat object and play with projections
"""

from spat import Spat

spatInstance = Spat(1,1,1)

spatInstance.drawSpat()

spatInstance.setCamera(7,1,15)

spatInstance.project()

