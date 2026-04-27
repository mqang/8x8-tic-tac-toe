from board import BOARD_CELLS, BOARD_SIZE, CENTER_MOVES, WIN_LENGTH


class Search_Strategy:
    def __init__(self, problem):
        self.problem = problem
        self.transposition_table = {}  # Bảng ghi nhớ
        self.first_move = True
        self.max_depth = 4
        self.max_candidates = 10
        self.candidate_radius = 2

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        result = self.problem.check_win(board)
        if result == 'O':
            return 100_000 + depth
        if result == 'X':
            return -100_000 - depth
        if depth == 0 or ' ' not in board:
            return self.problem.evaluate(board)

        board_tuple = tuple(board)
        tt_key = (board_tuple, depth, maximizing_player)
        if tt_key in self.transposition_table:
            return self.transposition_table[tt_key]

        if maximizing_player:
            max_eval = float('-inf')
            cutoff = False
            for move in self.get_ordered_moves(board, 'O', self.max_candidates):
                board[move] = 'O'
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board[move] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    cutoff = True
                    break
            if not cutoff:
                self.transposition_table[tt_key] = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            cutoff = False
            for move in self.get_ordered_moves(board, 'X', self.max_candidates):
                board[move] = 'X'
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board[move] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    cutoff = True
                    break
            if not cutoff:
                self.transposition_table[tt_key] = min_eval
            return min_eval

    def iterative_deepening(self, board, max_depth, maximizing_player):
        best_move = None
        for depth in range(1, max_depth + 1):
            current_best_move = self.find_best_move_at_depth(board, depth, maximizing_player)
            if current_best_move is not None:
                best_move = current_best_move
        return best_move

    def find_best_move_at_depth(self, board, depth, maximizing_player):
        moves = self.get_ordered_moves(board, 'O' if maximizing_player else 'X', self.max_candidates + 6)
        if not moves:
            return None

        if maximizing_player:
            best_val = float('-inf')
            best_move = -1
            for move in moves:
                board[move] = 'O'
                move_val = self.minimax(board, depth - 1, float('-inf'), float('inf'), False)
                board[move] = ' '
                if move_val > best_val:
                    best_val = move_val
                    best_move = move
            return best_move

        best_val = float('inf')
        best_move = -1
        for move in moves:
            board[move] = 'X'
            move_val = self.minimax(board, depth - 1, float('-inf'), float('inf'), True)
            board[move] = ' '
            if move_val < best_val:
                best_val = move_val
                best_move = move
        return best_move

    def candidate_moves(self, board, player):
        occupied = [index for index, value in enumerate(board) if value != ' ']
        if not occupied:
            return [move for move in CENTER_MOVES if board[move] == ' ']

        opponent = 'X' if player == 'O' else 'O'
        candidates = set()

        for index in occupied:
            row, col = divmod(index, BOARD_SIZE)
            for row_delta in range(-self.candidate_radius, self.candidate_radius + 1):
                for col_delta in range(-self.candidate_radius, self.candidate_radius + 1):
                    next_row = row + row_delta
                    next_col = col + col_delta
                    if 0 <= next_row < BOARD_SIZE and 0 <= next_col < BOARD_SIZE:
                        move = next_row * BOARD_SIZE + next_col
                        if board[move] == ' ':
                            candidates.add(move)

        for move in CENTER_MOVES:
            if board[move] == ' ':
                candidates.add(move)

        candidates.update(self.problem.winning_moves(board, player))
        candidates.update(self.problem.winning_moves(board, opponent))

        for indexes in self.problem.winning_lines():
            line = [board[index] for index in indexes]
            player_count = line.count(player)
            opponent_count = line.count(opponent)
            if opponent_count == 0 and player_count >= 2:
                candidates.update(index for index in indexes if board[index] == ' ')
            if player_count == 0 and opponent_count >= 2:
                candidates.update(index for index in indexes if board[index] == ' ')

        return list(candidates)

    def get_ordered_moves(self, board, player, limit=None):
        moves = self.candidate_moves(board, player)
        opponent = 'X' if player == 'O' else 'O'
        opponent_winning_moves = set(self.problem.winning_moves(board, opponent))

        def orthogonal_neighbors(index):
            row, col = divmod(index, BOARD_SIZE)
            neighbors = []
            if col > 0:
                neighbors.append(index - 1)
            if col < BOARD_SIZE - 1:
                neighbors.append(index + 1)
            if row > 0:
                neighbors.append(index - BOARD_SIZE)
            if row < BOARD_SIZE - 1:
                neighbors.append(index + BOARD_SIZE)
            return neighbors

        def all_neighbors(index):
            row, col = divmod(index, BOARD_SIZE)
            neighbors = []
            for row_delta in (-1, 0, 1):
                for col_delta in (-1, 0, 1):
                    if row_delta == 0 and col_delta == 0:
                        continue
                    next_row = row + row_delta
                    next_col = col + col_delta
                    if 0 <= next_row < BOARD_SIZE and 0 <= next_col < BOARD_SIZE:
                        neighbors.append(next_row * BOARD_SIZE + next_col)
            return neighbors

        def move_priority(move):
            board[move] = player
            winner = self.problem.check_win(board)
            created_threats = self.count_local_direct_threats(board, move, player)
            line_score = self.local_line_score(board, move, player, opponent)
            board[move] = ' '

            neighbors = all_neighbors(move)
            orthogonal = orthogonal_neighbors(move)
            opponent_adjacent = sum(board[n] == opponent for n in neighbors)
            player_adjacent = sum(board[n] == player for n in neighbors)
            orthogonal_adjacent = sum(board[n] != ' ' for n in orthogonal)
            center_bonus = 3 if move in CENTER_MOVES else 0
            return (
                winner == player,
                move in opponent_winning_moves,
                created_threats,
                line_score,
                player_adjacent,
                opponent_adjacent,
                orthogonal_adjacent,
                center_bonus,
            )

        moves.sort(key=move_priority, reverse=True)
        if limit is not None:
            return moves[:limit]
        return moves

    def find_best_move(self, board):
        self.transposition_table.clear()
        self.first_move = False

        winning_moves = self.problem.winning_moves(board, 'O')
        if winning_moves:
            return self.get_ordered_moves_for_subset(board, 'O', winning_moves)[0]

        blocking_moves = self.problem.winning_moves(board, 'X')
        if blocking_moves:
            return self.get_ordered_moves_for_subset(board, 'O', blocking_moves)[0]

        attacking_threats = self.moves_that_create_direct_threat(board, 'O')
        if attacking_threats:
            return self.get_ordered_moves_for_subset(board, 'O', attacking_threats)[0]

        defensive_threats = self.moves_that_create_direct_threat(board, 'X')
        if defensive_threats:
            return self.get_ordered_moves_for_subset(board, 'O', defensive_threats)[0]

        occupied_count = sum(value != ' ' for value in board)
        if occupied_count <= 1:
            center_choices = [move for move in CENTER_MOVES if board[move] == ' ']
            if center_choices:
                return min(center_choices, key=lambda move: (self.center_distance(move), move))

        return self.iterative_deepening(board, self.max_depth, True)

    def center_distance(self, move):
        row, col = divmod(move, BOARD_SIZE)
        return abs(row - 3.5) + abs(col - 3.5)

    def get_ordered_moves_for_subset(self, board, player, moves):
        ordered_moves = self.get_ordered_moves(board, player)
        move_set = set(moves)
        return [move for move in ordered_moves if move in move_set]

    def moves_that_create_direct_threat(self, board, player):
        moves = []
        for move in self.candidate_moves(board, player):
            board[move] = player
            if self.problem.winning_moves(board, player):
                moves.append(move)
            board[move] = ' '
        return moves

    def count_local_direct_threats(self, board, move, player):
        threats = 0
        for line in self.problem._lines_by_cell[move]:
            values = [board[index] for index in line]
            if values.count(player) == WIN_LENGTH - 1 and values.count(' ') == 1:
                threats += 1
        return threats

    def local_line_score(self, board, move, player, opponent):
        score = 0
        for line in self.problem._lines_by_cell[move]:
            values = [board[index] for index in line]
            if values.count(player) > 0 and values.count(opponent) > 0:
                continue
            player_count = values.count(player)
            opponent_count = values.count(opponent)
            empty_count = values.count(' ')
            if player_count == 3 and empty_count == 1:
                score += 900
            elif player_count == 2 and empty_count == 2:
                score += 70
            elif player_count == 1 and empty_count == 3:
                score += 3
            if opponent_count == 3 and empty_count == 1:
                score -= 1_200
            elif opponent_count == 2 and empty_count == 2:
                score -= 90
            elif opponent_count == 1 and empty_count == 3:
                score -= 4
        return score if player == 'O' else -score
