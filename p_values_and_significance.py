#!/usr/bin/env python
from scipy import stats
import csv

'''
The idea behind this script is to interpret the results of
experiments. In particular, if we send X letters to X individuals in
apparently identical conditions and record Y1 responses once and Y2
responses another time. How confident can we be that Y1-Y2 is due to
randomness or to some underlying difference.
'''

def min_max_significant(i, average_response_percentage = 1):
    '''
    finds the value which starts to be significant in a 2x2 contingency table
    for example, send 1,000 letters and usually get 10.
    if you get 5 letters, is it random or does it indicate some ulterior cause?
    we take p < 5% as the significance value
    '''

    one_percent = int(average_response_percentage/100.0*i)
    for away_from_average in range(1,one_percent):

        contingency_table = [[one_percent, i-one_percent],\
                             [one_percent - away_from_average, i+away_from_average-one_percent]]
        # note that the sum of each row of the contingency table should add up to "i"
        oddsratio, pvalue = stats.fisher_exact(contingency_table, alternative='two-sided')
        # we use two-sided because we could get more or less responses
        if pvalue <= 0.05:
            min_found = one_percent-away_from_average+1
            min_pvalue = pvalue
            break
            # the probability to observe less than min_found
            # by chance is less than 5% (in fact it's less than pvalue%)
        elif pvalue >0.05:
            # just in case we get all the way down to zero without significance
            min_found = None
            min_pvalue = None

    for max_outcomes in range(one_percent,i-one_percent):
        # note that the sum of each row of the contingency table should add up to "i"
        contingency_table = [[one_percent, i-one_percent],\
                             [max_outcomes, i-max_outcomes]]
        oddsratio, pvalue = stats.fisher_exact(contingency_table, alternative='two-sided')
        # we use two-sided because we could get more or less responses
        if pvalue < 0.05:
            max_found = max_outcomes-1
            max_pvalue = pvalue
            break
            # the probability to observe more than max_found responses
            # by chance is less than 5% (it's less than max_pvalue)

    return (min_found, min_pvalue),(max_found,max_pvalue)


#####################################
#         Write results to CSV      #
#####################################


letter_number = range(1000,35000,500)
average_response_percentage = 1
with open('significance_table.csv', 'wb') as csvfile:
    sigwriter = csv.writer(csvfile)
    for i in letter_number:
        data = min_max_significant(i)
        data_out = [i,int(average_response_percentage/100.0*i),\
                    data[0][0],data[0][1],data[1][0],data[1][1]]
        print data_out
        sigwriter.writerow(data_out)



#######################
# Quick Bibliography  #
#######################

# http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.fisher_exact.html
# http://graphpad.com/quickcalcs/contingency1/
# https://en.wikipedia.org/wiki/Fisher%27s_exact_test
