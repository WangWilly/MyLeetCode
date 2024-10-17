# Properties of Modular

Modular multiplication shares several properties with regular multiplication, which makes it a useful tool in various mathematical and computational contexts.

- Commutativity: `(a × b) mod n = (b × a) mod n`. The order of multiplication does not affect the result.
- Associative: `((a × b) × c) mod n = (a × (b × c)) mod n`. The way in which numbers are grouped during multiplication does not affect the outcome.
- Distributivity: `(a × (b + c)) mod n = ((a × b) mod n + (a × c) mod n) mod n`. This property links multiplication and addition in modular arithmetic.

Modular Multiplication :
```
(a x b) mod m = ((a mod m) x (b mod m)) mod m 

(a x b x c) mod m = ((a mod m) x (b mod m) x (c mod m)) mod m 
```

## Applications of Modular Multiplication
Modular multiplication has several applications in various domains:

- **Cryptography**: It is crucial in algorithms like RSA, where modular arithmetic ensures that encryption and decryption processes are secure and efficient.
- **Hash Functions**: In computer science, modular multiplication is often used in hashing algorithms, which are used to map data of arbitrary size to fixed-size values.
- **Digital Signal Processing**: Modular arithmetic is used in algorithms that process signals, images, and other forms of digital data.
- **Gaming and Simulations**: Modular arithmetic is used to create cyclic behaviors, such as rotating objects or managing time cycles in simulations and video games.

```cpp
((n % M) + M) % M // To handle negative numbers
```

## Modular Exponentiation

Modular exponentiation is a type of modular operation that involves raising a number to a power and then taking the remainder when divided by a modulus. It is commonly used in cryptography and number theory.

- `(a^b) mod n = ((a mod n)^b) mod n`. This property allows us to reduce the base of the exponentiation to a smaller number before performing the operation.
- `((a mod n) × (b mod n)) mod n = (a × b) mod n`. This property allows us to reduce the operands of multiplication to smaller numbers before performing the operation.

## Modular Inverse

The modular inverse of a number `a` modulo `n` is another number `b` such that `(a × b) mod n = 1`. It is used in various cryptographic algorithms and number theory problems.

- The modular inverse exists if and only if `a` and `n` are coprime (i.e., their greatest common divisor is 1).
- The modular inverse can be calculated using the extended Euclidean algorithm or by using Fermat's little theorem (for prime `n`).

## Modular Division

Modular division is the process of dividing a number by another number modulo a given modulus. It is used in various mathematical and computational contexts.

- Modular division is not a well-defined operation in general, as division is not closed under modular arithmetic.
- However, modular division can be approximated using the modular inverse, i.e., `a ÷ b mod n = (a × b^(-1)) mod n`, where `b^(-1)` is the modular inverse of `b` modulo `n`.

## Reference

- https://www.geeksforgeeks.org/modular-multiplication/
