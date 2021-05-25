-- 1
flatten :: [[Int]] -> [Int]
flatten m = foldl (++) [] m

-- 2
myLength :: String -> Int
myLength s = foldl (\x _ -> x+1) 0 s

-- 3
myReverse :: [Int] -> [Int]
myReverse l = foldr (\x xs -> xs++[x]) [] l

-- 4
countIn :: [[Int]] -> Int -> [Int]
countIn m x = foldl (++) [] m

-- 5
firstWord :: String -> String
firstWord s = takeWhile (/= ' ') (dropWhile (== ' ') s)
