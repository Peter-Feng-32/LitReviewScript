import csv
import pandas as pd
from tempfile import NamedTemporaryFile
import shutil

# do some preprocessing and splitting of papers to review.

n = 547  # number of papers to review
csv_filename = "filtered.csv"  # Splitted file of papers to review.
papersToReview = range(1, n)


reviewer_name = input("Enter your name: ")
print('\n')


# Iterate over original file.  Every time we come across a row with a reviewer name matching your name, print the row's data, ask for a decision, and write it back to the original file, and restart the reader

done = False
while not done:
    done = True
    tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

    with open(csv_filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        writer = csv.writer(tempfile, delimiter=",")

        columnNameToIndex = {}
        headers = next(reader)

        for i in range(0, len(headers)):
            columnNameToIndex[headers[i]] = i

        print('\n')
        writer.writerow(headers)

        for row in reader:
            if done:
                if (row[columnNameToIndex["Reviewer"]] == reviewer_name and row[columnNameToIndex["Reviewer Decision"]] == ""):
                    originalrow = row.copy()
                    # Print the row's data
                    print("Title")
                    print(row[columnNameToIndex["Title"]])
                    print('\n')
                    print("Source")
                    print(row[columnNameToIndex["Source title"]])
                    print('\n')
                    print("Abstract")
                    print(row[columnNameToIndex["Abstract"]])
                    print('\n')
                    # Accept this paper?
                    decision = "Not Made"
                    accepted = None
                    while(decision != 'Y' and decision != 'y' and decision != 'N' and decision != 'n'):
                        decision = input("Accept this paper? y/n :\n")
                        if(decision == 'Y' or decision == 'y'):
                            accepted = True
                        elif (decision == 'N' or decision == 'n'):
                            accepted = False

                    reasoning = input("Write reasoning: \n")

                    # Write decision
                    row[columnNameToIndex["Reviewer Decision"]
                        ] = "Accept" if accepted else "Reject"
                    row[columnNameToIndex["Reviewer Comments"]] = reasoning

                    # Confirm
                    confirm = "Not Made"
                    confirmed = None
                    while(confirm != 'Y' and confirm != 'y' and confirm != 'N' and confirm != 'n'):
                        confirm = input("Confirm? y/n: \n")
                        if(confirm == 'Y' or confirm == 'y'):
                            confirmed = True
                        elif (confirm == 'N' or confirm == 'n'):
                            confirmed = False

                    done = False
                    if confirmed:
                        print("CONFIRMED\n")
                        writer.writerow(row)
                    else:
                        print("NOT CONFIRMED\n")
                        writer.writerow(originalrow)
                else:
                    writer.writerow(row)
            else:
                writer.writerow(row)
        print('\n')
        # Now that every row has been iterated, write back to original file and read again.
        print("Writing to disk\n")
        shutil.move(tempfile.name, csv_filename)
