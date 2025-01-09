from rich.console import Console
from rich.table import Table
import keyboard
import concurrent.futures

class Problem:
    def __init__(self):
        self.console = Console()
        self.board_state = [str(i + 1) for i in range(64)]  # Khởi tạo trạng thái bảng để hiển thị
        self.board_state_back_end = [' ' for _ in  range(64)]  # Khởi tạo trạng thái bảng cho thuật toán

    def tic_tac_toe_table(self):
        table = Table(title="Tic-Tac-Toe-8x8", show_header=False, show_lines=True, row_styles=['none'])
        for i in range(8):
            table.add_column(str(i+1), justify="right", style="cyan", no_wrap=True)
        for i in range(8):
            start_index = 8 * i
            # Tạo một danh sách mới chứa c ác ô được định dạng màu sắc
            styled_cells = []
            for j in range(8):
                cell_content = self.board_state[start_index + j]
                if cell_content == "X":
                    styled_cells.append(f"[bold red]{cell_content}[/bold red]")
                elif cell_content == "O":
                    styled_cells.append(f"[bold yellow]{cell_content}[/bold yellow]")
                else:
                    styled_cells.append(f"[cyan]{cell_content}[/cyan]")
            # Thêm hàng với các ô đã được định dạng
            table.add_row(*styled_cells) 

        self.console.clear()
        self.console.print(table)

    def update_board(self, position, player_symbol):
        index = position - 1
        if 0 <= index < 64 and self.board_state_back_end[index] not in ['X', 'O']:
            self.board_state_back_end[index] = player_symbol
            self.board_state[index] = player_symbol  # Cập nhật hiển thị cho người dùng
            return True
        return False

    def check_win(self, board):
        # Kiểm tra hàng ngang
        for row in range(8):
            for col in range(5):
                if board[row * 8 + col] == board[row * 8 + col + 1] == board[row * 8 + col + 2] == board[row * 8 + col + 3] != ' ':
                    return board[row * 8 + col]

        # Kiểm tra hàng dọc
        for col in range(8):
            for row in range(5):
                if board[row * 8 + col] == board[(row + 1) * 8 + col] == board[(row + 2) * 8 + col] == board[(row + 3) * 8 + col] != ' ':
                    return board[row * 8 + col]

        # Kiểm tra đường chéo chính
        for row in range(5):
            for col in range(5):
                if board[row * 8 + col] == board[(row + 1) * 8 + col + 1] == board[(row + 2) * 8 + col + 2] == board[(row + 3) * 8 + col + 3] != ' ':
                    return board[row * 8 + col]

        # Kiểm tra đường chéo phụ
        for row in range(5):
            for col in range(3, 8):
                if board[row * 8 + col] == board[(row + 1) * 8 + col - 1] == board[(row + 2) * 8 + col - 2] == board[(row + 3) * 8 + col - 3] != ' ':
                    return board[row * 8 + col]

        return None

    def line_score(self, line, player, opponent):
        score = 0
        if line.count(player) == 4:
            score += 100
        elif line.count(player) == 3 and line.count(' ') == 1:
            score += 10
        elif line.count(player) == 2 and line.count(' ') == 2:
            score += 1

        if line.count(opponent) == 4:
            score -= 100
        elif line.count(opponent) == 3 and line.count(' ') == 1:
            score -= 50  # Tăng điểm để chặn đối thủ
        elif line.count(opponent) == 2 and line.count(' ') == 2:
            score -= 5  # Tăng điểm để chặn đối thủ

        return score

    def evaluate(self, board):
        winner = self.check_win(board)
        if winner == 'O':
            return 100
        elif winner == 'X':
            return -100
        
        score = 0
        for row in range(8):
            for col in range(5):
                line = board[row * 8 + col:row * 8 + col + 4]
                score += self.line_score(line, 'O', 'X')

        for col in range(8):
            for row in range(5):
                line = [board[row * 8 + col], board[(row + 1) * 8 + col], board[(row + 2) * 8 + col], board[(row + 3) * 8 + col]]
                score += self.line_score(line, 'O', 'X')

        for row in range(5):
            for col in range(5):
                line = [board[row * 8 + col], board[(row + 1) * 8 + col + 1], board[(row + 2) * 8 + col + 2], board[(row + 3) * 8 + col + 3]]
                score += self.line_score(line, 'O', 'X')

        for row in range(5):
            for col in range(3, 8):
                line = [board[row * 8 + col], board[(row + 1) * 8 + col - 1], board[(row + 2) * 8 + col - 2], board[(row + 3) * 8 + col - 3]]
                score += self.line_score(line, 'O', 'X')

        return score

