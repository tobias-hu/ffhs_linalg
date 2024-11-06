"""
Created on: 21.10.2024
Author: Tobias Gasche
Description: Class spat generates a spat, given methods set camera and project spat onto z=0
"""

import matplotlib.pyplot as plt
import numpy as np


def checkCoordinates(x, xMin, y, yMin, z, zMin):
    """
    Checks if the coordinates are within the bounds
    :param x:
    :param xMin:
    :param y:
    :param yMin:
    :param z:
    :param zMin:
    :return:
    """
    if x < xMin or y < yMin or z < zMin:
        raise Exception("Coordinates out of bounds. xMin: {}, yMin: {}, zMin: {}".format(xMin, yMin, zMin))


def plotLevels(points, plot, twoDimensional=False):
    """
    Plots the sidelines of the top and bottom level of a spat or his projection
    :param points:
    :param plot:
    :param twoDimensional:
    :return:
    """

    colors = ['red', 'blue', 'red', 'blue', 'magenta', 'brown', 'magenta', 'brown']

    for i in range(0, 8):
        j = i + 1
        if j % 4 == 0:
            j = j - 4

        x, y = ([points[i][0], points[j][0]],
                [points[i][1], points[j][1]])

        if not twoDimensional:
            z = [points[i][2], points[j][2]]
            plot.plot(x, y, z, c=colors[i])
        else:
            plot.plot(x, y, c=colors[i])


def plotSidelines(points, plot, twoDimensional=False):
    """
    Plots the sidelines between top and bottom levels of a spat or his projection
    :param points:
    :param plot:
    :param twoDimensional:
    :return:
    """
    colors = ['darkgreen', 'purple','darkgreen', 'purple']
    for i in range(0, 4):
        x, y = ([points[i][0], points[i + 4][0]],
                [points[i][1], points[i + 4][1]])

        if not twoDimensional:
            z = [points[i][2], points[i + 4][2]]
            plot.plot(x, y, z, c=colors[i])
        else:
            plot.plot(x, y, c=colors[i])


def getCoordinatesByAxis(points):
    """
    Gets the coordinates of the given points and reorders them into x,y and z coordinate-lits
    :param points:
    :return:
    """
    xCoordinates = [points[i][0] for i in range(len(points))]
    yCoordinates = [points[i][1] for i in range(len(points))]
    zCoordinates = [points[i][2] for i in range(len(points))]

    return [xCoordinates, yCoordinates, zCoordinates]


def _drawProjection(points):
    """
    Plots the projection on the xy-level
    :param points:
    :return:
    """
    x = [points[i][0] for i in range(len(points))]
    y = [points[i][1] for i in range(len(points))]

    # points
    plt.scatter(x, y, c='r')

    # label points
    pointNames = ["A'", "B'", "C'", "D'", "E'", "F'", "G'", "H'"]
    for x,y,i in zip(x,y,range(len(points))):
        plt.text(x, y, pointNames[i])


    # top and bottom
    plotLevels(points, plt, True)

    # sidelines
    plotSidelines(points, plt, True)

    plt.show()


class Spat:
    """
    The spat class
    """

    def __init__(self, x, y, z):
        """
        Initializes the spat
        Takes the x,y and z coordinates for the origin, which is in fact the first corner of the spat
        raises an error if the coordinates are outside the first octant of the coordinate system
        :param x:
        :param y:
        :param z:
        """
        self.u = np.array([4, 2, 1])
        self.v = np.array([2, 5, 1])
        self.w = np.array([1, 2, 8])

        try:
            checkCoordinates(x, 1, y, 1, z, 1)
        except ValueError as err:
            raise err

        self.origin = np.array([x, y, z])

        self.points = self.__calcPoints()

        self.cameraPoints = []

    def __calcPoints(self):
        """
        Calculates the corners of the spat with the given origin and the defined vectors (@see __init__)
        :return:
        """

        # bottom
        A = np.array(self.origin)
        B = self.origin + self.u
        C = self.origin + self.u + self.v
        D = self.origin + self.v

        # top
        E = self.origin + self.w
        F = self.origin + self.w + self.u
        G = self.origin + self.w + self.u + self.v
        H = self.origin + self.w + self.v

        return [A.tolist(), B.tolist(), C.tolist(), D.tolist(), E.tolist(), F.tolist(), G.tolist(), H.tolist()]

    def getPoints(self):
        """
        Just a normal getter method
        :return:
        """
        return self.points

    def drawSpat(self):
        """
        Draws the spat
        Which is not actually part of the paper, but it helped me to see what's going on...
        :return:
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # get x,y,z coordinates of all the points
        coordinatesByAxis = getCoordinatesByAxis(self.points)
        x = coordinatesByAxis[0]
        y = coordinatesByAxis[1]
        z = coordinatesByAxis[2]

        ax.set_xlabel('X-Achse')
        ax.set_ylabel('Y-Achse')
        ax.set_zlabel('Z-Achse')

        ax.scatter(x, y, z, c='r', marker='o')

        # Label points
        pointNames = ["A","B","C","D","E","F","G","H"]
        for x,y,z,i in zip(x,y,z,range(len(x))):
            ax.text(x,y,z,pointNames[i])

        # TOP AND BOTTOM
        plotLevels(self.points, ax)

        # SIDELINES
        plotSidelines(self.points, ax)

        plt.show()

    def setCamera(self, x, y, z):
        """
        Takes the camera position and checks if it is allowed to be there
        If everything is ok, the camera coordinates are set
        :param x:
        :param y:
        :param z:
        :return:
        """
        spatCoordinates = getCoordinatesByAxis(self.points)
        spatzCoordinates = spatCoordinates[2]

        zMax = max(spatzCoordinates)

        checkCoordinates(x, 1, y, 1, z, zMax + 1)

        self.cameraPoints = [x, y, z]

    def _projectPoint(self, x, y, z):
        """
        Calculates the projection of the given point to the xy-level
        :param x:
        :param y:
        :param z:
        :return:
        """
        cameraX = self.cameraPoints[0]
        cameraY = self.cameraPoints[1]
        cameraZ = self.cameraPoints[2]

        projectionX = (cameraX * z - x * cameraZ) / (z - cameraZ)
        projectionY = (cameraY * z - y * cameraZ) / (z - cameraZ)
        projectionZ = 0

        return [projectionX, projectionY, projectionZ]

    def project(self):
        """
        Checks if the camera coordinates are set
        Arranges the spat points to x,y,z coordinate lists
        Passes the points over to __projectPoint and then passes the projected points
        to _drawProjection
        :return:
        """
        if not self.cameraPoints:
            raise Exception("Projection not possible. Please add a camera point first.")

        # get all the points of the spat and project them
        spatCoordinates = getCoordinatesByAxis(self.points)
        projectionX = [spatCoordinates[0][i] for i in range(len(spatCoordinates[0]))]
        projectionY = [spatCoordinates[1][i] for i in range(len(spatCoordinates[1]))]
        projectionZ = [spatCoordinates[2][i] for i in range(len(spatCoordinates[2]))]

        projectedPoints = [self._projectPoint(projectionX[i], projectionY[i], projectionZ[i]) for i in
                           range(len(projectionX))]

        _drawProjection(projectedPoints)
