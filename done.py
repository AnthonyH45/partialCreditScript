"""
  IMPORTANT
    This program is poorly written as it assumes A LOT about the shape of the given CSV
    This is a PoC for adding partial credit (with a subtraction twist!) to gradescope CSVs
    There really should be more error checking and making sure stuff actually succeeds (like using [i] everywhere)
    This suffices for now
"""
import re


def main():
    # use a context manager to open/close the file properly
    with open("f.csv") as f:
        # This list comprehension reads each line of the file
        # For each line in the file, we are going to split each line on each `,` that IS NOT found within double quotes AFTER stripping whitespace
        #       This is done using regex: https://stackoverflow.com/questions/43067373/split-by-comma-and-how-to-exclude-comma-from-quotes-in-split
        #       This is because we need to preserve `Select All` questions and answers
        # Then we are going to grab all lines that ARE NOT length 1 since those are the newlines that got preserved as `['']` and we dont care for those
        a = [
            i
            for i in [
                re.compile(r",(?=(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)").split(
                    i.strip()
                )
                for i in f.readlines()
            ][1:]
            if len(i) != 1
        ]
        # this makes a tuple of (netID,[(score, weight, student choice, correct answer)])
        # the iter()*2 is needed for the next step of zipping them together
        b = [(i[2], [iter(i[10:])] * 2) for i in a]
        c = [(j[0], [i for i in zip(*j[1], *j[1])]) for j in b]

        # While this could be another list comprehensions (yea!) it makes it more readable to use a for loop
        # I used comprehensions earlier since I do not think we should waste lines of code on text parsing
        # c = [ (netID1,[()]), ...   ]
        for i in c:
            tot_sum = 0
            # This loop just looks at the tuple of answers
            for j in i[1]:
                # sort the student choice and clean it
                j_2 = sorted(j[2].replace('"', "").split(", "))
                # sort the correct ans and clean it
                j_3 = sorted(j[3].replace('"', "").split(", "))

                count = 0
                # if the correct answer only has one selection
                if len(j_3) == 1:
                    # check that the student selection is the right one
                    if j_2[0] in j_3:
                        # add the weight of the question to the total
                        count = count + int(j[1])
                    # increment total sum for this student by the count
                    tot_sum = tot_sum + count
                # if the correct answer has multiple correct selections
                else:
                    # make both lists into sets
                    j2s = set(j_2)
                    j3s = set(j_3)
                    # sort their union
                    ts = sorted(j2s | j3s)
                    # align each set as a list with an 'X' where they differ
                    # https://stackoverflow.com/questions/18303792/align-two-lists-by-adding-special-values-for-missing-entries
                    aligned_j2 = [x if x in j2s else "X" for x in ts]
                    aligned_j3 = [x if x in j3s else "X" for x in ts]
                    # combine each zip into a single
                    ziped_aligned = [z for z in zip(aligned_j2, aligned_j3)]
                    mc = 0
                    # for each tuple, we look at the first and second param to see if they match
                    for (x, y) in ziped_aligned:
                        # if Y is 'x' that means the student put something that is not the answer
                        if y == "X":
                            # so we SUBTRACT 1 for the student putting the wrong answer on multiple selections
                            mc = mc - 1
                        # if X is the same, then we add 1 point
                        elif x == y:
                            mc = mc + 1
                        # else, do nothing as we add 0
                    # since we don't want to add negatives, we will keep mc to add if it is positive, otherwise, we will make it 0
                    mc = mc if mc >= 0 else 0
                    # add out sum
                    # while we could just use `count` again, lets just use a new var to make it more apparant that there is a diff
                    tot_sum = tot_sum + mc
            # print out netid, score
            print(i[0], tot_sum)


if __name__ == "__main__":
    main()
