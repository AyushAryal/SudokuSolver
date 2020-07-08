class Board(object):
    def __init__(self, board):
        self.board = board
        self.size = len(board)
        if self.size % 3 != 0:
            raise Exception("Board cannot be partitioned")

        for row in self.board:
            if len(row) != self.size:
                raise Exception("Board is not a square")
        for row in self.board:
            for item in row:
                if item > self.size or item < 0 or type(item) != int:
                    raise Exception("Board item not in range")
        if not self.is_consistent():
            raise Exception("Board is in inconsistent state")

    def print_board(self):
        for row in self.board:
            print(" ".join(map(str, row)))

    def is_consistent(self):
        for i in range(self.size):
            item_set_row = set()
            item_set_col = set()
            for j in range(self.size):
                if (self.board[j][i] in item_set_row and self.board[j][i] != 0) or (self.board[i][j] in item_set_col and self.board[i][j] != 0):
                    return False
                item_set_row.add(self.board[j][i])
                item_set_col.add(self.board[i][j])

        partition_size = self.size // 3
        for i in range(0, self.size, partition_size):
            for j in range(0, self.size, partition_size):
                item_set = set()
                for x in range(partition_size):
                    for y in range(partition_size):
                        if self.board[j+y][i+x] in item_set and self.board[j+y][i+x] != 0:
                            return False
                        item_set.add(self.board[j+y][i+x])
        return True

    def is_solved(self):
        return self.find_empty_square() is None and self.is_consistent()

    def possible_choices(self, x, y):
        if self.board[y][x] != 0:
            return self.board[y][x]

        elimination_set = set()
        for i in range(self.size):
            elimination_set.add(self.board[i][x])
            elimination_set.add(self.board[y][i])

        partition_x = x - x % 3
        partition_y = y - y % 3
        partition_size = self.size // 3
        for i in range(partition_size):
            for j in range(partition_size):
                elimination_set.add(
                    self.board[partition_y + j][partition_x + i])

        return set(range(1, self.size+1)).difference(elimination_set)

    def find_empty_square(self):
        item_size = self.size * self.size
        for i in range(item_size):
            x, y = i % self.size, i // self.size
            if self.board[y][x] == 0:
                return (x, y)
        return None

    def backtrack(self):
        if self.is_solved():
            return True
        empty_square = self.find_empty_square()
        if empty_square:   
            x, y = empty_square
            for choice in self.possible_choices(x, y):
                self.board[y][x] = choice
                if self.is_consistent() and self.backtrack():
                    return True
            self.board[y][x] = 0
        return False


board_arr = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
             [5, 2, 0, 0, 0, 0, 0, 0, 0],
             [0, 8, 7, 0, 0, 0, 0, 3, 1],
             [0, 0, 3, 0, 1, 0, 0, 8, 0],
             [9, 0, 0, 8, 6, 3, 0, 0, 5],
             [0, 5, 0, 0, 9, 0, 6, 0, 0],
             [1, 3, 0, 0, 0, 0, 2, 5, 0],
             [0, 0, 0, 0, 0, 0, 0, 7, 4],
             [0, 0, 5, 2, 0, 6, 3, 0, 0], ]

solved_board_arr = [[3, 1, 6, 5, 7, 8, 4, 9, 2],
                    [5, 2, 9, 1, 3, 4, 7, 6, 8],
                    [4, 8, 7, 6, 2, 9, 5, 3, 1],
                    [2, 6, 3, 4, 1, 5, 9, 8, 7],
                    [9, 7, 4, 8, 6, 3, 1, 2, 5],
                    [8, 5, 1, 7, 9, 2, 6, 4, 3],
                    [1, 3, 8, 9, 4, 7, 2, 5, 6],
                    [6, 9, 2, 3, 5, 1, 8, 7, 4],
                    [7, 4, 5, 2, 8, 6, 3, 1, 9], ]

board = Board(board_arr)
if board.backtrack():
    board.print_board()
else:
    print("Cannot be solved")