#!/usr/bin/env python

from SkyNet import *
import numpy as np

nuclib = NuclideLibrary.CreateFromWinv("/projects/jina/jina_bianca/Winv/winvn_v3.0_sky_z60")

opts = NetworkOptions()
opts.ConvergenceCriterion = NetworkConvergenceCriterion.Mass
opts.MassDeviationThreshold = 1.0E-10
opts.IsSelfHeating = True
opts.EnableScreening = True

screen = SkyNetScreening(nuclib)
helm = HelmholtzEOS(SkyNetRoot + "/data/helm_table.dat")

strongReactionLibrary = REACLIBReactionLibrary("/evtdata/jina1/Skynet_Ashley/nucdata/reaclibs/reaclib2_nb22_2",
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
weakReactionLibrary = REACLIBReactionLibrary("/evtdata/jina1/Skynet_Ashley/nucdata/reaclibs/reaclib2_nb22_2",
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

T0 = 10.0    # initial temperature in GK
Ye = 0.3   # initial Ye
s = 14    # initial entropy in k_B / baryon
tau = 6   # expansion timescale in ms

# run NSE with the temperature and entropy to find the initial density
nse = NSE(net.GetNuclideLibrary(), helm, screen)
nseResult = nse.CalcFromTemperatureAndEntropy(T0, s, Ye)

densityProfile = ExpTMinus3(nseResult.Rho(), tau / 1000.0);

output = net.EvolveSelfHeatingWithInitialTemperature(nseResult.Y(), 0.0, 1.0E5,
    T0, densityProfile, "/projects/jina/jina_ashley/conditiongrid/Skynet_14_0.3")

NetworkOutput.MakeDatFile("/projects/jina/jina_ashley/conditiongrid/Skynet_14_0.3.h5")

#YvsA = np.array(output.FinalYVsA())
#A = np.arange(len(YvsA))

#np.savetxt("/projects/jina/jina_ashley/r-process_runs/r-process_new/final_12_frdm", np.array([A, YvsA]).transpose(),
#    "%6i  %30.20E")
