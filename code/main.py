import numpy as np
import matplotlib.pyplot as plt
import k2_get_id as kgi

def load_data():
    ID, _, _, _, _, _, _, _ = \
		    np.genfromtxt("../data/bouy.dat", skip_header=50,
                                  dtype=str, invalid_raise=False).T
    _, RA, dec, g, gerr, r, rerr, P = \
            np.genfromtxt("../data/bouy.dat", skip_header=50,
                          invalid_raise=False).T
    return ID, RA, dec, g, gerr, r, rerr, P

if __name__ == "__main__":

    ID, ra, dec, g, gerr, r, rerr, P = load_data()
    m = P > .95
    print len(ra)
    np.savetxt("m35_coords.txt", np.transpose((ra, dec)))
    assert 0
    RAs, DECs = ra[m], dec[m]

    for i, ra in enumerate(RAs):
	    ext, objid = kgi.ra_dec_search(ra, DECs[i], "C00", verbose=False)
	    print ext, i, "of", len(RAs), objid
	    ras, decs, objidlist, maglist = kgi.get_ras_decs_fluxes(ext, "C00")
	    print ras, decs
	    mag, corr_mag, model_tot, model_comp, model_err, time = \
			    kgi.get_lightcurve(ext, objid, "C00", mode="roll",
					       lcdir="/kepler/kepler2/K2/C00/lc/")
	    ndata = mag.shape[0]

# 	    objid = kgi.ra_dec_search_multi(ra, DECs[i], ras, decs,

	    if np.isfinite(corr_mag[0]): print "yes"
	    else: print "no", corr_mag[0]

#     mag, corr_mag, model_tot, model_err, time, rel_mag, rel_flux, flux_err = \
# 		    [np.zeros((nobj, ndata)) for i in range(8)]
#     model_comp = np.zeros((nobj, 3, ndata))
#     exts, objids = [], []

    print time
    np.savetxt("data", np.transpose((time, mag, corr_mag, model_tot)))
