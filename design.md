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

Neutrino cards could ignore some impediments? Flavored after neutrino non-interaction
Maybe neutrinos are unique in that there is a global 'neutrino flux' value, whereas say protons are only available to
the next few cards? To represent how you can just shoot a neutron beam to _anywhere_.

Specific card ideas:
- Nuclear reactor : Increases neutrino flux, supplies power
  - Power is a resource that can be used by active particle sources
    - Maybe can also be used by computer cards?
    - Consider having power not be just a resource but a positional thing.
    - Right now, there is maybe no reason to not generate power first?
      - But actually, maybe you want to save your power to get used by your ml cluster instead of your beam?
  

Change my card function architecture so all functions call a base function first (inheritance basically)
and that base function is responsible for performing universal card behaviors
- E.g. all computer cards will draw power if available

The core question I am asking for everything is:
"How is this experiment/detector/analysis method different from others?"


## GUI Card Class
I want to make a class to handle the cards as they appear in the GUI
Ideas:
- Make it inherit from tk.Button (probably)
  - Clicking it moves it from active row to deck and back.
- Click and drag feature?
- Have it linked to the backend Card object to which it is bound
- Have hover text for displaying up-to-date card function data (just for development)
  - This is so I don't need to make a new card image every single time I want to tweak a parameter
  - Pull this from the card_dict


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