-- 1
ones :: [Integer]
ones = [1] ++ ones

-- 2
nats :: [Integer]
nats = iterate (+1) 0

-- 3
ints :: [Integer]
ints = 0 : (concatMap (\x -> [x, -x]) (drop 1 nats))

-- 4
triangulars :: [Integer]
triangulars = scanl (+) 0 (drop 1 nats)

-- 5
factorials :: [Integer]
factorials = scanl (*) 1 (drop 1 nats)

-- 6
fibs :: [Integer]
fibs = map fst (iterate (\(a,b) -> (b,a+b)) (0,1))

-- 7
primes :: [Integer]
primes = recursivePrimes (drop 2 nats)
    where
        recursivePrimes (e:sl) = e : (recursivePrimes (filter (\n -> mod n e /= 0) sl))

-- 8
hammings :: [Integer]
hammings = 1 : map (2*) hammings `merge` map (3*) hammings `merge` map (5*) hammings
    where
        merge (x:xs) (y:ys)
            | x < y = x : xs `merge` (y:ys)
            | x > y = y : (x:xs) `merge` ys
            | otherwise = x : xs `merge` ys

-- 9
-- lookNsay :: [Integer]

-- 10
nextRow :: [Integer] -> [Integer]
nextRow row = zipWith (+) ([0] ++ row) (row ++ [0])

tartaglia :: [[Integer]]
tartaglia = iterate nextRow [1]
