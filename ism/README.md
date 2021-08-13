# Repo for ISM Spring '21 assignments

All code is found in hw2.py, broken up into four sections delineated by comment blocks. First block relates Tg (gas kinetic temperature) to the conversion factor. There's some asymptotic behavior that is either attributable to user error, unrealistic code, or actual physical behavior in log-decreasing order of probability, so I zoomed in on that low-temperature behavior in xco_vs_tg_zoomin.eps. Accordingly, xco_vs_tg_zoomout.eps shows the relation including higher temperatures. xco_vs_tg_hightemps.eps, which omits temperatures below 10K and now includes temperatures from 100K to 1000K, shows an exponential decrease in XCO with temperature. 

The second block relates velocity dispersion, sigmaNT, to conversion factor, XCO. Apparently there doesn't seem to be much change in XCO until sigmaNT gets to regions of 1000 cm/s and higher. From there, XCO decreases almost sigmoidally with increasing velocity dispersion, but I guess that's what happens when you logscale everything. The third block relates the surface density, Sigma_mol to XCO. From class, Sigma_mol is taken to be the product of alphaCO (virial parameter) and WCO (velocity-integrated brightness temperature, intTb). alphaCO itself is related to sigmaNT^2 (and mass, but we're just fixing that at an arbitrary 1e6 solar mass). Again, XCO decreases with increasing Sigma_mol (no surprise if Sigma_mol is positively related to sigmaNT via alphaCO). 

The fourth block was when I hadn't read the docs and thought I had to use the data from cloudfiles to make the relation. Maybe that *is* what we had to do? Anyway, the _cloudfiles are there for temperature and sigmaNT relations, and include the ^13CO as well as CO lines (hence the paired dots on the plots).  


