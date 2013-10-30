# -*- coding: utf-8 -*-
from collections import deque

'''
The GapBuffer has three parts:
a left and a right buffer holding text (a list and a deque), and a 
gap_buffer (a list) that initially contains garbage: '####'

when text is added inside the gap buffer, it keeps track of how many chars are stored
with self.cursor
cursor == 0 means all garbage, i.e.  '####'
cursor == 2, means two characters have now been filled with input, e.g.  'fo##'
(this is what must be saved from the buffer when saving the text)

INVARIANTS holding all the time:
0 <= cursor <= buffer_length

the size of the gap buffer is fixed:

-when the cursor moves across the left boundary,
the whole buffer gets shifted one character to the left.

-when the gap buffer is full and a char is inserted at the far right,
it overflows:
the whole gap buffer content gets pasted to the left buffer
and the gap buffer is then 'emptied' (the cursor is reset to 0).
'''

BUFF_LENGTH = 3

class GapBuffer(object):
    def __init__(self, text):
        self.cursor = 0
        
        self.left_buffer = []
        self.gap_buffer = ['#'] * BUFF_LENGTH
        self.right_buffer = deque(text)

    def move_left(self):
        if self.cursor > 0:
            self.right_buffer.appendleft(self.gap_buffer[self.cursor - 1])
            self.cursor -= 1 
        else:
            try:
                char = self.left_buffer.pop()
            except IndexError:
                print('\a')
            else:
                self.right_buffer.appendleft(char)

    def move_right(self):
        if self.cursor < BUFF_LENGTH:
            self.gap_buffer[self.cursor] = self.right_buffer.popleft()
            self.cursor += 1
        else:
            self.left_buffer.extend(self.gap_buffer)
            self.cursor = 0

    def insert_after(self, char):
        if self.cursor < BUFF_LENGTH:
            self.gap_buffer[self.cursor] = char
            self.cursor += 1
        else:
            self.left_buffer.extend(self.gap_buffer)
            self.gap_buffer[0] = char
            self.cursor = 1

    def delete_before(self):
        if self.cursor == 0:
            try:
                self.left_buffer.pop()
            except IndexError:
                print('\a')
        else:
            self.cursor -= 1  

             
    def save(self):
        text = ''.join(self.left_buffer) + ''.join(self.gap_buffer[:self.cursor]) + ''.join(self.right_buffer)
        return text

    def show(self):
        print ('[' + ''.join(self.left_buffer) + ']' +
               '[' + ''.join(self.gap_buffer[:self.cursor]) +
               '\033[91m' + ''.join(self.gap_buffer[self.cursor:]) +
               '\033[0m' + ']' +
               '[' + ''.join(self.right_buffer) + ']' + '  cursor:' + str(self.cursor))


#Test
# foo456 -> foobar456 -> foo123bar456 -> foo123
# including attempts at empty moves

#helper functions for testing

def put_string_after_cursor(string, buffer):
    print "insert word \"%s\" after the cursor:" % string
    for char in string:
        buffer.insert_after(char)
        buffer.show()

def move_right(n, buffer):
    [buffer.move_right() for i in range(n)]
    print "move right %d chars:" % n
    buffer.show()

def move_left(n, buffer):
    [buffer.move_left() for i in range(n)]
    print "move left %d chars:" % n
    buffer.show()

# actual test

t = "foo456"
b = GapBuffer(t)
b.show()
print "========================"
move_right(3, b)
b.show()
put_string_after_cursor("bar", b)
move_left(7, b) 
move_right(3, b)
put_string_after_cursor("123", b)
move_right(8, b)
print "delete 6 chars before the cursor:"

for i in range(6):
    b.delete_before()
    b.show()

print "========================"
t = b.save()
print t
