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
10|110010 -> 110010|10<br>
[For rounds subkeys 1, 2, 9 and 16, perform a single-bit left shift.
For other rounds, perform a double-bit left shift.](https://media.geeksforgeeks.org/wp-content/uploads/666-2.png)
- Perform a compression permutation* on the concatenated two key parts.<br>
[This is how to map the bits for the compression permutation](https://media.geeksforgeeks.org/wp-content/uploads/777.png)
5. After all 16 rounds of step 4 we will get all the subkeys

## B. Encryption
1. Perform the IP ([Initial Permutation*](https://media.geeksforgeeks.org/wp-content/uploads/444-3.png)) on the 64-bit input text
2. Split the 64-bit permutated text into two 32-bit parts: **LPT** and **RPT**
3. Process* the two parts 16 times using each one of the 16 subkeys
4. Perform the final permutation* (Reverse Initial Permutation - IP<sup>-1</sup>)
5. We now have the 64-bit encrypted text 

#### B.3* Each processing round consists of the following actions:
<ol>
<li>Create (or simply get if you have already calculated it in section A) the according subkey</li>
<li>
In each round:
<ul>
<li>The left part becomes the right part</li>
<li>The right part is calculated as a sum of the left part plus a function <i>f</i> on the right part and the according subkey. <br>
For example, for round 1 we will need the first subkey, for round 2 the second and so on. <br>
Here is how the function <i>f</i> works:
<ol type='a'>
<li>Perform an expansion permutation* on the right 32-bit part (RPT). This will produce a 48-bit block. <br>
<a href="https://www.tutorialspoint.com/cryptography/images/des_specification.jpg">This is how to map the bits for the expansion permutation</a>
</li>
<li>XOR the expanded permutated part (block) with the according 48-bit subkey.</li>
<li>We now have a 48-bit block. Split the block into 8 6-bit blocks and perform an S-Box permutation on each block. <br>
Here  is how the S-Box permutation works with an example:
<ul>
<li>This is a 48-bit part:<br>
110101 000101 100100 010010 100001 000011 010101 000010</li>
<li>This is the second 6-bit block of the 48-bit part:<br>
0|0010|1 <br></li>
<li>We use the first and the last bit to form a 2-bit <i>i</i> binary number: 01</li>
<li>We use the rest of the middle 4 bits to form a 4-bit <i>j</i> binary number: 0010</li>
<li>For each block we are given a specific <i>S</i> table. For block number 2 for example we get the table <i>S2</i> out of 8 <i>S</i> tables:
<table>
<tr>
<th>i /j</th>
<th>0</th>
<th>1</th>
<th>2</th>
<th>3</th>
<th>4</th>
<th>5</th>
<th>6</th>
<th>7</th>
<th>8</th>
<th>9</th>
<th>10</th>
<th>11</th>
<th>12</th>
<th>13</th>
<th>14</th>
<th>15</th>
</tr>
<tr>
<th>0</th>
<td>15</td>
<td>1</td>
<td>8</td>
<td>14</td>
<td>6</td>
<td>11</td>
<td>3</td>
<td>4</td>
<td>9</td>
<td>7</td>
<td>2</td>
<td>13</td>
<td>12</td>
<td>0</td>
<td>5</td>
<td>10</td>
</tr>
<tr>
<th>1</th>
<td>3</td>
<td>13</td>
<td>4</td>
<td>7</td>
<td>15</td>
<td>2</td>
<td>8</td>
<td>14</td>
<td>12</td>
<td>0</td>
<td>1</td>
<td>10</td>
<td>6</td>
<td>9</td>
<td>11</td>
<td>5</td>
</tr>
<tr>
<th>2</th>
<td>0</td>
<td>14</td>
<td>7</td>
<td>11</td>
<td>10</td>
<td>4</td>
<td>13</td>
<td>1</td>
<td>5</td>
<td>8</td>
<td>12</td>
<td>6</td>
<td>9</td>
<td>3</td>
<td>2</td>
<td>15</td>
</tr>
<tr>
<th>3</th>
<td>13</td>
<td>8</td>
<td>10</td>
<td>1</td>
<td>3</td>
<td>15</td>
<td>4</td>
<td>2</td>
<td>11</td>
<td>6</td>
<td>7</td>
<td>12</td>
<td>0</td>
<td>5</td>
<td>14</td>
<td>9</td>
</tr>
</table>
<a href="https://upload.wikimedia.org/wikipedia/commons/4/44/DES_S-box.jpg">You can find all S-Box permutation tables here</a></li>
<li>Select the number that is on the <i>i</i>-th row and <i>j</i>-th column and convert it to a 4-bit binary number. This number is the output <i>S2(B2)</i> (<i>S2</i> for the second block). <br>
</li>
<li>Take the <i>Sx(Bx)</i> outputs and concatenate them. We will now get a 32-bit part (4-bit outputs * 8 blocks). </li>
<li>Perform a P-Box permutation on the 32-bit S-Box output to obtain the final value of <i>f(RPT, subkey<sub>round</sub>)</i> <br>
<a href="https://image3.slideserve.com/5813050/p-box-l.jpg">This is how to map the bits for the P-Box permutation</a>
</li>
</ul>
</li>
</ol>
</li>
</ul>
</li>
</ol>

#### B.4* Final Permutation / Reverse Initial Permutation:
After we have completed all 16 rounds of encryption here is what we will do:
1. We have the output *L<sub>16</sub>R<sub>16</sub>*, which is a combination of the left and right 16th-round parts.
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
**ECB (Electronic Code Book)** mode: each 64-bit block of the original text is encrypted individually <br>
Other modes: **CBC (Chain Block Coding)** and **CFB (Cipher Feedback)** make each cipher block dependent on all the previous message blocks through an initial XOR operation.

Sources:<br>
https://www.geeksforgeeks.org/data-encryption-standard-des-set-1/ <br>
http://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm <br>
https://jhafranco.com/2012/02/10/simplified-des-implementation-in-python/

> Written with [StackEdit](https://stackedit.io/).
