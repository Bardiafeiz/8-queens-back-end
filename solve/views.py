from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import random
from copy import deepcopy


class Queen:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.char = '♕'

    def __str__(self):
        return f"row: {self.row}\ncolumn: {self.column}\nchar: {self.char}"


def objective_function(queens):
    h = 0
    threat_pairs = []

    for i in range(len(queens)):
        for j in range(i + 1, len(queens)):
            # Checking horizontal threats
            if queens[i].row == queens[j].row:
                h += 1
                threat_pairs.append((i, j))

            # checking diagonal threats
            if abs(queens[i].row - queens[j].row) == abs(queens[i].column - queens[j].column):
                h += 1
                threat_pairs.append((i, j))

    return h, threat_pairs


def board_state(queens):
    state = ''
    queens_states = [(q.row, q.column) for q in queens]

    for i in range(8):
        for j in range(8):
            state += '♕' if (i, j) in queens_states else ' '
    print(state)
    return state


class ReactView(APIView):
    def get(self, request):
        rows = [i for i in range(8)]

        columns = [i for i in range(8)]
        random.shuffle(columns)

        queens = [Queen(random.choice(rows), columns.pop()) for _ in range(8)]

        old_h = objective_function(queens)[0]
        queen_to_move = 0
        row_to_move = queens[queen_to_move].row
        continue_bool = True
        counter = 0

        all_board_states = {}

        while continue_bool:
            counter += 1
            queens[queen_to_move].row = row_to_move

            all_board_states['key' + str(counter)] = board_state(queens)

            next_rows = []
            columns_h = []

            for col in range(8):
                queens_copy = deepcopy(queens)
                col_h = float('inf')
                dest_row = 0

                for row in range(8):
                    queens_copy[col].row = row
                    temp = objective_function(queens_copy)[0]
                    print(temp)

                    if temp < col_h:
                        col_h = temp
                        dest_row = row

                columns_h.append(col_h)
                next_rows.append(dest_row)

            new_h = min(columns_h)
            queen_to_move = columns_h.index(new_h)
            row_to_move = next_rows[queen_to_move]

            continue_bool = new_h < old_h
            old_h = new_h

        print(objective_function(queens))
        return Response(all_board_states)
