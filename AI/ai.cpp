#include <iostream>
#include <vector>

const int BOARD_SIZE = 8;
const char BLACK = 'B';
const char WHITE = 'W';
const char EMPTY = '-';

void initializeBoard(std::vector<std::vector<char>>& board) {
    for (int i = 0; i < BOARD_SIZE; ++i) {
        std::vector<char> row(BOARD_SIZE, EMPTY);
        board.push_back(row);
    }

    board[3][3] = WHITE;
    board[3][4] = BLACK;
    board[4][3] = BLACK;
    board[4][4] = WHITE;
}

void printBoard(const std::vector<std::vector<char>>& board) {
    for (int i = 0; i < BOARD_SIZE; ++i) {
        for (int j = 0; j < BOARD_SIZE; ++j) {
            std::cout << board[i][j] << " ";
        }
        std::cout << std::endl;
    }
}
// Function to check if a position is on the board
bool isOnBoard(int x, int y) {
    return x >= 0 && x < BOARD_SIZE && y >= 0 && y < BOARD_SIZE;
}

// Function to find valid moves
std::vector<std::pair<int, int>> findValidMoves(const std::vector<std::vector<char>>& board, char playerColor) {
    std::vector<std::pair<int, int>> validMoves;
    char opponentColor = (playerColor == BLACK) ? WHITE : BLACK;

    // Directions to check: (dx, dy)
    const int directions[8][2] = {{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}};

    for (int x = 0; x < BOARD_SIZE; ++x) {
        for (int y = 0; y < BOARD_SIZE; ++y) {
            if (board[x][y] != EMPTY) continue;

            for (const auto& dir : directions) {
                int dx = dir[0], dy = dir[1];
                int i = x + dx, j = y + dy;
                bool foundOpponent = false;

                while (isOnBoard(i, j) && board[i][j] == opponentColor) {
                    foundOpponent = true;
                    i += dx;
                    j += dy;
                }

                if (foundOpponent && isOnBoard(i, j) && board[i][j] == playerColor) {
                    validMoves.emplace_back(x, y);
                    break;
                }
            }
        }
    }

    return validMoves;
}
int main() {
    std::vector<std::vector<char>> board;
    initializeBoard(board);
    printBoard(board);

    // TODO: Implement game logic and AI

    return 0;
}