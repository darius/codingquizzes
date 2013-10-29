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
0 <=  cursor   <= (buffer_length - 1)

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
        self.gap_buffer = list('#'*BUFF_LENGTH)
        self.right_buffer = deque(text)

    def move_left(self):
        if self.cursor > 0:
            self.right_buffer.appendleft(self.gap_buffer[self.cursor - 1])
            self.cursor -= 1 
        else:
            try:
                self.right_buffer.appendleft(self.left_buffer.pop())
            except:
                print('\a')

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
            self.cursor = max(self.cursor, self.cursor)
        else:
            self.left_buffer.extend(''.join(self.gap_buffer))
            self.gap_buffer[0] = char
            self.cursor = 1

    def delete_before(self):
        if self.cursor == 0:
            try:
                self.left_buffer.pop()
            except:
                print('\a')
        else:
            self.cursor -= 1  

             
    def save(self):
        text = ''.join(self.left_buffer) + ''.join(self.gap_buffer[:self.cursor]) + ''.join(self.right_buffer)
        return text

    def show(self):
        print '[' + ''.join(self.left_buffer) + ']' +\
              '[' + ''.join(self.gap_buffer[:self.cursor]) +\
              '\033[91m' + ''.join(self.gap_buffer[self.cursor:]) +\
              '\033[0m' + ']' +\
              '[' + ''.join(self.right_buffer) + ']' + '  cursor:' + str(self.cursor)


#Test
# foo456 -> foobar456 -> foo123bar456
# including attempts at empty moves

def put_string_after(string, gap_buffer):
    print "\ninsert word \"%s\" after the cursor:" % string
    for char in string:
        gap_buffer.insert_after(char)
        gap_buffer.show()

t = "foo456"

print "========================"
b = GapBuffer(t)
b.show()
print "========================"
[b.move_right() for i in range(3)]
print "\nmove right three positions:"
b.show()

put_string_after("bar", b)
 
[b.move_left() for i in range(7)]
print "\nmove left 7 positions (last move empty):"
b.show()

[b.move_right() for i in range(3)]
print "\nmove right three positions:"
b.show()

put_string_after("123", b)

print "========================"
t = b.save()
print t

[b.move_right() for i in range(8)]
print "\nmove right 8 positions:"
b.show()

print "\ndelete 6 chars before the cursor:"
for i in range(6):
    b.delete_before()
    b.show()

print "========================"
t = b.save()
print t