class Search_Strategy:
    def __init__(self, problem):
        self.problem = problem
        self.transposition_table = {}  # Bảng ghi nhớ
        self.first_move = True 

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        board_tuple = tuple(board)
        if board_tuple in self.transposition_table:
            return self.transposition_table[board_tuple]

        result = self.problem.check_win(board)
        if depth == 0 or result is not None:
            evaluation = self.problem.evaluate(board)
            self.transposition_table[board_tuple] = evaluation
            return evaluation

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_ordered_moves(board, 'O'):
                board[move] = 'O'
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board[move] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.transposition_table[board_tuple] = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_ordered_moves(board, 'X'):
                board[move] = 'X'
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board[move] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.transposition_table[board_tuple] = min_eval
            return min_eval

    def parallel_minimax(self, board, depth, maximizing_player):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for move in self.get_ordered_moves(board, 'O' if maximizing_player else 'X'):
                board[move] = 'O' if maximizing_player else 'X'
                futures.append(executor.submit(self.minimax, board.copy(), depth - 1, float('-inf'), float('inf'), not maximizing_player))
                board[move] = ' '
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        return max(results) if maximizing_player else min(results)

    def iterative_deepening(self, board, max_depth, maximizing_player):
        best_move = None
        for depth in range(1, max_depth + 1):
            best_move = self.find_best_move_at_depth(board, depth, maximizing_player)
        return best_move

    def find_best_move_at_depth(self, board, depth, maximizing_player):
        best_val = float('-inf')
        best_move = -1

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {}
            for move in self.get_ordered_moves(board, 'O' if maximizing_player else 'X'):
                board[move] = 'O' if maximizing_player else 'X'
                future = executor.submit(self.minimax, board.copy(), depth - 1, float('-inf'), float('inf'), not maximizing_player)
                futures[future] = move
                board[move] = ' '
            for future in concurrent.futures.as_completed(futures):
                move_val = future.result()
                if move_val > best_val:
                    best_val = move_val
                    best_move = futures[future]
        return best_move

    def get_ordered_moves(self, board, player):
        moves = [i for i in range(64) if board[i] == ' ']
        opponent = 'X' if player == 'O' else 'O'
        center_moves = [27, 28, 35, 36]
        moves.sort(key=lambda x: x in center_moves, reverse=True)
        moves.sort(key=lambda x: sum([board[x + dx] == player for dx in [-1, 1, -8, 8] if 0 <= x + dx < 64]), reverse=True)
        moves.sort(key=lambda x: sum([board[x + dx] == opponent for dx in [-1, 1, -8, 8] if 0 <= x + dx < 64]), reverse=True)
        return moves

    # def find_nearest_to_x(self, board):
    #     opponent = 'X'
    #     moves = [i for i in range(64) if board[i] == ' ']

    #     def distance_from_opponent(move):
    #         distances = [abs(move % 8 - pos % 8) + abs(move // 8 - pos // 8) for pos in range(64) if board[pos] == opponent]
    #         return min(distances) if distances else float('inf')

    #     moves.sort(key=lambda x: distance_from_opponent(x))
    #     return moves[0] if moves else None
    def find_nearest_to_x(self, board):
        opponent = 'X'
        moves = [i for i in range(64) if board[i] == ' ']

        def distance_from_opponent(move):
            distances_straight = [abs(move % 8 - pos % 8) + abs(move // 8 - pos // 8) for pos in range(64) if board[pos] == opponent]
            distances_diagonal = [max(abs(move % 8 - pos % 8), abs(move // 8 - pos // 8)) for pos in range(64) if board[pos] == opponent]

            if distances_straight and distances_diagonal:
                min_distance_straight = min(distances_straight)
                min_distance_diagonal = min(distances_diagonal)
                return min(min_distance_straight, min_distance_diagonal)
            elif distances_straight:
                return min(distances_straight)
            elif distances_diagonal:
                return min(distances_diagonal)
            else:
                return float('inf')

        moves.sort(key=lambda x: distance_from_opponent(x))
        return moves[0] if moves else None


    def find_best_move(self, board):
        if self.first_move:
            self.first_move = False
            return self.find_nearest_to_x(board)
        return self.iterative_deepening(board, 3, True)

if __name__ == "__main__":
    problem = Problem()
    search_strategy = Search_Strategy(problem)
    current_player = 'X'
    input_number = ""
    ai_moved = 0
    # current_player.append(input_move)


    while True:
        problem.tic_tac_toe_table()
        if current_player == 'X':
            if ai_moved != 0:
                problem.console.print(f"AI moved: {ai_moved}", style="bold yellow")
            problem.console.print("You're moving...", style="bold yellow")
            if input_number:
                problem.console.print(f"Current Player: {current_player}", style="bold green")
                problem.console.print(f"Player: {input_number}", style="bold green")
            key = keyboard.read_event()
            if key.event_type == keyboard.KEY_DOWN:
                if key.name.isdigit():
                    input_number += key.name
                elif key.name == 'enter' and input_number:
                    if problem.update_board(int(input_number), current_player):
                        winner = problem.check_win(problem.board_state_back_end)
                        if winner:
                            problem.console.print(f"Player {winner} wins!", style="bold green")
                            break
                        current_player = 'O'
                        input_number = ''
                        ai_moved = 0
                    else:
                        problem.console.print("Invalid move, try again!", style="bold red")
                elif key.name == 'backspace' and input_number:
                    input_number = input_number[:-1]
                elif key.name == 'esc':
                    break
        else:
            problem.console.print(f"AI is moving...", style="bold yellow")
            best_move = search_strategy.find_best_move(problem.board_state_back_end)
            ai_moved = best_move + 1
            problem.update_board(best_move + 1, 'O')
            winner = problem.check_win(problem.board_state_back_end)
            if winner:
                problem.tic_tac_toe_table()
                problem.console.print(f"Player {winner} wins!", style="bold green")
                break
            current_player = 'X'