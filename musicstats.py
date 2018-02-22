import sys
from scipy import stats
users = {}
women = set()
men = set()
with open('cust.csv', 'r') as userfile:
    for line in userfile:
        data = line.split(',')
        try:
            user = int(data[0])
            gender = int(data[2])
        except ValueError:         
            pass
        else:
            users[user] = data[1]
            if gender == 0:
                men.add(user)
            else:
                women.add(user)
lisSets = {}
lisCounts = {}
with open('tracks.csv', 'r') as trackfile:
    for line in trackfile:
        data = line.split(',')
        try:
            user = int(data[1])
            track = int(data[2])
            mobile = int(data[4])
        except ValueError:
            pass
        else:
            if user not in lisSets:
                lisSets[user] = set()
                lisCounts[user] = [0, [0, 0]]
            lisSets[user].add(track)
            lisCounts[user][0] += 1
            lisCounts[user][1][mobile] += 1
most = max(lisSets.itervalues(), key=lambda x: len(x))
print len(most)
womenCounts = []
menCounts = []
mobileCounts = []
nonmobileCounts = []
for user, lis in lisSets.iteritems():
    if len(lis) == len(most):
        print users[user]
for user, counts in lisCounts.iteritems():
    if user in men:
        menCounts.append(counts[0])
    else:
        womenCounts.append(counts[0])
    nonmobileCounts.append(counts[1][0])
    mobileCounts.append(counts[1][1])
print stats.ttest_ind(womenCounts, menCounts, equal_var=False)
print stats.ttest_rel(mobileCounts, nonmobileCounts)
print men
print women
