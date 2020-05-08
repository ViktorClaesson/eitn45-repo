import numpy as np


class InfoTheory:

    def expect(self, p):
        if p == 0:
            return 0
        else:
            return -p * np.log2(p)

    def BinaryEntropy(self, p):
        return self.expect(p) + self.expect(1 - p)

    def VectorEntropy(self, P):
        return sum([self.expect(p) for p in P])

    def Entropy(self, P):
        # Input P:
        #   Matrix (2-dim array): Each row is a probability
        #       distribution, calculate its entropy,
        #   Row vector (1Xm matrix): The row is a probability
        #       distribution, calculate its entropy,
        #   Column vector (nX1 matrix): Derive the binary entropy
        #       function for each entry,
        #   Single value (1X1 matrix): Derive the binary entropy
        #       function
        #   Output:
        #       array with entropies

        if P.shape[1] > 1:
            H = [self.VectorEntropy(Pv) for Pv in P]
        else:
            H = [self.BinaryEntropy(Pv[0]) for Pv in P]

        return np.array(H)

    def MutualInformation(self, P):
        # Derive the mutual information I(X;Y)
        #   Input P: P(X,Y)
        #   Output: I(X;Y)

        Pt = np.transpose(P)
        Px = np.array([[sum(P[row]) for row in range(P.shape[0])]])
        Py = np.array([[sum(Pt[col]) for col in range(Pt.shape[0])]])

        Hx = self.Entropy(Px)[0]
        Hy = self.Entropy(Py)[0]
        Hxy = sum(self.Entropy(P))
        I = Hx + Hy - Hxy

        return np.array([I])


if __name__ == '__main__':
    # init
    IT = InfoTheory()
    # 1st test
    P1 = np.transpose(np.array([np.arange(0.0, 1.1, 0.25)]))  # row vector
    H1 = IT.Entropy(P1)
    print('H1 =', H1)
    # 2nd test
    P2 = np.array([[0.3, 0.1, 0.3, 0.3],
                   [0.4, 0.3, 0.2, 0.1],
                   [0.8, 0.0, 0.2, 0.0]])
    H2 = IT.Entropy(P2)
    print('H2 =', H2)
    # 3rd test
    P3 = np.array([[0, 3/4], [1/8, 1/8]])
    I3 = IT.MutualInformation(P3)
    print('I3 =', I3)
    # 4th test
    P4 = np.array([[1/12, 1/6, 1/3],
                   [1/4, 0, 1/6]])
    I4 = IT.MutualInformation(P4)
    print('I4 =', I4)
