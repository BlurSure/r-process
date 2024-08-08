#!/usr/bin/env python

from SkyNet import *
import numpy as np
import sys

reaclib = "/mnt/home/agarw132/jina/nucdata/reaclibs/reaclib2_e40_bcpm"
winvname = "winvn_v3.0_sky_bcpm_z60"
nuclib = NuclideLibrary.CreateFromWinv("/mnt/home/agarw132/jina/nucdata/nuclibs/" + str(winvname))

opts = NetworkOptions()
opts.ConvergenceCriterion = NetworkConvergenceCriterion.Mass
opts.MassDeviationThreshold = 1.0E-10
opts.IsSelfHeating = True
opts.EnableScreening = True

screen = SkyNetScreening(nuclib)
helm = HelmholtzEOS(SkyNetRoot + "/data/helm_table.dat")

strongReactionLibrary = REACLIBReactionLibrary(str(reaclib),
  ReactionType.Strong, True, LeptonMode.TreatAllAsDecayExceptLabelEC,
  "Strong reactions", nuclib, opts, True)
symmetricFission = REACLIBReactionLibrary(SkyNetRoot
  + "/data/netsu_panov_symmetric_0neut", ReactionType.Strong, False,
  LeptonMode.TreatAllAsDecayExceptLabelEC,
  "Symmetric neutron induced fission with 0 neutrons emitted", nuclib, opts,
  False)
spontaneousFission = REACLIBReactionLibrary(SkyNetRoot +
  "/data/netsu_sfis_Roberts2010rates", ReactionType.Strong, False,
  LeptonMode.TreatAllAsDecayExceptLabelEC, "Spontaneous fission", nuclib, opts,
  False)

# use only REACLIB weak rates
weakReactionLibrary = REACLIBReactionLibrary(str(reaclib),
    ReactionType.Weak, False, LeptonMode.TreatAllAsDecayExceptLabelEC,
    "Weak reactions", nuclib, opts, True)

# or use the following code to use FFN rates and weak REACLIB rates pre-computed
# with the <SkyNetRoot>/examples/precompute_reaction_libs.py script

# ffnMesaReactionLibrary = FFNReactionLibrary.ReadFromDisk(
#     "ffnMesa_with_neutrino", opts)
# ffnReactionLibrary = FFNReactionLibrary.ReadFromDisk(
#     "ffn_with_neutrino_ffnMesa", opts)
# weakReactionLibrary = REACLIBReactionLibrary.ReadFromDisk(
#     "weak_REACLIB_with_neutrino_ffnMesa_ffn", opts)

# add neutrino reactions, if desired (will need a neutrino distribution
# function set with net.LoadNeutrinoHistory(...))
# neutrinoLibrary = NeutrinoReactionLibrary(SkyNetRoot
#     + "/data/neutrino_reactions.dat", "Neutrino interactions", nuclib, opts,
#     1.e-2, False, True)

reactionLibraries = [strongReactionLibrary, symmetricFission,
    spontaneousFission, weakReactionLibrary]

# reactionLibraries = [strongReactionLibrary, symmetricFission,
#     spontaneousFission, weakReactionLibrary, neutrinoLibrary,
#     ffnMesaReactionLibrary, ffnReactionLibrary]

net = ReactionNetwork(nuclib, [weakReactionLibrary, strongReactionLibrary,
    symmetricFission, spontaneousFission], helm, screen, opts)

# this part creates an array that is essentially just permutations of different condition combinations such that each command line entry via sys corresponds to exactly one combination of s and Ye
s_list = list(range(10, 52, 2))
s_arr = np.array(s_list)
Ye_list = list(range(200, 435, 5))
Ye_arr = np.array(Ye_list) / 1000

def long_Ye(yee):
    long_Ye = []
    for i in s_list:
        long_Ye.append(yee)
    return long_Ye
def chunk(yee):
    return np.column_stack((long_Ye(yee), s_arr))
permulist = []
for y in Ye_arr:
    permulist.append(chunk(y))

parr = np.array(permulist)
plist = parr.tolist()
empty=[]
for new_lst in plist:
    for new_new in new_lst:
        empty.append(new_new)
permarr = np.array(empty)


T0 = 10.0    # initial temperature in GK
Ye = float(permarr[int(sys.argv[1])][0])
s = int(permarr[int(sys.argv[1])][1])    # initial entropy in k_B / baryon
tau = 6   #int(sys.argv[2])   # expansion timescale in ms

# run NSE with the temperature and entropy to find the initial density
nse = NSE(net.GetNuclideLibrary(), helm, screen)
nseResult = nse.CalcFromTemperatureAndEntropy(T0, s, Ye)

densityProfile = ExpTMinus3(nseResult.Rho(), tau / 1000.0);

output = net.EvolveSelfHeatingWithInitialTemperature(nseResult.Y(), 0.0, 1.0E5,
                                                     T0, densityProfile, "/mnt/scratch/agarw132/jina/r_process_grid_bcpm/Skynet_y" + str(Ye) + "_s" + str(s))

YvsA = np.array(output.FinalYVsA())
A = np.arange(len(YvsA))

np.savetxt("/mnt/scratch/agarw132/jina/r_process_grid_bcpm/final_y" + str(Ye) + "_s" + str(s), np.array([A, YvsA]).transpose(),
    "%6i  %30.20E")
