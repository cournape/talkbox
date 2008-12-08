
def find_peaks(x, neighbours):
    peaks = []
    nx = x.size

    assert 2 * neighbours + 1 <= nx

    if nx == 1:
        peaks.append(0)
        return peaks
    elif nx == 2:
        if x[0] > x[1]:
            peaks.append(0)
        else:
            peaks.append(1)
            return peaks

    # Handle points which have less than neighs samples on their left
    for i in range(neighbours):
        cur = x[i]
        m = x[i+1]
        # look at the left of the current position
        for j in range(i):
            if m < x[j]:
                m = x[j]
        # look at the right of the current position
        for j in range(i+1, i+neighbours):
            if m < x[j]:
                m = x[j]

        if cur > m:
            peaks.append(i)
            #assert(pkcnt <= (nx / neighbours + 1))

    # Handle points which have at least neighs samples on both their left
    # and right
    for i in range(neighbours, nx - neighbours):
        cur = x[i]
        m = x[i+1];
        # look at the left
        for j in range(i - neighbours, i):
            if m < x[j]:
                m = x[j]
        # look at the right
        for j in range(i+1, i+neighbours):
            if m < x[j]:
                m = x[j]

        if cur > m:
            peaks.append(i)
            #assert(pkcnt <= (nx / neighbours + 1))

    # Handle points which have less than neighs samples on their right
    for i in range(nx - neighbours, nx):
        cur = x[i]
        m = x[i-1]
        # look at the left
        for j in range(i - neighbours, i):
            if m < x[j]:
                m = x[j]

        # look at the right
        for j in range(i+1, nx):
            if m < x[j]:
                m = x[j]

        if cur > m:
            peaks.append(i)
            #assert(pkcnt <= (nx / neighbours + 1))

    return peaks
