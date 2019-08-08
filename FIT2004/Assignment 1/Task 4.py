def searchPunct(key,lst):
    '''
    Method traverses through punct array to find if the key matches any items in the toRemove array, if there is a match then the key is
    replaced with an empty space, so as to say it is removed.
    :param key: word from final_string
    :param lst: punct list is the parameter for this method
    :return key is returned either without being altered or as an empty space
    :exception if the key is not a string then raise a ValueError message

    pre-condition:
        toRemove list must exist for method to be useful
        filtered string must exist from which the key arg is obtained
    post-condition:
        the key is found in the toRemove list and replaced with an empty space or it is left alone and returned
    time complexity:
        best case: O(len(punct)) = O(1)
        average case: O(len(punct)) = O(1)
        worst case: O(len(punct)) = O(1)
    space complexity:
        O(2) = O(1), variables remain the same, no new variable are stored after each each iteration
    '''
    for item in lst:
        if key == item:
            key = ''
            return key
    return key


def preprocess(file):
    '''
    Method reads from text file and concatenates each word into a final_string. The final_string is then filtered where punctuation is
    removed from the string. Finally words from filter_string are individually appended to a list and auxiliary verbs are removed. The final
    preprocessed list is returned.
    :param file: text file that is being read into (Writing.txt)
    :return preprocessed list, words that are not auxiliary verbs and without punctuation.
    :exception N/A

    pre-condition:
        Text file must exist, and all characters in text file must be lowercase
    post-condition:
        auxiliary verbs and punctuation is removed from string and processed into a list which is returned
    time complexity:
        worst case: O(nm)
    space complexity:
        O(nm)
    '''
    wordList = []
    toRemove = ['am', 'is', 'are', 'was', 'were', 'has', 'have', 'had', 'been', 'will', 'shall', 'may', 'can', 'would','should', 'might', 'could','a','an','the']
    punct = ['.', ',', '?', '!', ':', ';', '"']
    # Read lines into a list
    text_string = ''
    with open(file, 'r') as f:
        for line in f:
            if line[-1] != '\n':
                line += '\n'
            text_string += line

        final_string = ''
        for c in text_string:
            if c == '\n':
                c = ' '
            final_string += c

        if len(final_string) == 0:
            return False

        filter_string = ''
        for index in range(len(final_string)):
            filter_string += searchPunct(final_string[index], punct)

        counter1 = 0
        counter2 = 0
        words = []
        if filter_string[-1] != ' ':
            filter_string += ' '
        for char in range(len(filter_string)):
            counter2 = char
            if filter_string[char] == ' ':
                words.append(filter_string[counter1:counter2])
                counter1 = counter2 + 1

        n = 0
        processed = []
        while n < len(words):
            for aux in toRemove:
                if words[n] == aux:
                    n += 1
            processed.append(words[n])
            n += 1

        return processed

def wordSort(array):
    '''
    The following method takes preprocessed words and sorts them in alphabetical order using the radix sort algorithm
    :param array: the array returned from preprocess method is used as the input and items within are sorted in alphabetical order
    :return sorted array
    :exception if there is an integer present in array then raise ValueError

    pre-condition:
        array of words must be provided
    post-condition:
        array is sorted in alphabetical order
    time complexity:
        worst case: O(nm)
    space complexity:
        O(nm)
    '''
    maxLen = -1
    for string in array:
        if len(string) >= maxLen:
            maxLen = len(string)
    a = ord('a') - 1  # First character code
    z = ord('z') - 1  # Last character code
    n = z - a + 2
    count = [0]*n
    for pos in reversed(range(0,maxLen)): # fixed size so loop is constant
        for string in array:
            idx = 0
            if pos < len(string):
                idx = ord(string[pos]) - a
                if count[idx] != 0:
                    if type(count[idx]) == type(count):
                        count[idx].append(string)
                    else:
                        dup = []
                        dup.append(count[idx])
                        dup.append(string)
                        count[idx] = dup
                else:
                    count[idx] = string
            elif count[idx] != 0:
                if type(count[idx]) == type(count):
                    count[idx].append(string)
                else:
                    dup = []
                    dup.append(count[idx])
                    dup.append(string)
                    count[idx] = dup
            else:
                count[idx] = string
        del array[:]
        for item in range(len(count)):# Reassemble array in new order
            if count[item] != 0:
                if type(count[item]) == type(count):
                    array.extend(count[item])
                else:
                    array.append(count[item])
        count = [0]*n

    return array

