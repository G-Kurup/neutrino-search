# neutrino-search


###  Binary classifier for collider events using a neural network:



The `NeutrinoFinder.ipynb` notebook creates and trains a simple 3-layer feed forward network that classifies Standard Model (SM) events and Beyond Standard Model (BSM) events with clockwork sterile neutrinos. Standard Model events are the 'background' events that we expect at a collider, that follow from the Standard Model of particle physics. BSM events are collision events that contain non-SM particles that we would like to detect ('signal'). Clockwork neutrino models* in particular, contain sequences of massive sterile neutrinos that interact weakly with the Standard Model and provide a "natural" extension that explains the smallness of SM neutrinos.

Both signal and background events were generated using MadGraph,Pythia and Delphes**. MadGraph uses Monte Carlo simulations to generate parton-level events, Pythia hadronizes the generated partons, and Delphes applies detector effects. Read the clockwork neutrino paper (linked below) for details of the collider events, as well as the traditional (non-ML) collider analysis that was done. `.lhco` or LHC Olympics files are the default format for the output of these packages, and contain kinematic and detector observables for each detected particle of an event. 

The events in .lhco files were processed into flattened, padded vectors using the `ProcessLHCO.py` python script in the same repo. 

The datasets used in this notebook contain proton-proton collision events at a centre of mass energy of 14 TeV, producing hadronic jets. This simulates data that will be collected at the Large Hadron Collider in its high-luminosity run. To generate your own clockwork neutrino model events using MadGraph, Pythia and Delphes, use the code in the clockwork-neutrino-lhco-pipeline repo. 

The code generalizes easily to different models and signals. To use your own signal and background events, generate .lhco files using MadGraph and copy signal events and SM events into the ./sig and ./bkg sub-directories respectively. Run `ProcessLHCO.py` and `NeutrinoFinder.ipynb` in the same directory. 


*Read the paper [here.](https://arxiv.org/abs/1903.06191)

**[MadGraph5_aMC@NLO](http://madgraph.phys.ucl.ac.be), [Pythia](pythia.org), and [Delphes](https://github.com/delphes/delphes) are particle physics packages used to generate realistic collider events.
