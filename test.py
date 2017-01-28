# -*- coding: utf-8 -*-
import scipy.stats

"""
Parameters:

x : integer or array_like
    the number of successes, or if x has length 2, it is the number of successes and the number of failures.

n : integer
    the number of trials. This is ignored if x gives both the number of successes and failures

p : float, optional
    The hypothesized probability of success. 0 <= p <= 1. The default value is p = 0.5

alternative : {‘two-sided’, ‘greater’, ‘less’}, optional
    Indicates the alternative hypothesis. The default value is ‘two-sided’.

Returns:
p-value : float
    The p-value of the hypothesis test

"""




wins = 550 #number of wins
losses = 50 # number of losses
draws = 110 # number of draws

p = 0.5  #The probability the bot wins against the opponent

total = wins+losses+draws

result = scipy.stats.binom_test([wins,losses], total, p, alternative='less')
print ("The probability that the bot has a higher probability of winning against the opponent than %s is %s" %(p,result))
result = scipy.stats.binom_test([wins,losses], total, p)
print ("The probability that the bot has probability of winning against the opponent of around %s is %s" %(p,result))


