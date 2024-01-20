from ctypes import cdll, c_char_p


def response(board):
    lib = cdll.LoadLibrary('./AI/ai.so')
    lib.ai.argtypes = [c_char_p]
    lib.ai.restype = int
    t = lib.ai(board.encode('utf-8'))
    return t / 8, t % 8
