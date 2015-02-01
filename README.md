## LRFUCache

This is a simple Python implementation of a cache based on the 
[LRFU](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.55.1478) 
replacement policy. It has a relatively low overhead compared to linked list 
based cache implementations.

Overhead is reduced by evicting periodically in bulk. As such the cache will
typically contain fewer items than permitted by the upper bound supplied to the 
constructor.
