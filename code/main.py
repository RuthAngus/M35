import numpy as np
import matplotlib.pyplot as plt
import k2_get_id as kgi
from Kepler_ACF import corr_run
import glob
import subprocess

def load_Bouy():
    ID, _, _, _, _, _, _, _, _, _ = \
		    np.genfromtxt("../data/bouy.dat", skip_header=50,
                                  dtype=str, invalid_raise=False).T
    _, RA, dec, ra_err, dec_err, g, gerr, r, rerr, P = \
            np.genfromtxt("../data/bouy.dat", skip_header=50,
                          invalid_raise=False).T
    return ID, RA, dec, ra_err, dec_err, g, gerr, r, rerr, P

def match(ID, bouy_ra, bouy_dec, ra_err, dec_err, g, gerr, r, rerr, P):

    ra, dec, p, perr, g, gerr, r, rerr = np.genfromtxt("results.txt").T
    m = (p > 0)
    plt.clf()
    plt.plot(g[m]-r[m], p[m], "k.")
    plt.show()

    # load all the data (catalogue and light curves)
    fnames = glob.glob("../lcs/*")
    ras, decs = [np.zeros(len(fnames)) for i in range(2)]
    for i, fname in enumerate(fnames):
        ras[i] = float(fname[7:21])
        decs[i] = float(fname[22:])

    # match the data
    matched_ras, matched_decs, times, fluxes = [], [], [], []
    IDs, gs, gerrs, rs, rerrs, Ps = [], [], [], [], [], []
    for i, ra in enumerate(ras):
        d = np.sqrt((ra - bouy_ra)**2 + (decs[i] - bouy_dec)**2)
        m = np.argmin(d)
        if d[m] < 1e-6:
            print "star found"
            matched_ras.append(bouy_ra[m])
            matched_decs.append(bouy_dec[m])
            gs.append(g[m])
            gerrs.append(gerr[m])
            rs.append(r[m])
            IDs.append(ID[m])
            Ps.append(P[m])
            rerrs.append(rerr[m])
            t, f = np.genfromtxt(fnames[i]).T
            times.append(t)
            fluxes.append(f)
        else: print "star not found in the Bouy catalogue"
    return IDs, np.array(matched_ras), np.array(matched_decs), gs, gerrs, rs, \
            rerrs, Ps, times, fluxes

if __name__ == "__main__":

    ID, bouy_ra, bouy_dec, ra_err, dec_err, g, gerr, r, rerr, P = load_Bouy()
    m = np.isfinite(bouy_ra) * np.isfinite(bouy_dec)
    print len(P[m])
    IDs, ras, decs, gs, gerrs, rs, rerrs, Ps, times, fluxes = \
            match(ID, bouy_ra[m], bouy_dec[m], ra_err[m], dec_err[m], g, gerr,
                  r, rerr, P)

    periods, period_errs, g, gerr, r, rerr = [], [], [], [], [], []
    for i, ra in enumerate(ras):
        m = np.isfinite(times[i]) * np.isfinite(fluxes[i])
#         corr_run(times[i][m], fluxes[i][m],
#                  np.ones_like(fluxes[i][m])*1e-5, "%s_%s" % (ras[i], decs[i]),
#                  "acf")

        # load acf results
        fname = "acf/%s_%s_result.txt" % (ras[i], decs[i])
        period, period_err = np.genfromtxt(fname).T
        periods.append(period)
        period_errs.append(period_err)
        g.append(gs[i])
        gerr.append(gerrs[i])
        r.append(rs[i])
        rerr.append(rerrs[i])
        print ras[i], decs[i], period, period_err, gs[i], gerrs[i], rs[i], rerrs[i]
        subprocess.call("open acf/%s_%s_full.png" % (ras[i], decs[i]),
                        shell=True)
        raw_input('enter')

# np.savetxt("results.txt", np.transpose((ras, decs, periods, period_errs, gs,
#            gerrs, rs, rerrs)))
plt.clf()
rs, gs, periods = np.array(rs), np.array(gs), np.array(periods)
m = periods > 0
plt.plot(gs[m]-rs[m], periods[m], "k.")
plt.show()

#     fnames = glob.glob("acf/*txt")
#     for fname in fnames:
#         period, period_err = np.genfromtxt(fname)
#         print period, period_err
#         print fname
