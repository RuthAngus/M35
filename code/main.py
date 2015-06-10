import numpy as np
import matplotlib.pyplot as plt
import k2_get_id as kgi

def load_data():
    ID, _, _, _, _, _, _, _ = np.genfromtxt("../data/bouy.dat", skip_header=50,
                                            dtype=str, invalid_raise=False).T
    _, RA, dec, g, gerr, r, rerr, P = \
            np.genfromtxt("../data/bouy.dat", skip_header=50,
                          invalid_raise=False).T
    return ID, RA, dec, g, gerr, r, rerr, P

if __name__ == "__main__":

    ID, ra, dec, g, gerr, r, rerr, P = load_data()
    m = P > .95
    ra, dec = ra[m], dec[m]

    # get extension and object ID
    ext, objid = kgi.ra_dec_search(ra, dec, campaign="C00", verbose=False)
    print ext