def wordCount(array,no_dup):
    '''
    Method counts the number of occurences of each item in array
    :param array: list of sorted words
    :param no_dup: same list of words without duplicates
    :return list of word and count pairs [word, count] and total number of words in array at index 0 of list
    :exception if array or no_dup is empty terminate process

    pre-condition:
        array and no_dup lists must exist in order for the method to be useful
    post-condition:
        each word present in the array is appended to its own individual bucket as a [word,count] pair
    time complexity:
        O(nm)
    space complexity:
        O(nm)
    '''
    l = len(no_dup)
    global counter
    counter = [0] * l
    global bucket
    bucket = [[] for i in range(0, l)]
    for word in range(0,len(no_dup)):
        bucket[word].append(no_dup[word])
    bucket.insert(0,len(array)) # complexity of O(n)
    n = 0
    for w in range(len(array)):
        if w == 0:
            counter[n] += 1
        elif array[w] != array[w-1]:
            n+=1
            counter[n] += 1
        else:
            counter[n] += 1

    for freq in range(0,len(counter)):
        bucket[freq+1].append(counter[freq])

    return bucket

def removeDuplicates(arr, n):
    '''
    Function removes duplicates from array returned by wordSort() function. This is done by maintaining a separate index for the same array
    and returns a new size of the array.
    :param arr: array returned from radix sort
    :param n:size of arr
    :return:new size of arr

    pre-condition:
        sorted array must be provided
    post-condition:
        new size of arr is returned with no duplicates present in the array
    time complexity:
        O(n)
    space complexity:
        O(n)
    '''
    if n == 0 or n == 1:
        return n
    j = 0
    for i in range(0, n - 1):
        if arr[i] != arr[i + 1]:
            arr[j] = arr[i]
            j += 1
    arr[j] = arr[n - 1]
    j += 1
    return j

def binarySearch(lst, target):
    lo = 0
    hi = len(lst)-1
    while lo<=hi:
        mid = (lo+hi)//2
        if lst[mid]==target:
            return mid
        else:
            if target < lst[mid]:
                hi = mid - 1
            else:
                lo = mid+1
    print('NOT FOUND')


def leftMaxHeapify(A, left, initial, heapsize):
    if left < heapsize and A[left][1] == A[initial][1]:
        if binarySearch(bucket,A[left]) > binarySearch(bucket,A[initial]):
            maximum = left
        else:
            maximum = initial
    elif left < heapsize and A[left][1] < A[initial][1]:
        maximum = left
    else:
        maximum = initial
    return maximum


def maxHeapify(array, i, heapsize):
    '''
    Start from the last parent node and compare the lest and right child nodes, and swap the parent node with the largest child node
    provided that the value of the parent node is smaller than that of the child nodes'.
    :param array: heap of size k
    :param i: parent node index
    :param heapsize: size of heap (size = k)
    :return: N/A

    pre-condition:
        heap must be present
    post-condition:
        largest element sifts to the root node
    time-complexity:
        worst case: O(log(k))
        avg case: O(1)
    space complexty:
        O(logn)
    '''
    l = 2 * i + 1
    r = 2 * i + 2
    largest = leftMaxHeapify(array, l, i, heapsize)
    if r < heapsize and array[r][1] == array[largest][1]:
        if binarySearch(bucket,array[r])>binarySearch(bucket,array[largest]):
            largest = r
    elif r < heapsize and array[r][1] < array[largest][1]:
        largest = r
    if largest != i:
        temp = array[i]
        array[i] = array[largest]
        array[largest] = temp
        maxHeapify(array, largest, heapsize)


def buildmaxHeap(array,k):
    heap_size = k
    for i in reversed(range(0, k//2)):
        maxHeapify(array, i, heap_size)


def Heapsort(array,k):
    '''
    Given an array of size k elements, the following heap sort fucntion will sort the array into a max-heap
    :param array: array of sie k elements
    :param k: size of the array
    :return: max-heap of size k

    pre-condition:
        array with k elements present
    post-condition:
        max-heap of size k elements
    time complexity:
        O(log(k))
    space complexity:
        O(n)
    '''
    kHeap = array[1:k+1]
    buildmaxHeap(kHeap,k)
    n = len(kHeap)
    for i in reversed(range(0, n)):
        temp = kHeap[0]
        kHeap[0] = kHeap[i]
        kHeap[i] = temp
        n -= 1
        maxHeapify(kHeap, 0, n)
    return kHeap

def heapSortK(array):
    '''
    Heapsort for finding kTopElements. Whenever an element is inserted into heap of size k, this heapsort function is called to rearrange it
    back to a max heap.
    :param array: array of size k
    :return: max-heap of the array

    pre-condition:
        array with k elements present
    post-condition:
        max-heap of size k elements
    time complexity:
        O(log(k))
    space complexity:
        O(n)
    '''
    n = len(array)
    buildmaxHeap(array, n)
    for i in reversed(range(0, n)):
        temp = array[0]
        array[0] = array[i]
        array[i] = temp
        n -= 1
        maxHeapify(array, 0, n)
    return array


def kTopWords(array,heap,k):
    '''

    :param array: wordSort array without duplicates
    :param heap: heap of size k
    :param k: size specified by user
    :return: heap of size k

    pre-condition:
        sorted array, and size of heap speicified. As well as a heap with k elements
    post-condition:
        max-heap with k number of elements
    time complexity:
        O(nlog(k))
    space complexity:
        O(nm)
    '''
    n = len(array)
    for i in range(k+1,n):
        if array[i][1] == heap[-1][1]:
            if i < binarySearch(bucket,heap[-1]):
                heap.pop()
                heap.insert(0,array[i])
                heapSortK(heap)
        elif array[i][1] > heap[-1][1]:
            heap.pop()
            heap.insert(0,array[i])
            heapSortK(heap)

    return heap



######### TEST CASES #########

file_name = input("Give a file name: ")

def read_file():
    try:
        data = preprocess(file_name)
        print("Words are preprocessed.....")
        print_data = input("Do I need to display the remaining words (Y/N): ")
        if print_data == "Y" or print_data == "y":
            if data == False:
                print("Writing.txt is empty")
                exit()
            else:
                for word in data:
                    print(word)
            return data
        elif print_data == "N" or print_data == "n":
            exit()
        else:
            my_error = ValueError("Given input was not valid")
            raise my_error
    except IOError:
        print("Text file does not exist")

def radix_sort():
    try:
        radix = wordSort(read_file())
        global nodup
        nodup = []
        radix_copy = radix[:]
        n = removeDuplicates(radix_copy, len(radix_copy))
        for i in range(0, n):
            nodup.append(radix_copy[i])
        print("The remaining words are sorted in alphabetical order")
        print_sort = input("Do you want to see? (Y/N): ")
        if print_sort == "Y" or print_sort == "y":
            for word in radix:
                print(word)
            return radix
        elif print_sort == "N" or print_sort == "n":
            exit()
        else:
            my_error = ValueError("Given input was not valid")
            raise my_error
    except TypeError:
        print("input given is not a list type")

def word_count():
    try:
        count = wordCount(radix_sort(),nodup)
        print("The total number of words in the writing: {}".format(count[0]))
        print("The frequencies of each word:")
        for i in range(1,len(count)):
            print(count[i][0] + ": " + str(count[i][1]))
        return count
    except TypeError:
        print("input given for wordCount method is not a list type")

count_array = word_count()

def k_top_words():
    try:
        k = int(input("How many top-most frequent words do I display? "))
        k_sort = Heapsort(count_array, k)
        print("{} top most words appear in the writing are:".format(k))
        top_words = kTopWords(count_array,k_sort,k)
        for i in range(len(top_words)):
            print(top_words[i][0] + ": " +  str(top_words[i][1]))
    except TypeError:
        print("input given for kTopWords method is not a list type")

k_top_words()