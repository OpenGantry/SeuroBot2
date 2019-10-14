#!/usr/bin/env python

import curses

# ./q-curses.py

stdscr = curses.initscr()

curses.noecho()
curses.cbreak()

stdscr.addstr(2, 0, "Press ESC to end")

stdscr.addstr(10, 0, "Hello")
stdscr.addstr(12, 0, "World!")

stdscr.nodelay(1)

count=1

while True:

   stdscr.addstr(14, 12, str(count) + ' ')
   count += 1

   stdscr.refresh()
   time.sleep(0.04)

   c = stdscr.getch()

   if c != -1:
      if c == 27:
          break
      stdscr.addstr(16, 12, str(c) + '   ')

curses.nocbreak()
curses.echo()
curses.endwin()