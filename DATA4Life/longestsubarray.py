


def LongestSubarrayWithDistinctEntries(arr: list): 
    # _arr = list(set(arr))
    longest = -1
    temp = []
    for idx_org in range(len(arr)):
        for idx_tmp in range(len(temp)):
            if arr[idx_org] == temp[idx_tmp]:
                # 
                # arr: [1,2,3,3,3,1,2,3,1,2,2,2]
                # tmp[1,2,3] --- element 2 -- len (tmp) -->  longest length -- > greater --> as the longest
                # 
                _tmplongest = len(temp)
                if _tmplongest > longest:
                    longest= _tmplongest
                temp=temp[idx_tmp+1:]
                break
        # 
        temp.append(arr[idx_org])

    if longest==-1:
        return len(temp)

    return longest

if __name__=='__main__':
    # test cases
    arrs = [
        [1,1,1,1,1,1,1,1],
        [1,2,3],
        [1,2,3,3,3,1,2,3,1,2,2,2],
        [9,8,7,5,3,2,1,2,2,2],
        [1, 2, 1, 3, 1, 2, 1, 4],
        ]

    for _case in arrs:
        res = LongestSubarrayWithDistinctEntries(_case)
        print(f"for array {_case}, {res} is the length of the longest subarray")


