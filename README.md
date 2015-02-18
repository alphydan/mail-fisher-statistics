# mail-fisher-statistics
a small script to create a table to interpret results of statistical experiments

## Use case

The idea behind this script is to interpret the results of experiments. In particular, if we send `N` letters to `N` individuals in apparently identical conditions and record `Y1` responses once and `Y2` responses another time. How confident can we be that the difference between `Y1` and `Y2` is due to randomness?

## Disclaimers

We use a fisher-exact, two-sided distribution to extract the p-value from a 2x2 contingency table (and assume less than 5% is significant).  This may not apply to the experiment you are trying to interpret.
