from scipy.stats import binom

a = scipy.stats.binom_test([10,5], p=0.5, alternative='greater')
print(a)
