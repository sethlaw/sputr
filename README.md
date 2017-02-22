Security Payload Unit Test Repository (SPUTR)
---
A repository of payloads for security unit/integration testing.

Quickstart
--
1- sputr.py -h

Layout
--
* /
* sputr.py           # Go here for everything
* ../payloads/       # Different payload sets
* ../exploit_chars/  # Used by generate_payloads, interesting characters by vulnerability
* ../libs/           # language/framework libraries for including in unit tests.


config.json
---
To generate and start tests, need to build a config.json file. There are a few required json parameters if you building it by hand.
