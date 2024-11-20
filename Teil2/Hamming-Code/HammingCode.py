"""
Created on 13.11.2024
Author: Tobias Gasche
Description: HammingCode Class. Provides methods to generate generator-matrix and check-matrix for
    Hamming-Codes. Also provides a method to check if a codeword is valid
"""

import numpy as np


def _getParityBitResponsibility(databitPositions, paritybitPositions):
    """
    Returns the responsibility of paritybits for the given paritybit- and databitpositions
    Paritybit at positon 001 is responsible for all databits at position xxx1
    Paritybit at position 010 is responsible for all databits at position xx1x
    etc.
    :param databitPositions:
    :param paritybitPositions:
    :return:
    """
    parityResponsibility = []
    for p in paritybitPositions:
        # get the index where 1 stands
        responsibleForIndex = p.index('1')

        # get indexes of databits with 1 in responsibleindex
        responsibleForDatabits = []
        i = 0
        for d in databitPositions:
            if d[responsibleForIndex] == '1':
                responsibleForDatabits.append(i)

            i += 1
        parityResponsibility.append(responsibleForDatabits)
    return parityResponsibility


def _getEinheitsMatrix(length):
    """
    returns the Einheitsmatrix for the given length
    :param length:
    :return:
    """
    E = []
    for i in range(0, length):
        inner = []
        for j in range(0, length):
            if j == i:
                inner.append(1)
            else:
                inner.append(0)
        E.append(inner)
    return np.array(E)


class HammingCode:
    """
    Provides Methods to gnerate
    generator matrix
    checkmatrix
    paritymatrix
    check codewords
    encode words
    decode codewords
    """
    def __init__(self, m):
        # Codeword length
        self.n = 2 ** m - 1
        # number of parity bits
        self.m = m
        # number of data bits
        self.k = self.n - self.m
        # EinheitsMatrix
        self.E = _getEinheitsMatrix(self.k)
        self.databitPositions, self.paritybitPositions = self._getParitybitAndDatabitPositions()
        self.parityResponsibility = _getParityBitResponsibility(self.databitPositions, self.paritybitPositions)
        # ParityMatrix
        self.A = self._getParityMatrix(self.parityResponsibility)
        # GeneratorMatrix
        self.G = self.get_generator_matrix()
        # Checkmatrix
        self.P = self.get_check_matrix()

    def get_generator_matrix(self):
        """
        returns the generatormatrix
        this is fully calculated by the given length self.m which is defined when the object is created
        :return:
        """
        G = np.vstack([self.E, self.A])
        self.G = np.array(G).transpose()
        return self.G

    def _getParityMatrix(self, parityResponsibility):
        """
        Returns the Paritymatrix.
        This is the part where it matters which paritybit is responsible for which databits
        :param parityResponsibility:
        :return:
        """
        A = []
        for element in parityResponsibility:
            vector = [0 for _ in range(len(self.E[0]))]
            for index in element:
                vector = np.array((np.array(vector) + self.E[index]) % 2)

            A.append(vector)
        self.A = np.array(A)
        return self.A

    def get_check_matrix(self):
        """
        Returns the checkmatrix
        Checkmatrix is (A.transpose | E_n-k)
        """
        At = self.A.transpose()
        Enk = _getEinheitsMatrix(self.n - self.k)
        Enk = Enk.transpose()

        self.P = np.vstack([At, Enk]).transpose()
        return self.P

    def encode(self, word):
        """
        Encodes a given word with the generatormatrix created for the given codelength
        :param word:
        :return:
        """
        if self._check_word(word):
            wordVector = [int(i) for i in str(word)]
            wordVector = np.array([wordVector])
            result = np.dot(wordVector, self.G) % 2
            return result

    def decode(self, codeword):
        """
        Decodes a given codeword
        Checks whether the codeword is valid. if it is not, the codeword is first corrected
        :param codeword:
        :return:
        """
        # first -> check codeword
        if not self.check_codeword(codeword):
            codeword = self.getCorrection(codeword)

        codeword = self._formatCodeword(codeword)
        codewordVector = [int(i) for i in codeword]
        return codewordVector[:4]

    def check_codeword(self, codeword):
        """
        Checks if the given codeword is valid
        :param codeword:
        :return:
        """
        codeword = self._formatCodeword(codeword)

        if len(codeword) != self.n:
            raise Exception("Codeword to short")

        result = self._resultOfCheckmatrix(codeword)

        return np.array_equal(result, [0, 0, 0])

    def getCorrection(self, codeword):
        """
        Returns the correction of the given codeword
        if the codeword is valid there is nothing to correct and the given codeword is returned
        :param codeword:
        :return:
        """
        codeword = self._formatCodeword(codeword)
        result = self._resultOfCheckmatrix(codeword)
        match = np.all(self.P.transpose() == result, axis=1)
        errorposition = np.where(match)[0].squeeze()

        # if there is no error, return codeword
        if errorposition.size == 0:
            return codeword

        codeword[errorposition] = (codeword[errorposition] + 1) % 2
        return codeword

    def _getParitybitAndDatabitPositions(self):
        """
        Returns the positions of the parity- and the databits corresponding to the codelength
        :return:
        """
        databitPositions = []
        paritybitPositions = []
        for i in range(0, self.n):
            if (i + 1) & i == 0:
                """position of a paritybit"""
                paritybitPositions.append(np.binary_repr(i + 1, len(np.binary_repr(self.n))))
            else:
                """position of a databit"""
                databitPositions.append(np.binary_repr(i + 1, len(np.binary_repr(self.n))))
        return databitPositions, paritybitPositions

    def _check_word(self, word):
        """
        Checks if the word is valid
        Returns true or raises exceptions
        :param word:
        :return:
        """
        if len(str(word)) != self.k:
            raise Exception("Code word has to be {} but was {}.".format(self.k, len(str(word))))

            # check characters
        for char in str(word):
            if char != '0' and char != '1':
                raise Exception("{} detected. Word has to be binary. Only use 0 and 1 characters.".format(char))

        return True

    def bitFlip(self, codeword, position):
        """
        Little helper function to flip a bit in a certain position
        returns the given codeword with a flipped bit at the given position
        :param codeword:
        :param position:
        :return:
        """
        if position > len(codeword[0]):
            raise Exception("C'mon... You can't flip more than you have!")
        if position > 0:
            position = position - 1
        if position < 0:
            raise Exception("Position can't be negative.")
        if position == 0:
            print("Position can't be 0. We don't look at it as programmers would do. I took position 1")
        codeword[0][position] = (codeword[0][position] + 1) % 2
        return codeword

    def _resultOfCheckmatrix(self, codeword):
        """
        Multiplies the checkmatrix with the codewordvector
        Returns the resulting vector
        :param codeword:
        :return:
        """
        codeWordVector = np.array([codeword]).transpose()
        result = np.dot(self.P, codeWordVector) % 2
        return np.squeeze(result)

    def _formatCodeword(self, codeword):
        """
        Helperfunction to get the codeword as list wheather it was a ndarray or an integer
        :param codeword:
        :return:
        """
        if isinstance(codeword, np.ndarray):
            if len(codeword) != 1:
                raise Exception("Codeword can only have one vector")
            codeword = codeword[0].tolist()

        if isinstance(codeword, int):
            codeword = [int(i) for i in str(codeword)]

        codeword = [int(i) for i in codeword]

        return codeword

