import socket
import random
import math

class EncryptedObject():

     def to_binary(self, n):
         if n == 0:
             return 0
         else:
             if n % 2:
                 return (self.to_binary((n-1)/2)) * 10 + 1
             else:
                 return (self.to_binary((n) / 2)) * 10
     def efficient_power(self, a, n, p):
         print "ITERATE"
         if n == 1:
             return a % p
         else:

             return (self.efficient_power(a, math.floor(n/2.0), p)**2 * a if n % 2 else 1) % p

     def is_prime(self, p):
         if p == 2 or p == 3:
             return True
         for i in range(1,5):
             a = random.randint(2, p-2)
             print "Checking %s..." % a
             if self.efficient_power(a, p-1, p) != 1:
                 return False
         return True

     def generate_prime(self, max):
         list = range(2, max)
         for n in list:
             print "Testing " + str(n)
             if self.is_prime(n):
                 # remove all multiples
                 print n
                 print list
                 for i in range(n+n,max+n, n):
                     if i in list: list.remove(i)
         return list

     def __init__(self):
         pass
         #self._privateKey = self.generate_prime()
         #self._publicKey = self.generate_prime()


class EncryptedClient():
    def __init__(self):
        pass

class EncryptedServer():

    _key = {"public":"", "private":""}
    _users = {}
    def __init__(self):
        pass

def main():
    test = EncryptedObject()
    print test.is_prime(961748941)
    print test.generate_prime(2**20)


if __name__ == "__main__":
    main()