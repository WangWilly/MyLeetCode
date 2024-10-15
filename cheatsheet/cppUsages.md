# C++ Usages

- https://en.cppreference.com/w/cpp/container/priority_queue
- https://en.cppreference.com/w/cpp/iterator/next
- https://cplusplus.com/reference/algorithm/next_permutation/

## Binary Search

### Lower Bound

https://en.cppreference.com/w/cpp/algorithm/lower_bound

```cpp
template<class ForwardIt, class T = typename std::iterator_traits<ForwardIt>::value_type,
         class Compare>
ForwardIt lower_bound(ForwardIt first, ForwardIt last, const T& value, Compare comp)
{
    ForwardIt it;
    typename std::iterator_traits<ForwardIt>::difference_type count, step;
    count = std::distance(first, last);
 
    // lo < hi
    while (count > 0)
    {
        it = first;
        step = count / 2; // to lower shifting => (1 + 2) / 2 = 1
        // in some case, we have to use upper shifting => ((1 + 2) + 1) / 2 = 2
        std::advance(it, step);
 
        // [it, advance(it, step)) is a valid range
        // => `comp(*it, value)`: arr[mid] < value
        if (comp(*it, value)) { // <- *it is less than value, so move to the right
            first = ++it;
            count -= step + 1;
            /**
            ===
            lo = mid + 1;
            */
        } else {
            count = step;
            /**
            ===
            hi = mid;
            */
        }
    }
 
    return first;
}
```

example1:

```
intput: [1, 2, 3, 4, 5, 5, 5, 6, 7, 8, 9]
value: 5
output: 4

=> [1, 2, 3, 4, 5, 5, 5, 6, 7, 8, 9]
                ^
```

example2:

```
intput: [4, 5]
value: 5
output: 1

=> [4, 5]
       ^
```

### Upper Bound

https://en.cppreference.com/w/cpp/algorithm/upper_bound

```cpp
template<class ForwardIt, class T = typename std::iterator_traits<ForwardIt>::value_type,
         class Compare>
ForwardIt upper_bound(ForwardIt first, ForwardIt last, const T& value, Compare comp)
{
    ForwardIt it;
    typename std::iterator_traits<ForwardIt>::difference_type count, step;
    count = std::distance(first, last);
 
    // lo < hi
    while (count > 0)
    {
        it = first; 
        step = count / 2; // to lower shifting => (1 + 2) / 2 = 1
        // in some case, we have to use upper shifting => ((1 + 2) + 1) / 2 = 2
        std::advance(it, step);
 
        // [it, advance(it, step)) is a valid range
        // => `!comp(value, *it)`: arr[mid] <= value
        if (!comp(value, *it)) {
            first = ++it;
            count -= step + 1;
            /**
            ===
            lo = mid + 1;
            */
        } else {
            count = step;
            /**
            ===
            hi = mid;
            */
        }
    }
 
    return first;
}
```

example1:

```
intput: [1, 2, 3, 4, 5, 5, 5, 6, 7, 8, 9]
value: 5
output: 7

=> [1, 2, 3, 4, 5, 5, 5, 6, 7, 8, 9]
                         ^
```

example2:

```
intput: [4, 5]
value: 5
output: 2

=> [4, 5]
          ^
```
