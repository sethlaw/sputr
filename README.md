 _______  _______  __   __  _______  ______   
|       ||       ||  | |  ||       ||    _ |  
|  _____||    _  ||  | |  ||_     _||   | ||  
| |_____ |   |_| ||  |_|  |  |   |  |   |_||_ 
|_____  ||    ___||       |  |   |  |    __  |
 _____| ||   |    |       |  |   |  |   |  | |
|_______||___|    |_______|  |___|  |___|  |_|

Security Payload Unit Test Repository (SPUTR)
---
A repository of payloads for security unit/integration testing.

Quickstart
--
1- TODO

Layout
--
/
generate_payloads.py # For generating values into the payloads directory
../payloads/ <- Start here for different payload sets
../exploit_chars/ # Used by generate_payloads, interesting characters by vulnerability
../libs/ # language/framework libraries for including in unit tests.
