# Group_Partitioning
Project for course CS6002 - Selected Areas of Mechanism Design

### Hypotheses
1. For each allocation with max-envy of >= 3, there exists at least one node swap that can bring the max-envy down by at least 1.
    - Negated for n = 11, m = 20
2. For each allocation with max-envy of >= 3, there exists at least one node swap that can bring the sum of all envies down by at least 1.
    - Negated for n = 11, m = 20
3. For every graph with even number of nodes, there exists at least one EF-2 allocation where envy = 2 is present only for one colour.
    - Verified for n = 14, 16, 18 (all edge counts, 1000 random graphs per edge count)