import time
import curses
import asyncio
from random import randint, choice

TIC_TIMEOUT = 0.1


async def blink(canvas, row, column, symbol='*'):
    animation_style = [curses.A_DIM, None, curses.A_BOLD, None]
    canvas.border()
    curses.curs_set(False)

    while True:
        for style in animation_style:
            if style:
                canvas.addstr(row, column, symbol, style)
            else:
                canvas.addstr(row, column, symbol)
            canvas.refresh()
            await asyncio.sleep(0)


def main():
    animation_scheme = [2, 0.3, 0.5, 0.3]
    stars = '+*.:'
    curses.update_lines_cols()

    window = curses.initscr()
    height, width = window.getmaxyx()
    coroutines = [curses.wrapper(blink, randint(1, height-2), randint(1, width-2), symbol=choice(stars)) for _ in range(10)]
    while True:
        for timeout in animation_scheme:
            for coroutine in coroutines:
                coroutine.send(None)
            time.sleep(timeout)


# animation_scheme = [2, 0.3, 0.5, 0.3]


if __name__ == '__main__':
    main()
