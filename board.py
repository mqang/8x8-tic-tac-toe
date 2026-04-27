from rich.console import Console
from rich.table import Table

BOARD_SIZE = 8
WIN_LENGTH = 4
BOARD_CELLS = BOARD_SIZE * BOARD_SIZE
CENTER_MOVES = {27, 28, 35, 36}


class Problem:
    def __init__(self):
        self.console = Console()
        self._winning_lines = list(self.generate_winning_lines())
        self._lines_by_cell = [[] for _ in range(BOARD_CELLS)]
        for line in self._winning_lines:
            for index in line:
                self._lines_by_cell[index].append(line)
        self.board_state = [str(i + 1) for i in range(BOARD_CELLS)]  # Khởi tạo trạng thái bảng để hiển thị
        self.board_state_back_end = [' ' for _ in  range(BOARD_CELLS)]  # Khởi tạo trạng thái bảng cho thuật toán

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
        if 0 <= index < BOARD_CELLS and self.board_state_back_end[index] not in ['X', 'O']:
            self.board_state_back_end[index] = player_symbol
            self.board_state[index] = player_symbol  # Cập nhật hiển thị cho người dùng
            return True
        return False

    def generate_winning_lines(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE - WIN_LENGTH + 1):
                start = row * BOARD_SIZE + col
                yield tuple(start + offset for offset in range(WIN_LENGTH))

        for col in range(BOARD_SIZE):
            for row in range(BOARD_SIZE - WIN_LENGTH + 1):
                start = row * BOARD_SIZE + col
                yield tuple(start + offset * BOARD_SIZE for offset in range(WIN_LENGTH))

        for row in range(BOARD_SIZE - WIN_LENGTH + 1):
            for col in range(BOARD_SIZE - WIN_LENGTH + 1):
                start = row * BOARD_SIZE + col
                yield tuple(start + offset * (BOARD_SIZE + 1) for offset in range(WIN_LENGTH))

        for row in range(BOARD_SIZE - WIN_LENGTH + 1):
            for col in range(WIN_LENGTH - 1, BOARD_SIZE):
                start = row * BOARD_SIZE + col
                yield tuple(start + offset * (BOARD_SIZE - 1) for offset in range(WIN_LENGTH))

    def winning_lines(self):
        return self._winning_lines

    def winning_moves(self, board, player):
        moves = []
        for move in range(BOARD_CELLS):
            if board[move] != ' ':
                continue
            if any(all(index == move or board[index] == player for index in line) for line in self._lines_by_cell[move]):
                moves.append(move)
        return moves

    def check_win(self, board):
        winning_line = self.find_winning_line(board)
        if winning_line is not None:
            return board[winning_line[0]]
        return None

    def find_winning_line(self, board):
        for line in self.winning_lines():
            first = board[line[0]]
            if first != ' ' and all(board[index] == first for index in line[1:]):
                return line
        return None

    def line_score(self, line, player, opponent):
        player_count = line.count(player)
        opponent_count = line.count(opponent)
        empty_count = line.count(' ')

        # Dòng đã bị chặn hai đầu thì không còn giá trị chiến lược.
        if player_count > 0 and opponent_count > 0:
            return 0

        if player_count == 3 and empty_count == 1:
            return 900
        if player_count == 2 and empty_count == 2:
            return 70
        if player_count == 1 and empty_count == 3:
            return 3

        if opponent_count == 3 and empty_count == 1:
            return -1_200
        if opponent_count == 2 and empty_count == 2:
            return -90
        if opponent_count == 1 and empty_count == 3:
            return -4

        return 0

    def evaluate(self, board):
        winner = self.check_win(board)
        if winner == 'O':
            return 100_000
        elif winner == 'X':
            return -100_000

        score = 0
        for indexes in self.winning_lines():
            line = [board[index] for index in indexes]
            score += self.line_score(line, 'O', 'X')

        score += 2_500 * len(self.winning_moves(board, 'O'))
        score -= 3_000 * len(self.winning_moves(board, 'X'))

        for index, value in enumerate(board):
            if value == ' ':
                continue
            row, col = divmod(index, BOARD_SIZE)
            center_distance = abs(row - 3.5) + abs(col - 3.5)
            center_score = int(20 - center_distance * 3)
            score += center_score if value == 'O' else -center_score

        return score
