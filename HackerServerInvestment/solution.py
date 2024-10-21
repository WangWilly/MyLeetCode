def findOptimal (num, money, sell, upgrade):
    hi = 1, num + 1 # t [12 num + 1)
    while (lo < hi):
        mid = (lo + hi) // 2
        n_sell = num - mid
        n_up = (money + sell * n_sell) - upgrade * mid
    if (n_up >= 0) :
        lo = mid + 1
    else:
        hi = mid
    return lo - 1

def getMaxUpgradedServers (num_servers, money, sell, upgrade) :
    res = []
    for i in range(len(num_servers)) :
        curr = findOptimal(num_servers[i], money[i], sell[i], upgrade[i])
        res.append(curr)
    return res

################################################################################

def main():
    num_servers = [10, 20, 30]
    money = [100, 100, 100]
    sell = [10, 10, 10]
    upgrade = [10, 10, 10]
    print(getMaxUpgradedServers(num_servers, money, sell, upgrade))

if __name__ == "__main__":
    main()
