import scipy.stats

wins = 1000 #number of wins
losses = 300 # number of losses
draws = 50 # number of draws

p = 0.5  #The probability the bot wins against the opponent

total = wins+losses+draws

result = scipy.stats.binom_test([wins,losses], total, p, alternative='less')
print ("The probability that the bot has a higher probability of winning against the opponent than %s is %s" %(p,result))


