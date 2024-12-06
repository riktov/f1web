def collapse_trail(trail):
    """
    >>> collapse_trail([])
    []

    >>> collapse_trail([5])
    [5]

    >>> collapse_trail([5, 2])
    [5, 2]

    >>> collapse_trail([5, 5])
    [5]

    >>> collapse_trail([1, 5, 5, 5, 13, 2, 5, 13, 4, 19])
    [1, 5, 13, 4, 19]

    >>> collapse_trail([1, 5, 13, 2, 5, 4, 19])
    [1, 5, 4, 19]

    >>> collapse_trail([1, 5, 13, 2, 5, 13, 4, 19])
    [1, 5, 13, 4, 19]

    >>> collapse_trail([1, 5, 5, 19])
    [1, 5, 19]
    """
    collapsed = []

    for i in range(len(trail)):
        s = trail[i]
        collapsed.append(s)
        if i < len(trail):
            rest = trail[i + 1:]
            if s in rest:
                ridx = list(reversed(rest)).index(s)
                idx = len(rest) - ridx
                return collapsed + collapse_trail(rest[idx:])
    
    return collapsed

if __name__ == "__main__":
    import doctest
    doctest.testmod()