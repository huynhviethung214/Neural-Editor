# # ACTIONS = ['+', '-', '*', '/', '%']
# #          E1  E2 F1 F2 1->2 2->1 (E = empty & F = fill)
# ACTIONS = [-1, -2, 1, 2, 3, 4]
# STACK = []
# QUEUE = []
# VISITED = []
#
# MAX_A = 9
# MAX_B = 5
# GOAL = 6
#
#
# class BreakRecursion(Exception):
#     def __init__(self):
#         super(BreakRecursion, self).__init__()
#
#
# class Node:
#     def __init__(self, state, action):
#         # state: (a, b)
#         self.a = state[0]
#         self.b = state[1]
#         self.action = action
#
#     # Return new state
#     def take_action(self) -> [int, int]:
#         if self.action == -1:
#             return 0, self.b
#
#         elif self.action == -2:
#             return self.a, 0
#
#         elif self.action == 1:
#             if self.a < MAX_A:
#                 return MAX_A, self.b
#
#         elif self.action == 2:
#             if self.b < MAX_B:
#                 return self.a, MAX_B
#
#         elif self.action == 3:
#             if self.a + self.b <= MAX_B:
#                 return 0, self.a + self.b
#             else:
#                 b_amount_until_fill = MAX_B - self.b
#                 fill_amount = self.a - b_amount_until_fill
#                 return fill_amount, MAX_B
#
#         elif self.action == 4:
#             if self.a + self.b <= MAX_A:
#                 return self.a + self.b, 0
#             else:
#                 a_amount_until_fill = MAX_A - self.a
#                 fill_amount = self.b - a_amount_until_fill
#                 return MAX_A, fill_amount
#         return self.a, self.b
#
#
# def find_formula(state):
#     STACK.append(state)
#
#     while STACK:
#         current_state = STACK.pop(0)
#         VISITED.append(current_state)
#
#         for action in ACTIONS:
#             new_state = Node(current_state, action).take_action()
#
#             if new_state[0] == GOAL or new_state[1] == GOAL:
#                 print(f'\nSolution Found! {new_state}')
#                 VISITED.append(new_state)
#                 print(f'Solution Path: {VISITED} With Length {len(VISITED)}')
#                 return
#
#             if new_state not in VISITED:
#                 STACK.insert(0, new_state)
#                 print(f'New State {new_state}')
#
#
# try:
#     find_formula((0, 0))
# except RecursionError:
#     print('No Solution(s)!')

a = []
a.insert(0, 1)
a.insert(3, 4)
a.insert(2, 9)
a.insert(1, 8)
print(a)