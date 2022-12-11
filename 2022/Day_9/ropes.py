import numpy as np

lines = []
with open('./input.txt') as f:
    for line in f:
        lines.append(line.strip())


# === First Part ===
class Tail:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.grid = np.zeros(shape=(height, width))
        self.grid[height//2, width//2] = 1
        self.rel_pos_head = [0, 0]
        self.tail_pos = [height//2, width//2]

    def pull_rope(self, move):
        if isinstance(move, str):
            direction, magnitude = move.split(' ')
            prev_tail_pos = self.tail_pos.copy()
            for mag in range(int(magnitude)):
                if direction == "U":
                    self.rel_pos_head[1] += 1
                elif direction == "D":
                    self.rel_pos_head[1] -= 1
                elif direction == "R":
                    self.rel_pos_head[0] += 1
                elif direction == "L":
                    self.rel_pos_head[0] -= 1
                tail_move = self._move_tail()
                self._update_grid(tail_move)
        elif isinstance(move, list):
            prev_tail_pos = self.tail_pos.copy()
            self.rel_pos_head[0] += move[0]
            self.rel_pos_head[1] += move[1]
            tail_move = self._move_tail()
            self._update_grid(tail_move)

        total_tail_move_x = self.tail_pos[0] - prev_tail_pos[0]
        total_tail_move_y = self.tail_pos[1] - prev_tail_pos[1]
        return [total_tail_move_x, total_tail_move_y]

    def _move_tail(self):
        if abs(self.rel_pos_head[0]) < 2 and abs(self.rel_pos_head[1]) < 2:
            tail_move = (0, 0)
        elif abs(self.rel_pos_head[0]) == 2:
            tail_move = (2/self.rel_pos_head[0], self.rel_pos_head[1])
        else:
            tail_move = (self.rel_pos_head[0], 2/self.rel_pos_head[1])

        self.rel_pos_head[0] -= tail_move[0]
        self.rel_pos_head[1] -= tail_move[1]

        return tail_move

    def _update_grid(self, tail_move):
        self.tail_pos[0] += tail_move[1]
        self.tail_pos[1] += tail_move[0]
        self.grid[int(self.tail_pos[0]), int(self.tail_pos[1])] += 1


max_height = 0
max_width = 0
for line in lines:
    direction, magnitude = line.split(' ')
    if direction == "U":
        max_height += int(magnitude)
    elif direction == "R":
        max_width += int(magnitude)
    elif direction == "D":
        max_width += int(magnitude)
    elif direction == "L":
        max_width += int(magnitude)

tail = Tail(max_height * 2, max_width * 2)
for line in lines:
    _ = tail.pull_rope(line)

print("Places visited: ", np.count_nonzero(tail.grid))


# === Second Part ===
class LongTail(Tail):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.node2 = Tail(height, width)
        self.node3 = Tail(height, width)
        self.node4 = Tail(height, width)
        self.node5 = Tail(height, width)
        self.node6 = Tail(height, width)
        self.node7 = Tail(height, width)
        self.node8 = Tail(height, width)
        self.node9 = Tail(height, width)
        self.node10 = Tail(height, width)
        self.grid = self.node10.grid

    def pull_rope(self, move):
        move1 = self.node2.pull_rope(move)
        move2 = self.node3.pull_rope(move1)
        move3 = self.node4.pull_rope(move2)
        move4 = self.node5.pull_rope(move3)
        move5 = self.node6.pull_rope(move4)
        move6 = self.node7.pull_rope(move5)
        move7 = self.node8.pull_rope(move6)
        move8 = self.node9.pull_rope(move7)
        move9 = self.node10.pull_rope(move8)

        self.grid = self.node10.grid

longtail = LongTail(max_height * 2, max_width * 2)
for line in lines:
    longtail.pull_rope(line)
