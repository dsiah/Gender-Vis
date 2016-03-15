import random, nltk
from nltk.corpus import names

def gender_features(name):
    return {'suffix(1)': name[-1],
            'suffix(2)': name[-2:],
            'suffix(3)': name[-3:]}

def gender_features2(name):
    features = {}
    features["first_letter"] = name[0].lower()
    features["last_letter"] = name[-1].lower()

    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features["count({})".format(letter)] = name.lower().count(letter)
        features["has({})".format(letter)] = (letter in name.lower())
    
    return features

# Label Data
labeled_names = ([(name, 'male')   for name in names.words('male.txt')] + 
                 [(name, 'female') for name in names.words('female.txt')])

# Shuffle
random.shuffle(labeled_names)

# Segment into groups 
train_names   = labeled_names[1500:]    # (1) Train
devtest_names = labeled_names[500:1500] # (2) Debug
test_names    = labeled_names[:500]     # (3) Test

# Groom
train_set   = [(gender_features(n), gender) for (n, gender) in train_names]
devtest_set = [(gender_features(n), gender) for (n, gender) in devtest_names]
test_set    = [(gender_features(n), gender) for (n, gender) in test_names]

# Build Bayes Classifier
classifier  = nltk.NaiveBayesClassifier.train(train_set) 

# Run debug set & log
errors = []
for (name, tag) in devtest_names:
    guess = classifier.classify(gender_features(name))
    if guess != tag:
        errors.append((tag, guess, name))

for (tag, guess, name) in sorted(errors):
    print('correct={:<8} guess={:<8s} name={:<30}'.format(tag, guess, name))

# print(nltk.classify.accuracy(classifier, devtest_set))
print(nltk.classify.accuracy(classifier, test_set))

classifier.show_most_informative_features(10)