# -*- coding: utf-8 -*-

import curses
import sys
import argparse
from queue import Queue


class Window:
	def __init__(self, n_rows, n_cols, row = 0, col = 0):
		self.n_rows = n_rows
		self.n_cols = n_cols
		self.row = row
		self.col = col

	@property
	def bottom(self):
		return self.row + self.n_rows - 1

	def up(self, cursor):
		if cursor.row == self.row - 1 and self.row > 0:
			self.row -= 1

	def down(self, buffer, cursor):
		if cursor.row == self.bottom + 1 and self.bottom < buffer.bottom:
			self.row += 1

	def translate(self, cursor):
		return cursor.row - self.row, cursor.col - self.col

	def horizontal_scroll(self, cursor, left_margin = 5, right_margin = 2):
		n_pages = cursor.col // (self.n_cols - right_margin)
		self.col = max(n_pages * self.n_cols - right_margin - left_margin, 0)

class Cursor:
	def __init__(self, row = 0, col = 0, col_hint = None):
		self.row = row
		self._col = col
		self._col_hint = col if col_hint is None else col_hint

	@property
	def col(self):
		return self._col

	@col.setter
	def col(self, col):
		self._col = col
		self._col_hint = col

	def up(self, buffer):
		if self.row > 0:
			self.row -= 1
			self._clamp_col(buffer)

	def down(self, buffer):
		if self.row < buffer.bottom:
			self.row += 1
			self._clamp_col(buffer)

	def left(self, buffer):
		if self.col > 0:
			self.col -= 1
		elif self.row > 0:
			self.row -= 1
			self.col = len(buffer[self.row])

	def right(self, buffer):
		if self.col < len(buffer[self.row]):
			self.col += 1
		elif self.row < buffer.bottom:
			self.row += 1
			self.col = 0

	def _clamp_col(self, buffer):
		self._col = min(self._col_hint, len(buffer[self.row]))

class Buffer:
	def __init__(self, lines):
		self.lines = lines

	def __len__(self):
		return len(self.lines)

	def __getitem__(self, index):
		return self.lines[index]

	@property
	def bottom(self):
		return len(self) - 1

	def insert(self, cursor, string):
		row, col = cursor.row, cursor.col
		if len(self.lines) == 0:
			self.lines.append("")
			self.lines[row] += string
		else:
			current = self.lines.pop(row)
			new = current[:col] + string + current[col:]
			self.lines.insert(row, new)

	def split(self, cursor):
		row, col = cursor.row, cursor.col
		current = self.lines.pop(row)
		self.lines.insert(row, current[:col])
		#self.lines[row] += "\n"
		self.lines.insert(row + 1, current[col:])

	def delete(self, cursor):
		row, col = cursor.row, cursor.col
		if (row, col) < (self.bottom, len(self[row])):
			current = self.lines.pop(row)
			if col < len(current):
				new = current[:col] + current[col + 1:]
				self.lines.insert(row, new)
			else:
				next = self.lines.pop(row)
				new = current + next
				self.lines.insert(row, new)


def right(window, buffer, cursor):
	cursor.right(buffer)
	window.down(buffer, cursor)
	window.horizontal_scroll(cursor)

def left(window, buffer, cursor):
	cursor.left(buffer)
	window.up(cursor)
	window.horizontal_scroll(cursor)

def main(stdscr, input_queue):

	with open("test.txt") as f:
		buffer = Buffer(f.read().splitlines())

	window = Window(curses.LINES - 1, curses.COLS - 1)
	cursor = Cursor()
	
	stdscr.nodelay(True)
	index = 0

	for i in range(len(buffer.lines)): 
		buffer.lines[i] += "\n"

	#import time
	#print("Debug buffer : ", buffer.lines)
	#time.sleep(2)
	
	while True:
		with open("test.txt") as f:
			buffer = Buffer(f.read().splitlines())
		window = Window(curses.LINES - 1, curses.COLS - 1)

		for i in range(len(buffer.lines)):
			buffer.lines[i] += "\n"
		stdscr.erase()
		
		for row, line in enumerate(buffer[window.row : window.row + window.n_rows]):
			if row == cursor.row - window.row and window.col > 0:
				line = "<<" + line[window.col + 1:]
			if len(line) > window.n_cols:
				line = line[:window.n_cols - 1] + ">>"
			stdscr.addstr(row, 0, line)
		stdscr.move(*window.translate(cursor))

		try:
			k = stdscr.getkey()
		except:
			continue

		if k == "KEY_F(8)":
			sys.exit(0)
		elif k == "KEY_UP":
			cursor.up(buffer)
			window.up(cursor)
			window.horizontal_scroll(cursor)
			index = 0
			for i in range(cursor.row):
				index += len(buffer.lines[i])
				index += 1
			index += cursor.col
			#if cursor.row != 0 and cursor.col <= len(buffer.lines[cursor.row - 1]):
			#	index -= len(buffer.lines[cursor.row - 1])
			#elif cursor.row != 0 and cursor.col > len(buffer.lines[cursor.row - 1]):
			#	index -= cursor.col
		elif k == "KEY_DOWN":
			cursor.down(buffer)
			window.down(buffer, cursor)
			window.horizontal_scroll(cursor)
			index = 0
			for i in range(cursor.row):
				index += len(buffer.lines[i])
				index += 1
			index += cursor.col
			#if cursor.row < buffer.bottom and cursor.col <= len(buffer.lines[cursor.row + 1]):
			#	index += len(buffer.lines[cursor.row])
			#elif cursor.row < buffer.bottom and cursor.col > len(buffer.lines[cursor.row + 1]):
			#	index = index + len(buffer.lines[cursor.row]) + len(buffer.lines[cursor.row + 1]) - cursor.col
		elif k == "KEY_LEFT":
			#cursor.left(buffer)
			#window.up(cursor)
			#window.horizontal_scroll(cursor)
			left(window, buffer, cursor)
			index -= 1
		elif k == "KEY_RIGHT":
			#cursor.right(buffer)
			#window.down(buffer, cursor)
			#window.horizontal_scroll(cursor)
			right(window, buffer, cursor)
			index += 1
		elif k == "\n":
			#for i in range(cursor.row):
			#	index += len(buffer.lines[i])
			#index += cursor.col
			input_queue.put(["I", index, k])
			index += 1
			buffer.split(cursor)
			right(window, buffer, cursor)
			#right(window, buffer, cursor)
		elif k in ("KEY_DELETE", "\x04", "KEY_DC"):
			buffer.delete(cursor)
			input_queue.put(["D", index])
		elif k in ("KEY_BACKSPACE", "\x7f"):
			if (cursor.row, cursor.col) > (0, 0):
				left(window, buffer, cursor)
				index -= 1
				buffer.delete(cursor)
			input_queue.put(["D", index])
			#index -= 1
		else:
			buffer.insert(cursor, k)
			for _ in k:
				right(window, buffer, cursor)
			input_queue.put(["I", index, k])
			index += 1

if __name__ == "__main__":
	input_queue = Queue()
	curses.wrapper(main, input_queue)
