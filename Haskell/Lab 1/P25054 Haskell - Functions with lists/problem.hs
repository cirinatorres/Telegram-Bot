myLength :: [Int] -> Int
myLength [] = 0
myLength (x:sl) = 1 + myLength sl

myMaximum :: [Int] -> Int
myMaximum [x] = x
myMaximum (x:sl) = max x (myMaximum sl)

myListSum :: [Int] -> Int
myListSum [x] = x
myListSum (x:sl) = x + myListSum sl

average :: [Int] -> Float
average [x] = fromIntegral x
average l = fromIntegral (myListSum l) / fromIntegral (myLength l)

reverseList :: [Int] -> [Int]
reverseList [p] = [p]
reverseList (p:sl) = reverseList sl ++ [p]

buildPalindrome :: [Int] -> [Int]
buildPalindrome [] = []
buildPalindrome l = reverseList l ++ l

removeElementFromList :: [Int] -> Int -> [Int]
removeElementFromList [] _ = []
removeElementFromList [px] y
    | px == y = []
    | otherwise = [px]
removeElementFromList (px:sx) y
    | px == y = removeElementFromList sx y
    | otherwise = [px] ++ removeElementFromList sx y

remove :: [Int] -> [Int] -> [Int]
remove [] _ = []
remove x [] = x
remove x (py:sy) = remove (removeElementFromList x py) sy

flatten :: [[Int]] -> [Int]
flatten [] = []
flatten [m] = m
flatten (m:sm) = m ++ flatten sm

oddsNevens :: [Int] -> ([Int],[Int])
oddsNevens [] = ([],[])
oddsNevens (x:sl)
    | even x = ([] ++ fst (oddsNevens sl), [x] ++ snd (oddsNevens sl))
    | otherwise = ([x] ++ fst (oddsNevens sl), [] ++ snd (oddsNevens sl))

isPrime :: Int -> [Int] -> [Int]
isPrime n [] = [n]
isPrime n (x:sx)
    | mod n x == 0 = [x] ++ sx
    | otherwise = [x] ++ isPrime n sx

generateDivisors :: Int -> Int -> [Int] -> [Int]
generateDivisors it n l
    | it == n + 1 = l
    | mod n it == 0 = generateDivisors (it+1) n (isPrime it l)
    | otherwise = generateDivisors (it+1) n l

primeDivisors :: Int -> [Int]
primeDivisors n = generateDivisors 2 n []

