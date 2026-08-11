######################################
############ RPD indexes #############
######################################

######################################
# If any question please contact
# the author of the code
# marco.righi@cnr.it
######################################

import sys
import array
import datetime

sampleValue = []


def isAworstThanB(A, B):
    isAltB = None
    if A < B:
        isAltB = True
    if A > B:
        isAltB = False
    return isAltB


def RPDlep(elements):
    index = 0
    positive = []
    negative = []
    comparisionPositive = 0
    comparisionNegative = 0
    comparisionTot = 0
    for idx in range(1, len(elements)):
        comparisionTot = comparisionTot + 1
        value = abs(elements[idx - 1] - elements[idx])

        improve = isAworstThanB(elements[idx - 1], elements[idx])
        if improve is not None:  # not neutral condition
            if improve:
                comparisionPositive = comparisionPositive + 1
                positive.append(value)
            if not improve:
                comparisionNegative = comparisionNegative + 1
                negative.append(value)
    P = 0
    for idx in range(len(positive)):
        P = P + positive[idx]

    Ptot = (comparisionPositive / comparisionTot) * P

    N = 0
    for idx in range(len(negative)):
        N = N + negative[idx]

    Ntot = (comparisionNegative / comparisionTot) * N

    if (Ptot + Ntot) > 0:
        index = (Ptot - Ntot) / (Ptot + Ntot)

    return index


def RPDlea(elements):
    index = 0
    positive = []
    negative = []
    comparisionPositive = 0
    comparisionNegative = 0
    comparisionTot = 0
    for idx in range(1, len(elements)):
        comparisionTot = comparisionTot + 1
        value = abs(elements[idx - 1] - elements[idx])

        improve = isAworstThanB(elements[idx - 1], elements[idx])
        if improve is not None:  # not neutral condition
            if improve:
                comparisionPositive = comparisionPositive + 1
                element = value * comparisionPositive / comparisionTot
                positive.append(element)
            if not improve:
                comparisionNegative = comparisionNegative + 1
                element = value * comparisionNegative / comparisionTot
                negative.append(element)
    Ptot = 0
    for idx in range(len(positive)):
        Ptot = Ptot + positive[idx]

    Ntot = 0
    for idx in range(len(negative)):
        Ntot = Ntot + negative[idx]

    if (Ptot + Ntot) > 0:
        index = (Ptot - Ntot) / (Ptot + Ntot)

    return index


def RPDlepr(elements):
    index = 0
    positive = []
    negative = []
    comparisionPositive = 0
    comparisionNegative = 0
    comparisionTot = 0
    for idx in range(len(elements) - 1, 0, -1):
        comparisionTot = comparisionTot + 1
        value = abs(elements[idx - 1] - elements[idx])

        improve = isAworstThanB(elements[idx - 1], elements[idx])
        if improve is not None:  # not neutral condition
            if improve:
                comparisionPositive = comparisionPositive + 1
                element = value * comparisionPositive / comparisionTot
                positive.append(element)
            if not improve:
                comparisionNegative = comparisionNegative + 1
                element = value * comparisionNegative / comparisionTot
                negative.append(element)

    Ptot = 0
    for idx in range(0, len(positive)):
        Ptot = Ptot + positive[idx]

    Ntot = 0
    for idx in range(0, len(negative)):
        Ntot = Ntot + negative[idx]

    if (Ptot + Ntot) > 0:
        index = (Ptot - Ntot) / (Ptot + Ntot)

    return index


def RPDgep(elements):
    index = 0
    positive = []
    negative = []
    comparisionPositive = 0
    comparisionNegative = 0
    comparisionTot = 0
    for idx in range(0, len(elements) - 1):
        for idxOther in range(idx + 1, len(elements)):
            comparisionTot = comparisionTot + 1
            value = abs(elements[idx] - elements[idxOther])

            improve = isAworstThanB(elements[idx], elements[idxOther])
            if improve is not None:  # not neutral condition
                if improve:
                    comparisionPositive = comparisionPositive + 1
                    positive.append(value)
                if not improve:
                    comparisionNegative = comparisionNegative + 1
                    negative.append(value)
    P = 0
    for idx in range(len(positive)):
        P = P + positive[idx]

    Ptot = (comparisionPositive / comparisionTot) * P

    N = 0
    for idx in range(len(negative)):
        N = N + negative[idx]

    Ntot = (comparisionNegative / comparisionTot) * N

    if (Ptot + Ntot) > 0:
        index = (Ptot - Ntot) / (Ptot + Ntot)

    return index


