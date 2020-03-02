# Thesis

## Structure

- `plot.py` defines a few functions which take care of plotting the desired histogram on the (sub)canvas(es).
- `plotVariables.py` defines a class for the leptons, as well as some usefull utilities and all possible variables we might want to make a histogram of.
- `makeHists.py` takes care of the filling of the histograms as well as applying the selection criteria on the events.
- `leptonPlots.py` can be seen as the main program; It initializes histograms and fills them by calling functions from `makeHist.py`. When the histograms are filled, it calls for the `plot.py` script to make beautiful plots.
- `cutflow.py` is a script which is made for the sole purpose of creating cutflow tables in a LaTeX format.
- `cuts.py` defines a class used to apply the selection criteria.

## Data structure

- In the `\*.stack` files, the sources which will be used in the plots are given. The goal is that one can just choose a stack file and the program will then only use the sources given by this stack file and ignore all other sources. However, this is not implemented fully yet. The `\*.stack` files also give the desired color and legend label (in LaTeX) for one background.

- In the `\*.conf` files, all samples from a given year are listed with their directory on the t2b network and their cross-section.

## TO DO

- Match sources from stack files to the actual root files given by the conf files
- Work on the naming of programs and functions
- Maybe: restrict Wmass funtion from using b-tagged jets for W mass calculation, possibly resulting in the inability to reconstruct two W masses for each events due to a lack of light jets
- Apply BDT and/or NN to data
- Generalize creating a legend in various positions (now hardcoded)
- Generalize setting the yrange
- Change for _ in tree
- Make a progressbar
- New top reconstruction script, possibly use Kirills code
- Maybe: only save seperate histos when making them and stack them at plotting time, with the possibility of determining the order of plotting at that time as well (for instance for mll put ttbar bkg on bottom)
- Update structure
- Using TTH MVA for now, get back to using tZq MVA (changed in both cuts.py and plotVariables.py)
- Make programs compatible with submitting jobs to cream02
- Maybe write script reduceTuple which handles applying the cuts to one bkg/sign source at a time and saves results in a new .root file, special for this bkg/sign source. This makes for easier parallelization.
- Remake cutflow table
- Improve plotter script (now using TList of hists)
- Make it such that `makeHists.py` is able to assign different bkg/signal source files to one and the same histogram

## Recently done

- Finish `cutflow.py` script
- Reconstruct W and top mass
- Fix the amount of jets: two of the jets are actually the two leptons!
- Reduce trees for ML training
- Normalize trees
- Check eta coverage electrons and muons
- Save the histograms in a .pkl format such that they don't have to be remade everytime you want to change the plotting style...
- Make plotter program just handle the .pkl histos, also call this script when making the histos
