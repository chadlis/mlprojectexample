# Servier - Drug molecule properties prediction



Model
--------
A first model using the fingerprints extraction was tested only in a jupyter notebook with the same split (see `notebooks/SCH_Model1_01.ipynb`)

The implemented model is `MPNN - Message-passing neural network`.

MPNN is a graph neural network. It is based on
- This paper: https://arxiv.org/abs/1704.01212
- This implementation: https://keras.io/examples/graph/mpnn-molecular-graphs/ | https://deepchem.readthedocs.io/en/latest/api_reference/models.html#mpnnmodel

Traditional methods (like the one used in Model 1) do the feature extraction part separately.
An advantage of this kind of models is that the feature extraction is integrated in the model and tuned in the fitting process.

The MPNN of this tutorial consists of three stages: message passing, readout and classification. <br />

`Message passing` <br />
The message passing step itself consists of two parts:

1. The edge network, which passes messages from the neighbors of a node v to the node v, based on the edge features between them, resulting in an updated node  v'.

2. The gated recurrent unit (GRU), which takes as input the most recent node state and updates it based on previous node states. 

Importantly, step (1) and (2) are repeated for k steps, and where at each step 1...k, the radius (or number of hops) of aggregated information from v increases by 1.

&nbsp;