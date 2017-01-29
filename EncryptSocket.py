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
         if n == 1:
             return a % p
         else:
             return (self.efficient_power(a, math.floor(n/2.0), p) * self.efficient_power(a, math.ceil(n/2.0), p)) % p

     def is_prime(self, p):
         for i in range(1,5):
             a = random.randint(2, p-2)
             print "Checking %s..." % a
             if self.efficient_power(a, p-1, p) != 1:
                 return False
         return True

     def generate_prime(self):
         pass
     def __init__(self):
         self._privateKey = self.generate_prime()
         self._publicKey = self.generate_prime()


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
    for i in range(3,10):
        print test.to_binary(i)
    print test.efficient_power(12, 3, 7)
    print (12**3) % 7


if __name__ == "__main__":
    main()