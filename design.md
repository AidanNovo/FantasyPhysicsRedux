## General Brainstorming

If I really want the GUI to be more responsive, I should implement some multiprocessing

Ideas for additional cards
I think there are a handful of areas I can develop cards in
- More 'core' cards——detectors, sources, and analysis
- Objective cards——big overall theme stuff, maybe sort of like MTG color pie?
- Auxiliary cards——little 'extra' cards for people to slot in that do more unique things

What if data storage is a thing? Like you have a certain max amount of data?
- Inspired by CERN's many issues with long-term data storage
- Analysis doesn't really use up your data, though...
  - Maybe some analysis cards can _refine_ your data? Like, reduce your total data amount by half but also gain a multiplier to its efficacy?

For aesthetic reasons at the very _least_, neutrino flux should be high but neutrino detectors convert flux to data inefficiently

Incorporate particle energies somehow?
- Make particle beams scale energy based on power?
- Really this is kind of poking at a deeper idea, which is the idea of having qualities/attributes to the things you generate

### Idea: Token Expansion
- Second row of cards (or tokens or coins or whatever we want to call them)
- This second row are the particles and data and such that our experiment is generating
  - Could be sort of nice aesthetically to see your sources generate things then your detectors act on them
  - This can also incorporate some of the "capacity" things I like the idea of--e.g. max amount of data
    - The capacities can visually be the width of the token's row
    - Consider whether it is fun to have to need to manage your capacities
  - Particle tokens can decay after X ticks (i.e. X card activations)
    - I really like this idea
    - Teaches people about decay modes also?
      - Will probably need to simplify a bit
  - Do background particles get constantly added?
    - E.g. if you have a proton detector build, do you need to worry about neutrinos coming in?
    - This is only a problem (mechanically) if you have a max particle capacity
    - Maybe ask Dr. Rogan if particle pollution is a problem
      - Noise?

Neutrino cards could ignore some impediments? Flavored after neutrino non-interaction
Maybe neutrinos are unique in that there is a global 'neutrino flux' value, whereas say protons are only available to
the next few cards? To represent how you can just shoot a neutron beam to _anywhere_.

So, under this design, rounds flow like this:
1. Pick / arrange cards
2. Start round
3. Each tick:
   1. Activate all tokens (top to bottom, left to right)
   2. Activate current card

## Token Refactor Structure
cards.py - hold card (and token) definitions

main.py - gui stuff

Each place cards can go is a card_holder object
Function to add a new card to a card_holder
Function to move them between card_holders
When activating cards, you go down the row in the order of card_holder activation


### Specific card ideas:
- **Nuclear Reactor** : Increases neutrino flux, supplies power
  - Power is a resource that can be used by active particle sources
    - Maybe can also be used by computer cards?
    - Consider having power not be just a resource but a positional thing.
    - Right now, there is maybe no reason to not generate power first?
      - But actually, maybe you want to save your power to get used by your ml cluster instead of your beam?
- **SuperK**
  - Discussed w/ Dr. Rogan, he suggests that we have super-k tuned for lower energy neutrinos
- **IceCube**
  - Discussed w/ Dr. Rogan, he suggests that we have IceCube tuned for higher energy astroparticle neutrinos
- **Neutrino Oscillation (topic)**
  - I want to encourage spacing out your detectors (simulate long baseline experiments)
  - So, something like:
    - Neutrinos with flavors not previously detected generate 2x data
      - This also requires a neutrino token rework where the oscillation chance is random (is random good?)
      - Note: this will be difficult to implement in the current code framework. Passive effects are not well-supported
    - When a neutrino is re-detected with a different flavor, it generates 2x data
      - This will also be very hard to implement in the current framework
  - 2x score if you have at least 2 \[detector] cards
    - A bit blunt and basic, but easy to implement
  - Multiply score by (1.5 * \[number of spaces between your two furthest detector cards])
    - A little more interesting, also easy to implement
- **Sterile Neutrino Search (topic)**
- **Neutrino Mass Measurement (topic)**
- **Computing Center (special)**
  - Has 'computer' tag
  - Increase size of data row
  - Grants passive: All other cards with the 'computer' tag trigger twice (hard to implement right now)
  - Name this after a real tier 1 or tier 2 CERN computing center
  - Consumes power
  - Stupid idea but I think it is fun: High energy particles can 'flip bits' and interact with this?
    - This actually provides a little bit of a downside to 
- **Coal power plant (special)**
  - Generates lots of cheap power tokens
  - Also generates pollution tokens which do something bad
    - Clog up your token rows? Incur a negative effect when activated each tick?
    - If we do score attack, maybe pollution sticks around between rounds? So it really does incur escalating costs?
- **Renewable power plant (special)**
  - (wind, hydro, etc.)
  - Generates a few power tokens
  - No downside
- **Shielding card (special)**
  - Basically just a card that is _really_ good at blocking particles. To reduce noise for sensitive detectors
- **Monte Carlo Sim (analysis)**
  - Maybe some sort of random effects?
