# Visualizer 

Press A to Start = AStar Algorithm
Press D to Start = Depth First Search
Press B to Start = Breath First Search 

> Working on Dijsktar Algorithm 


# A* Algorithm 
Heuristic Meaning = Enabling someone to discover or learn something for themeselves 
> a "hands-on or interactive heuristic approcah to learning"

> Wikipedia = A heuristic, or heuristic technique, is any approach to problem solving or self-discovery that employs a practical method that is not guaranteed to be optimal, perfect, or rational, but is nevertheless sufficient for reaching an immediate, short-term goal or approximation

The idea behind heuristic approach is to give us educated guess as to which node that we should look at next that are currently on the path that we have found. Basically, heuristic is a guess and a better guess we use, we try to find the best solution. 

In this algorithm we decide which direction we will be moving at based on three factors. Those three factors are score or costs associated with every single node and they are denoted by H, G and F. 

> H Stands for Heuristic Value. The guess how far our start node to the end node. 

> G stands for current shortest distance from the start node to this given node (current Node)

> F is simply the addition of  G + H

When we look at what node we want to visit next, we will look for the node that has current smallest F Score 

We will start with the start node and it will always have the G score of zero. 

We can only move on forward direction in this algorith, and this call us for to use a heuristic called manhattan distance(L distance). We just take difference between the rows and the difference between the column and add those together. Basically, distance formula if you are familiar with trigonometry. (x2-x1)+(y2-y1)

> If we consider diagnoal we can use Euclidean distance. 


If the G Score was greater than what we currently have then we continue. 


# Heap 

A Heap is a Binary Tree but it is a special type of binary tree that satisfies two additional properties. 

1. Completeness - It needs to have all of its level filled up completely except the last level and if its partly filled up then it needs to be filled up from left to the right. 
 0  1  2  3  4  5  6  7   8
[8,12,23,17,31,30,44,102,18]

                          8
                        /  \
                       12   23
                      / \   / \
                     17  31 30 44
                    / \
                  102  18 

> The above binary tree is an example of complete Heap  

2. The Heap  - We can distinguish between min heap and max heap. In the min-heap, every node's value is basically going to be smaller than or equal to its children value. Similarly, if we dealing with max-heap, every node's value should be greater than or equal to its children value 

> A Heap is not sorted as we can see from the tree above. The root node represents the smallest value in the tree. Hence the name Min Heap. 

One beautiful thing about heap is that we can represent them in the form of array. There are some pretty neat properties that we can use to find the children node of a specific node or parent node of a specific node by using indices and using them to calcuate the children node of  the parent node.  

## Finding the Child Node  
We start at index 0 and to find the two children node. In order to find the first children node we multiply the index by 2 and add 1. Similary, to get the second child we multiply the index 2 and add 2.

first_child = current_index *2 + 1 
second_child = current_index *2 + 2

## Finding the Parent Node

Similarly, we we were to find the parent node we subtract the current_node index by 1, divide it by 2 and finally round it down.

parent_node = math.floor(current_index-1 / 2)

# Insertion 

How can I add 9 to my heap ? 

1. Satisfy the heap Property i.e add 9 as a child of the 31. See, the Picture above.
2. After it is added, we check if it satisfies the property, it not we shift it up.  


# Remove 
1. We take the root node and swap it with the final value in the heap. In our example, we would swap 8 and 31 
2. Now since we have our root node at the bottom we basically, pop it of because essentially it is an array representation. 
3. Now, our min-heap is no longer heap, so we take the value and we shift down until it satisfies the min heap property

Shift down involves a little more work compared to the shift up because we will have to account for both of its children node.

