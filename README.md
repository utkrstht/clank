# clank
clank is an review tool specifically for hack club stardance, it can run quick checks on projects for common rejection reasons and create proof review video as well for faster reviews.

### features
clank runs these checks on a project:
- Valid raw README link check
- No README/Short README check 
- Private/Non-existent repository check
- Private/Non-existent demo check
- Demo pointing inside repository check
- Unallowed hosting providers for demo check
- Basic AI README check
- AI generated Stardance project banner check (via C2pa metadata)
- AI codebase check
- Stardance project banner relevance check
and probably a few more that I forgot(?)

once these checks are complete, depending on whatever issues there were present, clank creates a rejection message and a proof video via selenium

for the proof videos, clank opens the repository, demo and stardance project page and goes through them, including all repository files that would be considered in the checks.

clank aims to use little to no AI in it's review processes compared to other similar projects, but this has it's own flaws such as missing sloppy websites with little to no AI signs in it's codebase.

clank is a good boy and good at it's job (i hope), i'll probably add a pat feature for clank in the future so you can pet it for good reviews

### goals
- ~~Create review videos~~
- Link with Slack and Fiona

### ai usage
(this is regarding ai usage in the development process of clank, not the review processes in clank)  
AI usage is so incredibly little, you can scroll through the code and I've added little comments which show you where AI was used

### outro
clank is pretty bad right now, it's not all that good but yeah  
made with love by kaboom (utkrstht)  
MIT License  