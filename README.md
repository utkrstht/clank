# clank
clank is an review tool specifically for hack club stardance, it can run quick checks on projects for common rejection reasons for faster reviews.

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

once these checks are complete, depending on whatever issues there were present, clank creates a rejection message.

clank uses extremely minimal AI in any of it's review processes only to process image information which could otherwise not be processed programmatically, any and all AI used is strictly limited to processing information which cannot be processed via programatic means

### goals
- Create review videos

### ai usage
(this is regarding ai usage in the development process of clank, not the review processes in clank)  
AI usage is so incredibly little, you can scroll through the code and I've added little comments which show you where AI was used

You may also notice, after me commiting a bit, there's like 47 fix commits, that is because after I do a bit of work, I force opencode to review my code for any bugs because I Write Shit Code.

### outro
clank is pretty bad right now, it's not all that good but yeah  
made with love by kaboom (utkrstht)  
MIT License  