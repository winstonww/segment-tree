import sys


def roundup(num, base):
    res = 1
    while res < num:
        res *= base
    return res


def lchild(pos):
    return 2 * pos


def rchild(pos):
    return 2 * pos + 1


class SegmentTree(object):
    def __init__(self, callback, sentinel):
        self.arr = None
        self.callback = callback
        self.sentinel = sentinel
        self.segmentTree = None

    def build(self, arr):
        self.arr = arr
        self.segmentTree = [self.sentinel for _ in range(roundup(len(arr), 2) * 2)]

        def _build(lo, hi, pos):
            if lo == hi:
                self.segmentTree[pos] = arr[lo]
                return
            mid = (lo + hi) // 2
            _build(lo, mid, lchild(pos))
            _build(mid+1, hi, rchild(pos))

            self.segmentTree[pos] = self.callback(
                self.segmentTree[lchild(pos)],
                self.segmentTree[rchild(pos)])

        _build(0, len(arr)-1, 1)

    def query(self, qlo, qhi):
        
        def _query(qlo, qhi, lo, hi, pos):
            if (qlo <= lo and qhi >= hi):
                return self.segmentTree[pos]

            if (qlo > hi or qhi < lo):
                return self.sentinel

            mid = (lo + hi) // 2
            left = _query(qlo, qhi, lo, mid, lchild(pos))
            right = _query(qlo, qhi, mid+1, hi, rchild(pos))
            return self.callback(left, right)

        return _query(qlo, qhi, 0, len(self.arr)-1, 1)


arr = [1,2,5,1,6,-1,-5,1,6,7,8,10,12]
minSegmentTree = SegmentTree(min, sys.maxsize)
maxSegmentTree = SegmentTree(max, -sys.maxsize)
minSegmentTree.build(arr)
maxSegmentTree.build(arr)
from random import randint
for _ in range(50):
    i = randint(0, len(arr)-1)
    j = randint(i, len(arr)-1)
    assert(minSegmentTree.query(i, j) == min(arr[i:j+1]))
    assert(maxSegmentTree.query(i, j) == max(arr[i:j+1]))
