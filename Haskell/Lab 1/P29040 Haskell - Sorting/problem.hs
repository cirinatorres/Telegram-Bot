insert :: [Int] -> Int -> [Int]
insert [] x = [x]
insert (p:sl) x
    | p > x = [x, p] ++ sl
    | otherwise = [p] ++ insert sl x

isort :: [Int] -> [Int]
isort [] = []
isort (x:sl1) = insert (isort sl1) x

remove :: [Int] -> Int -> [Int]
remove [e] x = []
remove (e:sl) x
    | e == x = sl
    | otherwise = [e] ++ remove sl x

myFindMin :: [Int] -> Int
myFindMin [x] = x
myFindMin (x:sl) = min x (myFindMin sl)

ssort :: [Int] -> [Int]
ssort [] = []
ssort l = [myFindMin l] ++ ssort (remove l (myFindMin l))

merge :: [Int] -> [Int] -> [Int]
merge x [] = x
merge [] y = y
merge (x:sx) (y:sy)
    | x < y = [x] ++ merge sx (y:sy)
    | otherwise = [y] ++ merge (x:sx) sy

msort :: [Int] -> [Int]
msort [] = []
msort [e] = [e]
msort l = merge (msort $ take (div (length l) 2) l) (msort $ drop (div (length l) 2) l)

myQSort :: [Int] -> [Int] -> [Int]
myQSort [] l2 = l2
myQSort [e] l2 = e:l2
myQSort  (el1:sl1) l2 = myQSortPart sl1 [] [] l2
    where
        myQSortPart :: [Int] -> [Int] -> [Int] -> [Int] -> [Int]
        myQSortPart [] left right l2 = myQSort left (el1:myQSort right l2)
        myQSortPart (hl1:sl1) left right l2
            | hl1 > el1 = myQSortPart sl1 left (hl1:right) l2
            | otherwise = myQSortPart sl1 (hl1:left) right l2

qsort :: [Int] -> [Int]
qsort l = myQSort l []

myGenQsort :: Ord a => [a] -> [a] -> [a]
myGenQsort [] l2 = l2
myGenQsort [e] l2 = e:l2
myGenQsort (hl1:sl1) l2 = myGenQsortPart sl1 [] [] l2
    where
        myGenQsortPart [] left right l2 = myGenQsort left (hl1:myGenQsort right l2)
        myGenQsortPart (x:sx) left right l2
            | x > hl1 = myGenQsortPart sx left (x:right) l2
            | otherwise = myGenQsortPart sx (x:left) right l2

genQsort :: Ord a => [a] -> [a]
genQsort l = myGenQsort l []
