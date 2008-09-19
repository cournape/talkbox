# Simplest periodogram: no smoothing (no kernel, no tapping), no detrend.
p = spectrum(lh, plot=FALSE, detrend=FALSE, taper=0.0)
print(p$spec)
