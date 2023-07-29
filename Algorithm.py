import pandas as pd

# Load data from CSV file
data = pd.read_csv('/content/drive/MyDrive/Products.csv', header=None)

# Convert data into a list of transactions
transactions = []
for row in data.values:
    transactions.append([item for item in row if pd.notna(item)])

# Calculate the support of each item in the dataset
item_support = {}
for transaction in transactions:
    for item in transaction:
        if item not in item_support:
            item_support[item] = 0
        item_support[item] += 1
num_transactions = len(transactions)
for item in item_support:
    item_support[item] = item_support[item] / num_transactions

# Generate frequent itemsets with at least 5% support
frequent_itemsets = {}
min_support = 0.05
for item in item_support:
    if item_support[item] >= min_support:
        frequent_itemsets[frozenset([item])] = item_support[item]
while frequent_itemsets:
    candidate_itemsets = {}
    for itemset1 in frequent_itemsets:
        for itemset2 in frequent_itemsets:
            union = itemset1.union(itemset2)
            if len(union) == len(itemset1) + 1:
                if union not in candidate_itemsets:
                    candidate_itemsets[union] = 0
                for transaction in transactions:
                    if union.issubset(transaction):
                        candidate_itemsets[union] += 1
                candidate_itemsets[union] = candidate_itemsets[union] / num_transactions
    frequent_itemsets = {}
    for itemset in candidate_itemsets:
        if candidate_itemsets[itemset] >= min_support:
            frequent_itemsets[itemset] = candidate_itemsets[itemset]

# Generate association rules with at least 70% confidence
min_confidence = 0.7
association_rules = []
for itemset1 in frequent_itemsets:
    for itemset2 in frequent_itemsets:
        if len(itemset1.intersection(itemset2)) == 0 and len(itemset1.union(itemset2)) == len(itemset1) + 1:
            confidence = frequent_itemsets[itemset1.union(itemset2)] / frequent_itemsets[itemset1]
            if confidence >= min_confidence:
                association_rules.append((itemset1, itemset2, confidence))

# Print the frequent itemsets and association rules
print("Frequent itemsets:")
for itemset in frequent_itemsets:
    print(list(itemset), frequent_itemsets[itemset])
print("Association rules:")
for rule in association_rules:
    print(list(rule[0]), "->", list(rule[1]), "confidence:", rule[2])