- **Background Modeling (analysis)**
  - We want this to be good for things that are noise sensitive
  - Maybe data tokens have a signal:noise ratio? And this can improve that?
    - How would the signal:noise ratio be determined?
    - I think ideally the concept of 'signal' and 'noise' is emergent rather than baked in.
    - Relevant issue here is that the 'signal' and the 'noise' are on top of one another rather than separate.
    so e.g. having 'noise' be a bunch of low-value data tokens does not really represent it perfectly. It leads to
    strange behaviors like being able to fix your signal:noise ratio by building more data storage.
      - That said, this is still a _pretty_ good implementation.
  - If we go with the 'noise is low-value data tokens' approach, background modeling could have the effect of
  removing your X lowest-value data tokens
- **Accelerator Ring (special)**
  - Like they have at CERN!
  - Increase the energy of any particles generated

### Passive Card Implementation
The more I think about things, the more I really think we need 'passive' cards.
I am imagining having passive cards be wide 'sideways' rectangles, display under decklist (make decklist collapsible).

Question is, to some degree, what does 'passive' mean?
- I think maybe I mean 'cards that modify what other cards do'
- Or maybe it is mostly just "cards that are always active"
  - But again, what does that really _mean?_
- This is hard to implement in a scalable way. It is easy to make it so that every neutrino detector just checks if you 
have a 'neutrino oscillation' card, but once every detector is checking for 8 different passives, things get clunky
  - Ideally, the passive effect lives entirely in the passive card object.
  - Maybe we do an 'event' system? E.g. in nubby, you have 'peg doubled -> do effect'. We could have a standardized set
  of events that are broadcast?
  - Could have passive cards activate in the f_card_start() / f_card_end() functions in order to modify things
  - Not sure if this fully fixes the issue with modularity. It is better than having every single card check for this

You could possibly implement this with a big rewrite to make things event and observer based

Thinking about implementing an "all cards with the computer tag trigger twice" effect
- Put some logic in the start function that checks if the next card is a computer card? Hard to implement
- Have an observer object sitting around (passive card) listening for a "card triggered" event
  - Observer card can be created by the computing center card
  - Check the event for whether the card has a computer tag
  - If so, put a copy of the card trigger event (without the computer tag) onto the stack
    - This means I have to implement a stack

Passive cards could include:
- Physics topic cards
- Outreach modifier cards

Passive cards are definitely going to grant you an observer 'token' at least behind the scenes
Putting that into the GUI could be good for players understanding the mechanics
- Requires additional design work

Question is really _when_ you get that observer token
- Created at start of round:
  - Allows for us to not do the gui tokens, we just imagine the card up in the row is doing this
  - Less hassle, feels more like a passive _on the card_
  - More interesting card ordering interactions?
    - Incentivizes using the passives like filler cards (passives must be ordered still)
  - Feels a little cleaner, and I am sort of worried about the game getting overly complex
  - I think this is what I want to do
- Created on card activation
  - Goes more with previous design ideas, easier to implement
  - More interesting card ordering interactions?
    - Incentivizes putting good passives all the way left

Alternative idea: Make passive cards a special card type, all cards with passive effects go left
- Makes deck display / pack opening messy
- Slightly cleaner design-wise
- Bad idea I think
- Also, I think it is a little *too* nice to players. They should have to work with a limited number of slots


### Outreach scaling rework
I don't really like the 'current' idea for outreach scaling where each card just gets
a numerical bonus based on some nebulous outside factor.

Can I do my outreach scaling differently? Current problems:
- Inelegant
- Makes cards extremely wordy
- Kind of overcomplicated if we want detailed bonuses
- We want people to be able to precisely predict what the outreach bonus will be

Idea:
- Sidebar includes a breakdown of the outreach multipliers
  - This fixes the problem with cards having limited real estate
  - But also makes it harder for people to predict exactly what the outreach bonus will be

Change my card function architecture so all functions call a base function first (inheritance basically)
and that base function is responsible for performing universal card behaviors
- E.g. all computer cards will draw power if available

The core question I am asking for everything is:
"How is this experiment/detector/analysis method different from others?"

Idea:
- Display power tokens under cards like energy cards in the pokemon TCG

Idea:
- Tentpole physics card effects can change how the basic physics works
- e.g. If you have a card representing a theory that says that protons can decay, then protons can decay

Idea:
- Neutrino oscillation card can reward you more for having different flavors of neutrino?

Idea:
- Almost all topic cards should provide data scaling given specific conditions are met
- E.g.
  - neutrino oscillation multiplies data generated by neutrinos that have oscillated
  - Astroparticle research multiplies data generated by high energy particles
- The inspiration for this came from the realization that 'what data is 'good' is just a function of what you are
looking for. When thinking about the background modeling analysis card, I wanted it to throw out non-useful data,
and thus had to think about what 'non-useful data' means



## Card Design Graphic Elements

The final card design needs all of the following:
- Card name
- Card type
- Card tags
- Card image
- Mechanic description (get templating)
- Outreach flavor text
- Card level?
- Card rarity marker?

## Score Attack Mode Brainstorming

Basic score attack mode should just be like:
- Beat X score
- If you do so, you get to pick a pack to open
- Continue for as long as you can
