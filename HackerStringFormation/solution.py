mem = dict()

def findOptimal(target, charMap, tarIdx, wordIdx):
    if (tarIdx == len(target)):
        return 1
    if ((tarIdx, wordIdx) in mem):
        return mem[(tarIdx, wordIdx)]

    charMapOrdered = sorted([[it[0], it[1]] for it in charMap[target[tarIdx]].items()])

    res = 0
    for oPair in charMapOrdered:
        if (oPair[0] <= wordIdx):
            continue
        res += findOptimal(target, charMap, tarIdx + 1, oPair[0]) * oPair[1]
    
    res %= 1000000007
    mem[(tarIdx, wordIdx)] = res
    return res


def numWays(words, target):
    # Write your code here
    charMap = dict()

    for w in words:
        for i in range(len(w)):
            if (w[i] not in charMap):
                charMap[w[i]] = dict()
            if (i not in charMap[w[i]]):
                charMap[w[i]][i] = 0
            charMap[w[i]][i] += 1

    return findOptimal(target, charMap, 0, -1)

################################################################################

def main():
    words = ["acca","bbbb","caca"]
    target = "aba"
    print(numWays(words, target))

if __name__ == "__main__":
    main()
