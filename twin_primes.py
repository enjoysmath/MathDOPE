from sympy import *
import matplotlib.pyplot as plt
from sympy.combinatorics import Permutation, PermutationGroup

class RepSeq:
    def __init__(self, *args):
        self._pattern = tuple(args)
        assert len(self._pattern)

    @property
    def pattern(self):
        return self._pattern
    
    def __getitem__(self, i):
        return self._pattern[i % self.period]
    
    @property
    def period(self):
        return len(self._pattern)
    
    def mul_mod(self, N, b):
        a = self.pattern
        b = b.pattern
        l = lcm(sum(a), sum(b)) % N
        n = len(a); m = len(b)
        i = 0; j = 0
        c = []
        s = a[i] % N; t = b[j] % N
        i = (i + 1) % n
        j = (j + 1) % m
        
        while sum(c) % N != l:     
            if s == t:
                c.append(s)
                s = a[i] % N; t = b[j] % N
                i = (i + 1) % n
                j = (j + 1) % m                
            elif s < t:
                s = (s + a[i]) % N                
                i = (i + 1) % n
            else:                
                t = (t + b[j]) % N
                j = (j + 1) % m
        return RepSeq(*c)        
    
    def __mul__(self, b):
        a = self.pattern
        b = b.pattern
        l = lcm(sum(a), sum(b))
        n = len(a); m = len(b)
        i = 0; j = 0
        c = []
        s = a[i]; t = b[j]
        i = (i + 1) % n
        j = (j + 1) % m
        
        while sum(c) != l:     
            if s == t:
                c.append(s)
                s = a[i]; t = b[j]
                i = (i + 1) % n
                j = (j + 1) % m                
            elif s < t:
                s += a[i]
                i = (i + 1) % n
            else:                
                t += b[j]
                j = (j + 1) % m
        return RepSeq(*c)
    
    def __str__(self):
        return str(self._pattern)
    
    @staticmethod
    def entry0_of_simult_mul(*A):
        N = len(A)
        i = [0 for k in range(N)]
        s = [A[k][0] for k in range(N)]
        min_s = min(s); max_s = max(s)
        
        while min_s != max_s:
            for k in range(N):
                if s[k] < max_s:
                    i[k] += (i[k] + 1) % A[k].period
                    s[k] += A[k][i[k]]
            min_s = min(s)
            max_s = max(s)          
            
        return s[0]

    def symmetric_swaps(self):
        transpos = set()        
        for i in range(len(self.pattern)):
            for j in range(i+1, len(self.pattern)):
                if self.pattern[i] == self.pattern[j]:
                    transpos.add((i+1, j+1))
        return transpos
    
    def symmetry_group(self):
        transpos = (Permutation(*t) for t in self.symmetric_swaps())
        return PermutationGroup(*transpos)
        
    def __add__(self, b):
        a = self
        c = [a[0] + b[0]]
        i = 1
        n = len(c)
        
        while n % 2 == 1 or c[:n//2] != c[n//2:]:
            c.append(a[i] + b[i])
            i += 1 
            n = len(c)
            
        assert c[:n//2] == c[n//2:]
        return RepSeq(*c[:n//2])
    
    def rotate(self, j):
        a = self
        pattern = [None] * a.period
        
        for i in range(a.period):
            pattern[i] = a[i + j]
            
        return RepSeq(*pattern)
    
    #def reduce(self):
        #a = self
        #for i in range(self.period):
            
                    
                
c = RepSeq(1, 1, 2)
d = RepSeq(2, 1, 1)


print(c*c)