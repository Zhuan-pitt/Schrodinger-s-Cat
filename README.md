# Catch Schrödinger's Cat
The Kingdom of Physics is in chaos since King Schrödinger's cat is missing. The king sends his greatest knight, you, to catch his cat. However, this unusual cat possesses an extraordinary ability of superposition: it can be found simultaneously at two positions. Will you be able to track down the mysterious cat and bring the Kingdom of Physics back to calm? 

<img width="1198" alt="start" src="https://github.com/Zhuan-pitt/Schrodinger-s-Cat/assets/70167028/8092da88-bc2f-4054-bc1d-b9f098f3cfbb">


## Rules
The game takes place on a 10 $\times$ 10 chessboard. Everyday the cat can move one or two squares in any direction (the same as Kings in chess, but it can move one or two steps), and the knight can move as a "L" shape (the same as Knights in chess). The cat and the knight move alternatively. You are required to use one Knight to capture the cat. 

However, the cat can be in a superposition state of two locations: the origin and the destination. It will only collapse to a determined location after the knight makes its move. In order to have a better chance of capturing the cat, you can apply quantum gates on the cat to change its state before moving the knight. You can find four different quantum gates randomly located on the board: Pauli-X gate ($X$), Pauli-Z gate ($Z$), Hadamard gate ($H$), and the phase gate ($S$). Additionally, you can find M on the board representing Measure, which allows you to measure the superposition state before moving the knight.

Walls are added to the chessboard. The cat is always able to tunnel through the wall (due to its high energy), but the knight will have to collect Energy Capsules from the chessboard to tunnel through the wall via the quantum tunneling effect.

A demonstrating video of the game can be found [here](https://youtu.be/Soxb8MSjrIA).

<img width="1199" alt="game" src="https://github.com/Zhuan-pitt/Schrodinger-s-Cat/assets/70167028/aff3629b-645e-47eb-bed9-b5a3f18e3b62">

## Theory of Quantum gates behind the game

Here, we denote the state of the cat at the origin at each step as $|0\rangle$ and at the destination as $|1\rangle$. After the cat makes the move, it will be in the superposition state of $|0\rangle$ and $|1\rangle$, i.e.
```math
\begin{equation}
\Psi_{cat}=\frac{|0\rangle+|1\rangle}{\sqrt{2}} \quad \text{or} \quad \Psi_{cat}=\frac{|0\rangle-|1\rangle}{\sqrt{2}}
\end{equation}
```
Therefore, the cat has an equal probability of remaining at the origin or jumping to the destination.

The Pauli-X gate is defined as 
```math
X=\left[\begin{array}{ll}
0 & 1 \\
1 & 0
\end{array}\right]
```
which can switch state $|0\rangle$ to $|1\rangle$ and $|1\rangle$ to $|0\rangle$.


The Pauli-Z gate is defined as 
```math
Z=\left[\begin{array}{cc}
1 & 0 \\
0 & -1
\end{array}\right]
```
which can switch state $|1\rangle$ to $-|1\rangle$ and keep $|0\rangle$ unchanged.


Hadamard gate $H$ is defined
```math
H=\frac{1}{\sqrt{2}}\left[\begin{array}{cc}
1 & 1 \\
1 & -1
\end{array}\right].
```
Hadamard gate can be used to change the basis, i.e., $HZH=X$.

Phase gate $S$ is defined as
```math
S=\left[\begin{array}{cc}
1 & 0 \\
0 & e^{i \frac{\pi}{2}}
\end{array}\right].
```
It is easy to find that $Z=S^2$.
## Strategy Guidance
As an example, if we want to obtain $\Psi_0 = |0\rangle$ (or $\Psi_1 = |1\rangle$) from $\Psi_{super}=\frac{|0\rangle+|1\rangle}{\sqrt{2}}$, one possible strategy is that first measuring the superposition state (using $M$) and if needed applying Pauli-X gate ($X$) to obtain the desired state. 

Alternatively, one can obtain $\Psi_1 = |1\rangle$ by sequentially applying Pauli-Z gate ($Z$) and Hadamard gate ($H$) on $\Psi_{super}=\frac{|0\rangle+|1\rangle}{\sqrt{2}}$.

There are many other alternative strategies to obtain a desired state, depending on the available quantum gates for operations.

## Installation
To start the game, make sure you have installed the Python Library ```numpy``` and ```pygame```. It can be installed via pip:
```
pip install pygame
pip install numpy
```
The game can be downloaded via
```
git clone https://github.com/Zhuan-pitt/Schrodinger-s-Cat.git
```
Open the downloaded folder and run
```
python main.py
```
## Note
- For simplicity, in the superposition state displayed in the game, the coefficient of $|0\rangle$ is always shown as 0 or 1. The normalization coefficient is neglected.
- The coefficient $j$ in the superposition state indicates the imaginary unit.
