# 02180_AI_belief_revision

### Authors
* [Ivan Serrano Subtil ](https://github.com/ivans14) (212477)
* [Manuel del Angel Tena ](https://github.com/manu2022) (213286)
* [Daniel Paez Martin ](https://github.com/iZelex) (212600)

### Description
Implementation of a belief revision agent. The propositions are introduced from the display and the belief base system will update itself to remove any inconsistency with its beliefs. The library Sympy has been used to easier handle of the proposition formulas and have more time to design and implement a competent Belief Base system.

### Project distribution
* `display.py`: Contains the classes and methods used for handleing the graphical display of the project. 
* `beliefBase.py`: Core file of the project containing the class for the belief base and the class for beliefs. Handles most of the logic and main code for defining the agent.
* `entailment.py`: Implementation of the entailment check between the belief base and the new proposition.
* `utils.py`: Useful fucntions left for further work in the future as the time didn't allowed to properlly implement them in the system yet.


### Run the program
To run the project run the `display.py`. 

### Notes
* The system doesn't allow for bi-implication yet as the implementation has resulted tricky and could't make it in time. We recomend transforming the expression and using the logical operators avaible for you on the display.
* When implementing logical operators use the buttons as the system recognizes those symbols as operators but perhaps not other equivalent for people, such as: (Implication) '->', '=>' or '>>'.
* Lower and upper case are indifferent in the system.


### We hope you enjoy our revision agent :)
