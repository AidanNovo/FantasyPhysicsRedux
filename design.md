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

### Specific card ideas:
- Nuclear reactor : Increases neutrino flux, supplies power
  - Power is a resource that can be used by active particle sources
    - Maybe can also be used by computer cards?
    - Consider having power not be just a resource but a positional thing.
    - Right now, there is maybe no reason to not generate power first?
      - But actually, maybe you want to save your power to get used by your ml cluster instead of your beam?
- 
  

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

## Card Design Elements

The card design needs all of the following:
- Card name
- Card type
- Card tags
- Card image
- Mechanic description (get templating)
- Outreach flavor text
- Card level?
- Card rarity marker?