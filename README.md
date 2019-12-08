# simple-DES
An attempt at a simple DES algorithm Python implementation

# The DES (Data Encyption Standard) algorithm in detail
## A. Get the 16 subkeys from the primary key
In order to encrypt the original text we need 16 smaller 48-bit subkeys which are generated from a primary 64-bit key.
Here is how to do this:
1. Convert the 64-bit primary key to binary (if you haven't already)
2. Discard every 8th bit of the key.
3. Cut the new 56-bit key into two parts, left and right, each one being of 28 bits length.
4. To get each one of the subkeys from the two parts:
- Perform a left shift on each of the two key parts. A left shift is a process where the Most Significant Bits (MSB) become the Least Significant (LSB).
An example:
10|110010 -> 110010|10
[For rounds subkeys 1, 2, 9 and 16, perform a single-bit left shift.
For other rounds, perform a double-bit left shift.](https://media.geeksforgeeks.org/wp-content/uploads/666-2.png)
- Perform a compression permutation* on the concatenated two key parts.
[This is how to map the bits for the compression permutation](https://media.geeksforgeeks.org/wp-content/uploads/777.png)
5. After all 16 rounds of step 4 we will get all the subkeys

## B. Encryption
1. Perform the IP ([Initial Permutation*](https://media.geeksforgeeks.org/wp-content/uploads/444-3.png)) on the 64-bit input text
2. Split the 64-bit permutated text into two 32-bit parts: **LPT** and **RPT**
3. Process the two parts 16 times using each one of the 16 subkeys
4. Perform the final permutation* (Reverse Initial Permutation - IP<sup>-1</sup>)
5. We now have the 64-bit encrypted text 

#### B.3* Each processing round consists of the following actions:
1. Create (or simply get if you have already calculated it in section A) the according subkey
2. In each round:
- The left part becomes the right part
- The right part is calculated as a sum of the left part plus a function *f* on the right part and the according subkey.
For example, for round 1 we will need the first subkey, for round 2 the second and so on.
Here is how the function *f* works: 
a. Perform an expansion permutation* on the right 32-bit part (RPT). This will produce a 48-bit block.
[This is how to map the bits for the expansion permutation](https://www.tutorialspoint.com/cryptography/images/des_specification.jpg)
b. XOR the expanded permutated part (block) with the according 48-bit subkey.
c. We now have a 48-bit block. Split the block into 8 6-bit blocks and perform an S-Box permutation on each block.
Here  is how the S-Box permutation works with an example:
	- This is a 48-bit part:
110101 000101 100100 010010 100001 000011 010101 000010
	- This is the second 6-bit block of the 48-bit part:
0|0010|1 
	- We use the first and the last bit to form a 2-bit *i* binary number: 01
	- We use the rest of the middle 4 bits to form a 4-bit *j* binary number: 0010
	- For each block we are given a specific *S* table. For block number 2 for example we the table *S2* out of 8 *S* tables:
	-
| i / j | 0 | 1 | 2  | 3 | 4 | 5 | 6  | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
| - | - | :-: | :-: | :-:|:-:|:-:| :-: | :-: | :-:|:-: | :-:  | :-:  | :-:  | :-:  | :-:  | -: |
| **0** | 15 | 1 | 8 | 14 | 6 | 11| 3| 4 | 9 | 7 | 2 | 13 | 12 |0 | 5 | 10
| **1** | 3 | 13 | 4 | 7 | 15 | 2 | 8 | 14 | 12 | 0 | 1 | 10 | 6 | 9 | 11 | 5 |
| **2** | 0 | 14 | 7 | 11 | 10 | 4 | 13 | 1 | 5 | 8 | 12 | 6 | 9 | 3 | 2 | 15 |
| **3** | 13 | 8 | 10 | 1 | 3 | 15 | 4 | 2 | 11 | 6 | 7 | 12 | 0 | 5 | 14 | 9 |

[You can find all S-Box permutation tables here](https://upload.wikimedia.org/wikipedia/commons/4/44/DES_S-box.jpg)
- Select the number that is on the *i*-th row and *j*-th column. This number is the output *S2(B2)* (*S2* for the second block)
- Take the *Sx(Bx)* outputs and concatenate them. We will now get a 32-bit part.
d. Perform a P-Box permutation on the 32-bit S-Box output to obtain the final value of *f(RPT, subkey<sub>round</sub>)*
[This is how to map the bits for the P-Box permutation](https://image3.slideserve.com/5813050/p-box-l.jpg)

#### B.4* Final Permutation - Reverse Initial Permutation:
After we have completed all 16 rounds of encryption here is what we will do:
1. We have the output *L<sub>16</sub>R<sub>16</sub>*, which is a combination of the left and right 16-round parts.
Reverse the two parts to obtain *R<sub>16</sub>L<sub>16</sub>*
2. Apply the final permutation* (IP<sup>-1</sup>).
[This is how to map the bits for the final permutation](https://www.researchgate.net/profile/Professor_Fahim_Akhter/publication/270680867/figure/tbl2/AS:642486745714688@1530192185514/nverse-Initial-Permutation-IP-1-13.png)

## C. Decryption
To decrypt an encrypted message simply apply the process of encryption using the 16 subkeys in reverse order.

#### Permutation:
- A permutation is effectively a shuffling of elements. 
- A compression permutation is a permutation that ignores certain elements
- An expansion permutation is a permutation where elements are repeated (counted for more than one times)

#### Notes:
**ECB (Electronic Code Book)** mode: each 64-bit block of the original text is encrypted individually
Other modes: **CBC (Chain Block Coding)** and **CFB (Cipher Feedback)** make each cipher block dependent on all the previous message blocks through an initial XOR operation.

Sources:
https://www.geeksforgeeks.org/data-encryption-standard-des-set-1/
http://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm
https://jhafranco.com/2012/02/10/simplified-des-implementation-in-python/

> Written with [StackEdit](https://stackedit.io/).
