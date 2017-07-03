import csv

from sklearn import svm

X = []
y = []

feature_set_len = 3455
test_set_length = 1115
training_set_length = feature_set_len - test_set_length

with open('tweet_features_nltk.csv', newline='') as csvfile:
    tweetfeaturereader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for feature_list in tweetfeaturereader:
        X.append([float(x) for x in feature_list[:-2]])
        y.append(int(feature_list[-1]))

clf = svm.SVC()

clf.fit(X[:training_set_length], y[:training_set_length])

predictions = clf.predict(X[training_set_length:])

spam_matched = 0
total_spam_count = 0
nonspam_matched = 0
others_count = 0
matched_count = 0
for x in range(test_set_length):
    if y[training_set_length+x] == 1:
        total_spam_count += 1
    else:
        others_count += 1
    if y[training_set_length+x] == predictions[x]:
        matched_count += 1
        if predictions[x] == 1:
            spam_matched += 1
        else:
            nonspam_matched += 1

print("Match count: ", matched_count)
print("Accuracy: ", matched_count/test_set_length)
print("Spam found: ", spam_matched)
print("Total spam count: ", total_spam_count)
print("Nonspam found: ", nonspam_matched)
print("Others count: ", others_count)
