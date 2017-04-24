r'''
EoN (Epidemics on Networks)

EoN is a Python package for the simulation of epidemics on networks 
and ODE models of disease spread.

The algorithms are based on the book
        
`Mathematics of epidemics on networks: from exact to approximate 
models`
by Kiss, Miller & Simon
        http://www.springer.com/book/9783319508047
        
Please cite the book if using these algorithms

For simulations, we assume that input networks are **NetworkX** 
graphs; see https://networkx.github.io/



EoN consists of two sets of algorithms.  

- The first deals with simulation of epidemics on networks.  The most significant of these are `fast_SIS` and `fast_SIR` which significantly outperform Gillespie algorithms (also included).  These algorithms are discussed in more detail in the appendix of the book.


- The second deals with solution of systems of equations derived in the book.  For these it is possible to either provide the degree distribution, or simply use a network and let the code determine the degree distribution.


- There are a few additional algorithms which are not described in the book, but which we believe will be useful. Most notably, the function `visualize` which creates a sequence of images of a network which are appropriate for creating a movie showing disease spread.

Distributed under MIT license.  See :download:`license.txt<../license.txt>` for full details.


Auxiliary functions
-------------------
We start with a few useful auxiliary functions

'''

print("warning - EoN is currently under significant development.  Interface"
      +" may change with little if any warning until version 1.0")
print("Warning - testing in Python 3 is limited")

__author__ = "Joel C. Miller, Istvan Z. Kiss, and Peter Simon"
__version__ = "0.93"

#__all__ = 

class EoNError(Exception):
    r'''
    this will be the basic error type for EoN
    '''
    pass

def _get_rate_functions(G, tau, gamma, transmission_weight = None, 
                        recovery_weight=None):
    r'''
    Arguments:
        G : networkx Graph
            the graph disease spread on

        tau : number
            disease parameter giving edge transmission rate (subject to edge scaling)

        gamma : number (default None)
            disease parameter giving typical recovery rate, 
        
        transmission_weight : string (default None)
            `G.edge[u][v][transmission_weight]` scales up or down the recovery rate.

        recovery_weight : string       (default None)
            a label for a weight given to the nodes to scale their 
            recovery rates
                `gamma_i = G.node[i][recovery_weight]*gamma`
    Returns:
        : trans_rate_fxn, rec_rate_fxn
            Two functions such that 
            - `trans_rate_fxn(u,v)` is the transmission rate from u to v and
            - `rec_rate_fxn(u)` is the recovery rate of u.
'''
    if transmission_weight is None:
        trans_rate_fxn = lambda x, y: tau
    else:
        trans_rate_fxn = lambda x, y: tau*G.edge[x][y][transmission_weight]

    if recovery_weight is None:
        rec_rate_fxn = lambda x : gamma
    else:
        rec_rate_fxn = lambda x : gamma*G.node[x][recovery_weight]


    return trans_rate_fxn, rec_rate_fxn



import EoN.simulation
from EoN.simulation import *
import EoN.analytic
from EoN.analytic import *
import EoN.auxiliary
from EoN.auxiliary import *


'''
These are the systems I want to include based on their numbering in the 
book:

coded (3.7) SIS individual based
(3.30) SIR individual based
NOT coded (3.26) SIS pair based
(3.39) SIR pair based

chapter 4?

(5.13) SIS heterogeneous pairwise
(5.15) SIR heterogeneous pairwise
(5.18) SIS compact pairwise
(5.19) SIR compact pairwise
(5.20) SIS super compact pairwise
(5.22) SIR super compact pairwise
(5.36) SIS effective degree
(5.38) SIR effective degree
(5.43) SIR compact effective degree
(5.44) SIS compact effective degree = SIS compact pairwise

(6.2) Epidemic probability discrete time
(6.3) Epidemic probability continuous time
(6.5) Epidemic probability non-Markovian
(6.6) Epidemic size discrete time
(6.7) Epidemic size continuous time
(6.8) Epidemic size non-Markovian
(6.10) Epidemic size discrete time (large IC)
(6.11) Discrete-time EBCM model
(6.12) Continuous time EBCM model

(8.1) SIS pairwise contact conserving rewiring
(8.5) SIS eff. deg. contact conserving rewiring
(8.7) SIS pairwise random activation/deletion
(8.13) SIS eff. deg. random activation/deletion
(8.15) SIS pairwise link-status dependent act/del
(8.16) SIS link deactivation-activation on fixed networks.
(8.19) EBCM dynamic network

(9.5) SI^{K}R multistage pairwise for homogeneous
(9.27) SIR pairwise, constant infection duration.
(9.35) SIR homogeneous pairwise, general recovery
(9.36) SIR EBCM non-Markovian trans/recovery

add models that take in graph, measure degree distribution and run EBCM
similarly for EBCM with neighbor degrees (see barabasi_SIR.py)

consider explicitly defining toast graph etc.
'''

