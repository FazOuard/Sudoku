import sys , pygame as pg
import copy
from sudoku import solve_sudoku, is_valid
pg.init()
screen_size=750,750
screen=pg.display.set_mode(screen_size)
font=pg.font.SysFont("arial",60)
clock = pg.time.Clock()

initial_puzzle = [
        [5,3,-1,-1,7,-1,-1,-1,-1],
        [6,-1,-1,1,9,5,-1,-1,-1],
        [-1,9,8,-1,-1,-1,-1,6,-1],
        [8,-1,-1,-1,6,-1,-1,-1,3],
        [4,-1,-1,8,-1,3,-1,-1,1],
        [7,-1,-1,-1,2,-1,-1,-1,6],
        [-1,6,-1,-1,-1,-1,2,8,-1],
        [-1,-1,-1,4,1,9,-1,-1,5],
        [-1,-1,-1,-1,8,-1,-1,7,9]
    ]
original_grid = [row.copy() for row in initial_puzzle]  # keep the givens
display_grid = [row.copy() for row in initial_puzzle]   # what we draw/modify

# currently selected cell (row, col) or (None, None) when nothing selected
selected_row, selected_col = None, None


def draw_background():
    screen.fill(pg.Color('white'))
    pg.draw.rect(screen,pg.Color("black"),pg.Rect(15,15,720,720),10)
    i=1
    while (i*80)<720:
        line_width=5 if i%3>0 else 10
        pg.draw.line(screen,pg.Color("black"),pg.Vector2((i*80)+15,15),pg.Vector2((i*80)+15,735),line_width)
        pg.draw.line(screen,pg.Color("black"),pg.Vector2(15,(i*80)+15),pg.Vector2(735,(i*80)+15),line_width)
        i+=1

    # draw selection highlight
    if selected_row is not None and selected_col is not None:
        x = selected_col*80 + 15
        y = selected_row*80 + 15
        pg.draw.rect(screen, pg.Color("gold"), pg.Rect(x+2, y+2, 80-4, 80-4), 4)

def draw_numbers():
    row=0
    offset=39
    while row<9:
        col=0
        while col<9:
            val = display_grid[row][col]
            if val != -1:
                color = pg.Color("black") if original_grid[row][col] != -1 else pg.Color("dodgerblue")
                n_text = font.render(str(val),True,color)
                screen.blit(n_text,pg.Vector2(col*80+offset+3,row*80+offset-15))
            col+=1
        row+=1

def game_loop():
    global selected_row, selected_col
    for event in pg.event.get():
        if event.type==pg.QUIT:
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                x, y = event.pos
                if 15 <= x <= 735 and 15 <= y <= 735:
                    col = (x - 15) // 80
                    row = (y - 15) // 80
                    selected_row, selected_col = int(row), int(col)
                else:
                    selected_row, selected_col = None, None
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s:  # Solve
                temp = [row.copy() for row in original_grid]
                if solve_sudoku(temp):
                    display_grid[:] = temp
                else:
                    print("No solution found")
            if event.key == pg.K_r:  # Reset
                display_grid[:] = [row.copy() for row in original_grid]

            # navigation keys and entry require a selected cell
            if selected_row is not None and selected_col is not None:
                # arrow keys
                if event.key == pg.K_UP:
                    selected_row = max(0, selected_row - 1)
                if event.key == pg.K_DOWN:
                    selected_row = min(8, selected_row + 1)
                if event.key == pg.K_LEFT:
                    selected_col = max(0, selected_col - 1)
                if event.key == pg.K_RIGHT:
                    selected_col = min(8, selected_col + 1)

                # clear cell
                if event.key in (pg.K_BACKSPACE, pg.K_DELETE, pg.K_0, pg.K_KP0):
                    if original_grid[selected_row][selected_col] == -1:
                        display_grid[selected_row][selected_col] = -1

                # number entry (main keys and keypad)
                for num_key, val in ((pg.K_1,1),(pg.K_2,2),(pg.K_3,3),(pg.K_4,4),(pg.K_5,5),(pg.K_6,6),(pg.K_7,7),(pg.K_8,8),(pg.K_9,9),
                                      (pg.K_KP1,1),(pg.K_KP2,2),(pg.K_KP3,3),(pg.K_KP4,4),(pg.K_KP5,5),(pg.K_KP6,6),(pg.K_KP7,7),(pg.K_KP8,8),(pg.K_KP9,9)):
                    if event.key == num_key:
                        # only allow editing non-given cells
                        if original_grid[selected_row][selected_col] == -1:
                            prev = display_grid[selected_row][selected_col]
                            display_grid[selected_row][selected_col] = -1
                            if is_valid(display_grid, val, selected_row, selected_col):
                                display_grid[selected_row][selected_col] = val
                            else:
                                display_grid[selected_row][selected_col] = prev
                                print("Invalid move")

    # draw and update display
    draw_background()
    draw_numbers()
    pg.display.flip()
    clock.tick(60)

while True:
    game_loop()