def RPDgea(elements):
    index = 0
    positiveGroup = []
    negativeGroup = []
    for idx in range(1, len(elements)):
        comparisionTot = 0
        positive = []
        negative = []
        comparisionPositive = 0
        comparisionNegative = 0
        for idxOther in range(0, idx):
            # value=elements[idx]-elements[idxOther]
            comparisionTot = comparisionTot + 1
            value = abs(elements[idx] - elements[idxOther])

            # if the last (the head) is better than the previous...
            improve = isAworstThanB(elements[idxOther], elements[idx])
            if improve is not None:  # not neutral condition
                if improve:
                    comparisionPositive = comparisionPositive + 1
                    positive.append(value)
                if not improve:
                    comparisionNegative = comparisionNegative + 1
                    negative.append(value)
        PtmpTot = 0
        for idx in range(0, len(positive)):
            PtmpTot = PtmpTot + positive[idx]

        NtmpTot = 0
        for idx in range(0, len(negative)):
            NtmpTot = NtmpTot + negative[idx]

        positiveGroup.append(PtmpTot * comparisionPositive / comparisionTot)
        negativeGroup.append(NtmpTot * comparisionNegative / comparisionTot)

    Ptot = 0
    for idx in range(0, len(positiveGroup)):
        Ptot = Ptot + positiveGroup[idx]

    Ntot = 0
    for idx in range(0, len(negativeGroup)):
        Ntot = Ntot + negativeGroup[idx]

    if (Ptot + Ntot) > 0:
        index = (Ptot - Ntot) / (Ptot + Ntot)

    return index


def RPDgepr(elements):
    index = 0
    positiveGroup = []
    negativeGroup = []
    for idx in range(len(elements) - 2, -1, -1):
        comparisionTot = 0
        positive = []
        negative = []
        comparisionPositive = 0
        comparisionNegative = 0
        for idxOther in range(idx + 1, len(elements), +1):
            comparisionTot = comparisionTot + 1
            value = abs(elements[idx] - elements[idxOther])
            # x o -- x o o -- x o o o
            improve = isAworstThanB(elements[idx], elements[idxOther])
            if improve is not None:  # not neutral condition
                if improve:
                    comparisionPositive = comparisionPositive + 1
                    positive.append(value)
                if not improve:
                    comparisionNegative = comparisionNegative + 1
                    element = abs(value)
                    negative.append(value)
        PtmpTot = 0
        for idx in range(0, len(positive)):
            PtmpTot = PtmpTot + positive[idx]

        NtmpTot = 0
        for idx in range(0, len(negative)):
            NtmpTot = NtmpTot + negative[idx]

        if comparisionTot > 0:
            positiveGroup.append(PtmpTot * comparisionPositive / comparisionTot)
            negativeGroup.append(NtmpTot * comparisionNegative / comparisionTot)

    Ptot = 0
    for idx in range(0, len(positiveGroup)):
        Ptot = Ptot + positiveGroup[idx]

    Ntot = 0
    for idx in range(0, len(negativeGroup)):
        Ntot = Ntot + negativeGroup[idx]

    if (Ptot + Ntot) > 0:
        index = (Ptot - Ntot) / (Ptot + Ntot)

    return index

# for line in sys.stdin:
#     sampleValue.append(float(line.rstrip('\n')))
#
#
# for idx in range(0,len(sampleValue)):
#     print(sampleValue[idx])

# sampleValue=list(reversed([-1,-2,-4,-6]))
# sampleValue=list(reversed([1,2,4,6]))
# sampleValue=[1,1,1,1]
# sampleValue=[0.0183179687636068,0.66165806279797,1,6.51487788578436e-10]
#
# # chiamata funzioni
# print("RPDlep START")
# print(datetime.datetime.now())
# v=RPDlep(sampleValue)
# print("RPDlep STOP")
# print(datetime.datetime.now())
# print(v)
# print("-----")
#
# print("RPDlea START")
# print(datetime.datetime.now())
# v=RPDlea(sampleValue)
# print("RPDlea STOP")
# print(datetime.datetime.now())
# print(v)
# print("-----")
#
# print("RPDlepr START")
# print(datetime.datetime.now())
# v=RPDlepr(sampleValue)
# print("RPDlepr STOP")
# print(datetime.datetime.now())
# print(v)
# print("-----")
#
# print("RPDgep START")
# print(datetime.datetime.now())
# v=RPDgep(sampleValue)
# print("RPDgep STOP")
# print(datetime.datetime.now())
# print(v)
# print("-----")
#
# print("RPDgea START")
# print(datetime.datetime.now())
# v=RPDgea(sampleValue)
# print("RPDgea STOP")
# print(datetime.datetime.now())
# print(v)
# print("-----")
#
# print("RPDgepr START")
# print(datetime.datetime.now())
# v=RPDgepr(sampleValue)
# print("RPDgepr STOP")
# print(datetime.datetime.now())
# print(v)
