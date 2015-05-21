PconsC and PconsC2
==================

* Maja Gocevska (<gocemaja@ulb.ac.be>
* Yannick Jadoul (<yajadoul@vub.ac.be>)
* Inez Van Laer (<ivlaer@vub.ac.be>)

Python environment
------------------
This implementation of the PconsC and PconsC2 methods is written in Python, version 2.7. It needs the scipy, numpy, scikit-learn and matplotlib libraries to be installed.

Data
----
The data is assumed to be ordered in the following way, within the data folder:

    data/
      sequence_names
      sequences/
        <sequence_name>.fa
      folds/
        set<i>
      contacts/
        <sequence_name>.CB
      <method>/
        <sequence_name>.pred
      alignments/
        <sequence_name>.fa
      psipred/
        <sequence_name>.pred
      netsurfp/
        <sequence_name>.pred

The methods are assumed to be formed as *alignment*\_*E-value*\_*prediction-method*, see *constants.py*.

Running
-------
Both *pconsc.py* and *pconsc2.py* can be called with the following parameters:

* *--data*: the data folder
* *--intermediate*: a folder to save intermediate data
* *--results*: the folder where results are saved
* *--cores*: the number of cores that can be used
* *--fold*: the fold to leave out when training and to use as test data

Other important parameters of the methods can be changed in the *constants.py* source file.

When running *pconsc.py*, the folder *pconsc* should exist in the results folder. For *pconsc2.py*, *pconsc2\_layer\_<i>* has to exist for all layers for 0 to the number of extra layers.
