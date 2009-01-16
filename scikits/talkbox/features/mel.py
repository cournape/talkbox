import numpy as np

def hz2mel(f):
    """Convert an array of frequency in Hz into mel."""
    return 1127.01048 * np.log(f/700 +1)

def mel2hz(m):
    """Convert an array of frequency in Hz into mel."""
    return (np.exp(m / 1127.01048) - 1) * 700
