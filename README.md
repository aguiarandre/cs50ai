
# <h1 align='center'>:crystal_ball: CS50ai :crystal_ball:</h1>

<p align='center'> CS50's Introduction to Artificial Intelligence with Python repo.</p>
<p align='center'><img src="media/TODO.png" alt="" width="75%"/> </p>

# Projects

## Search Problems
Search problems can be modeled as an `agent` within an `environment`. This agent has an initial `state (S)`, and after fulfilling an `action (A)`, ends up in a resulting new state (resembling a `transition model`). The objective is to go from an `initial state` to an `end state` after a series of `actions`. As we'll realize, several problems can be thought of as a `search problem` as well.

`TODO`: cite frontier and node as main data structures that help understand these solutions.

[Degrees](01-search/project/degrees/srs)         |  [Tic-Tac-Toe](01-search/project/tic-tac-toe/src)
:-------------------------:|:-------------------------:
<img src="01-search/project/degrees/src/media/frontier/frontier.gif"  width="300"/>  |  <img src="01-search/project/tic-tac-toe/src/media/computer-won.png" width="300"/>
Nodes and Frontiers | MinMax Strategy 
Breadth First Search | Adversarial Search
Depth First Search | ![formula](https://render.githubusercontent.com/render/math?math=\alpha-\beta) Pruning



## Knowledge
`TODO`: Talk about knowledge representation, how proposition logic is important (and we usually ignore, don't see applications and so on) and how inference is interesting and powerful.

`TODO`: Talk about resemblance with search problems: given state and action leading to an inferred new proposition.

[Knights and Knaves](02-knowledge/project/knights/)         |  [Minesweeper](02-knowledge/project/minesweeper/)
:-------------------------:|:-------------------------:
<img src="02-knowledge/project/knights/media/TODO.png"  alt="" width="300"/>  |  <img src="02-knowledge/project/minesweeper/media/pygame-minesweeper-32x32.gif" width="300"/>
Proposition Logic | Knowledge representation 
| | Inference


## Dealing with Uncertainty
`TODO`: Talk about bayes-rule, bayesian network, probability distribution, markov chains, transition model.

[Pagerank](03-uncertainty/project/pagerank/) | [Heredity](03-uncertainty/project/heredity/)
:-------------------------:|:-------------------------:
<img src="03-uncertainty/project/pagerank/TODO" alt="" width="300"/> | <img src="03-uncertainty/project/heredity/media/bayesian-network.png" alt=""  width="300"/>
Random Surfer Model  | Bayesian Network 
Markov Chain | Probability Distribution 


## Optimization Strategies
`TODO`: Talk about the different types of optimization strategies. 

`TODO`: Talk about concepts similar to previous learnings, frontiers (available worlds), neighbors, resemblance with search and knowledge engineering and representation.

Local Search (Hill-Climbing)| Linear Programming (Lagrange Multipliers)  | Constraint Satisfaction Problem (CSP)
:-------------------------:|:-------------------------:|:------------:
<img src="04-optimization/class/media/hill-climbing.png"  width="300"/>  |  <img src="04-optimization/class/media/linear-programming.png" width="300"/> | <img src="04-optimization/class/media/csp.png" width="300"/>

`TODO`: Specify that sudoku was an independent project. Deepen on Constraint Satisfaction Problems and how modeling a sudoku was the tough part. Node Consistency was easy, Arc consistency was tough.


[Crossword](04-optimization/project/crossword)         |  [Sudoku](04-optimization/project/sudoku)
:-------------------------:|:-------------------------:
<img src="04-optimization/project/crossword/media/output.png"  width="300"/>  |  <img src="04-optimization/project/sudoku/media/1/output-easy-v2.gif" width="300"/>
Node Consistency | Modeling (Variable, Row, Column, Box)
Arc Consistency | Restriction Representation
AC3 Algorithm | Backtracking

## Learning from Data

`TODO`: Talk about the simplicity of shopping. That it should not be considered as a real-life example of what a classification problem look like - explain why (load-data, missing, data pipeline, so on)

`TODO`: discussion on reinforcement-learning problem. Talk about the interesting (philosophically speaking) part concerning the fact that a `learning step`, so to speak, is composed at the same time by a `reward` **AND** a `punishment`, because the AI both wins and lose at the same time.

[Shopping](05-learning/project/shopping/)         |  [Nim](05-learning/project/nim/)
:-------------------------:|:-------------------------:
<img src="05-learning/project/shopping/TODO.png" alt=""  width="300"/>  |  <img src="05-learning/project/nim/TODO.png" alt="" width="300"/>
Simple Classification Model | Reinforcement Learning
| | Q-Learning

## Neural Networks Concepts
`TODO`: Talk about neural networks architectures. Image convolution and max-pooling strategies. Dropout for regularization, how it may avoid over-reliance on specific weights. 

[Traffic](06-neural-networks/project/traffic/)         | |
:-------------------------:|:-------------------------:
<img src="06-neural-networks/project/traffic/TODO.gif"  alt="" width="300"/> | |
Image Classification | |
Hidden Layers | |
Convolution | |
Pooling Layers | |
Dropout | |


## Natural Language Ideas
`TODO`: Talk about language structures, context-free grammar, applications on classification and topic modeling (with a nice simple application using only tf-idf for it (not complex LDA or stuff like that)), word representation as basis of a high-dimensional field, distributed representation and how word2vec represents words that appear in the same context more often as closer vectors in this distriuted dimension.

[Parser](07-language/project/parser/)         |  [Questions](07-language/project/questions/)
:-------------------------:|:-------------------------:
<img src="07-language/project/parser/TODO.gif"  alt="" width="300"/>  |  <img src="07-language/project/questions/TODO.png" alt="" width="300"/>
Context Free Grammar | Term Frequency
| | Inverse Document Frequency
| | Markov Chains 
| | Word Embeddings

