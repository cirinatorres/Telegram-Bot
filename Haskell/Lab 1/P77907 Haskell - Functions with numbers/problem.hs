absValue :: Int -> Int
absValue x
    | x < 0 = -x
    | otherwise = x

power :: Int -> Int -> Int
power x p
    | p == 0 = 1
    | p == 1 = x
    | otherwise = x * power x (p-1)

isPrimeAux :: Int -> Int -> Bool
isPrimeAux n it
    | n == it = True
    | mod n it == 0 = False
    | otherwise = isPrimeAux n (it+1)

isPrime :: Int -> Bool
isPrime n
    | n < 2 = False
    | otherwise = isPrimeAux n 2

slowFib :: Int -> Int
slowFib n
    | n < 2 = n
    | otherwise = slowFib (n-1) + slowFib (n-2)

quickFibIter :: Int -> Int -> Int -> Int -> Int
quickFibIter n it fm1 fm2
    | n == it = (fm1 + fm2)
    | otherwise = quickFibIter n (it+1) (fm1+fm2) fm1

quickFib :: Int -> Int
quickFib n
    | n < 2 = n
    | otherwise = quickFibIter n 2 1 0
