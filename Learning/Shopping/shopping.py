import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    evidence = []
    labels = []
    with open(filename) as f:
        reader = list(csv.DictReader(f))
        # print(reader[0])
        for row in reader:
            # Administrative, Informational, ProductRelated, Month, OperatingSystems, Browser, Region, TrafficType, VisitorType, and Weekend should all be of type int
            for items in [
                "Administrative",
                "Informational",
                "ProductRelated",
                "OperatingSystems",
                "Browser",
                "Region",
                "TrafficType",
            ]:
                row[items] = int(row[items])

            # Month should be 0 for January, 1 for February, 2 for March, etc. up to 11 for December.
            months = [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "June",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ]
            for month in months:
                if row["Month"] == month:
                    # print("Month change")
                    # print(row["Month"])
                    row["Month"] = months.index(month)
                    # print(row["Month"])

            # VisitorType should be 1 for returning visitors and 0 for non-returning visitors.
            # print(row["VisitorType"])
            row["VisitorType"] = 1 if row["VisitorType"] == "Returning_Visitor" else 0
            # print(row["VisitorType"])

            # Weekend should be 1 if the user visited on a weekend and 0 otherwise.
            row["Weekend"] = 1 if row["Weekend"] == "TRUE" else 0

            for items in [
                "Administrative_Duration",
                "Informational_Duration",
                "ProductRelated_Duration",
                "BounceRates",
                "ExitRates",
                "PageValues",
                "SpecialDay",
            ]:
                row[items] = float(row[items])

            evidence.append(list(row.values())[:-1])
            labels.append(1 if row["Revenue"] == "TRUE" else 0)

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    positive = 0
    negative = 0
    accuratePositive = 0
    accurateNegative = 0
    for i in range(len(labels)):
        if labels[i] == 1:
            positive += 1
            accuratePositive += 1 if predictions[i] == 1 else 0
        else:
            negative += 1
            accurateNegative += 1 if predictions[i] == 0 else 0

    return ((accuratePositive / positive), (accurateNegative / negative))


if __name__ == "__main__":
    main()
