# 🔴⚫ Checkers AI Solver

This project implements a **Checkers AI** that autonomously plays both sides using **Alpha-Beta Pruning**. It reads an initial board state from a file, calculates the best sequence of moves until the game ends, and writes each board state along the way to an output file.

---

## 📌 Features

- ✅ Alpha-Beta pruning with a configurable depth limit (default: 7)
- ✅ Enforces **mandatory jumps** and supports **chained jumps**
- ✅ Handles **piece promotion** (kinging)
- ✅ Plays both red (`r`/`R`) and black (`b`/`B`) sides
- ✅ Strategy-aware behavior:
  - Wins **as fast as possible** when a win is guaranteed
  - **Delays loss** when defeat is unavoidable
- ✅ Simple, file-based input/output system

---

## 📂 Input Format

The AI expects a text file containing an 8×8 board like this:

.......b
..r...b.
........
R...b.b.
........
..r.....
...r....
....B...

where b is black and r is red. Each empty space is indicated by a dot. Kings are indicated by 
capital letters.

---

## 📤 Output Format

The output is a text file showing the full move sequence, where each board state is separated by a blank line.

.......b
..r...b.
........
R...b.b.
........
..r.....
...r....
....B...

.......b
..r...b.
........
R...b.b.
.r......
........
...r....
....B...

... (more moves) ...


---

## 🚀 Usage

### 1. Prepare an input file

Save your board configuration to a file like `input.txt`.

### 2. Run the solver

```bash
python checkers_ai.py --inputfile input.txt --outputfile output.txt


🧠 AI Logic

Search: Alpha-Beta Pruning with depth limit

Evaluation Function: Considers:

Material value (normal pieces and kings)

Positional advantage (center control, promotion potential)

Chain jump opportunities

Edge safety

Mobility and numerical advantage

Game End Detection: Automatically ends when one player has no pieces

🛠️ Configuration

To increase or decrease search depth, change this variable at the top of the file:



