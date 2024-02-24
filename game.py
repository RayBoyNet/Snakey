import curses
from curses import wrapper
import time
import random

def game(stdscr):

 max_y = curses.LINES
 max_x = curses.COLS
 mid_y = int(max_y/2)
 mid_x = int(max_x/2)
 min_y = 0
 min_x = 0
 
 def print_snake():
  stdscr.clear()
  for i in snake_coord:
   stdscr.addch(i[0],i[1],"█",curses.color_pair(1))
  print_globule()
  stdscr.refresh()
  time.sleep(delay)

 def move_left():
  snake_coord.pop(len(snake_coord)-1)
  old_tup = snake_coord[0]
  new_tup = (old_tup[0],) + (old_tup[1]-1,)
  snake_coord.insert(0,new_tup)
  print_snake()
  # print(snake_coord)

 def move_right():
  snake_coord.pop(len(snake_coord)-1)
  old_tup = snake_coord[0]
  new_tup = (old_tup[0],) + (old_tup[1]+1,)
  snake_coord.insert(0,new_tup)
  print_snake()
  # print(snake_coord)

 def move_up():
  snake_coord.pop(len(snake_coord)-1)
  old_tup = snake_coord[0]
  new_tup = (old_tup[0]-1,) + (old_tup[1],)
  snake_coord.insert(0,new_tup)
  print_snake()
  # print(snake_coord)

 def move_down():
  snake_coord.pop(len(snake_coord)-1)
  old_tup = snake_coord[0]
  new_tup = (old_tup[0]+1,) + (old_tup[1],)
  snake_coord.insert(0,new_tup)
  print_snake()
  # print(snake_coord)

 def direction():
  vector = [snake_coord[0][0]-snake_coord[1][0],snake_coord[0][1]-snake_coord[1][1]]
  # [0,1]  : right
  # [1,0]  : down
  # [-1,0] : up
  # [0,-1] : left
  return vector
 
 def globule_gen():
  globule_y = random.randint(min_y,max_y-1)
  globule_x = random.randint(min_x,max_x-1)
  globule_coord[0] = globule_y
  globule_coord[1] = globule_x
  while tuple(globule_coord) in snake_coord:
    globule_y = random.randint(min_y,max_y-1)
    globule_x = random.randint(min_x,max_x-1)
    globule_coord[0] = globule_y
    globule_coord[1] = globule_x
  return globule_coord
 
 def print_globule():
  stdscr.addch(globule_coord[0],globule_coord[1],"O")
  return None
 
 def check_globule(delay):
  if (snake_coord[0][0] == globule_coord[0]) and (snake_coord[0][1] == globule_coord[1]):
    globule_gen()
    grow()
    delay /= 1.05
  return delay
 
 def grow():
  num = (max_y-1) * (max_x-1)
  if len(snake_coord) > 0.75*num:
    # print(num)
    return None
  last_coord_y = snake_coord[-1][0]
  last_coord_x = snake_coord[-1][1]
  second_last_coord_y = snake_coord[-2][0]
  second_last_coord_x = snake_coord[-2][1]
  vector = [last_coord_y-second_last_coord_y,last_coord_x-second_last_coord_x]
  # print(f"vector: {vector}")
  new_coord_y = snake_coord[-1][0] + vector[0]
  new_coord_x = snake_coord[-1][1] + vector[1]
  # print(f"new coord: [{new_coord_y},{new_coord_x}]")
  snake_coord.append((new_coord_y,new_coord_x))
  return None
 
 def get_key():
  input = stdscr.getkey()
  # print(input)
  return input
 
 def collision_detector():
   length = len(snake_coord)
   unique = len(set(snake_coord))
   return length != unique
 
 # Initialise

 def initialise():
  stdscr.nodelay(True)
  curses.noecho()
  curses.curs_set(0)
  curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
  print_snake()
  return None
 
 snake_coord = [(mid_y,mid_x-1),(mid_y,mid_x),(mid_y,mid_x+1),(mid_y,mid_x+2)]
 globule_coord = [0,0]
 dir_vec = [0,0]
 delay = 0.1
 globule_coord = globule_gen()

 initialise()
     
 while True:

  try:
    input_key = get_key()
  except:
    input_key = None

  try:

    match (input_key):
      case 'w':
        move_up()  
        dir_vec = direction()  
      case 'a':
        move_left() 
        dir_vec = direction()    
      case 's':
        move_down() 
        dir_vec = direction()      
      case 'd':
        move_right() 
        dir_vec = direction()
      # case ' ':
      #   break  
      case _:
        match (dir_vec):
          case [-1,0]:
            move_up()   
          case [0,-1]:
            move_left()
          case [1,0]:
            move_down()
          case [0,1]:
            move_right()
          case _:
            move_left()

  # except KeyboardInterrupt:
  #   break
  
  except:
    time.sleep(3)
    print("Out of bounds!")
    break
  
  delay = check_globule(delay)

  if collision_detector():
    time.sleep(3)
    print("Ouroboros!")
    break

wrapper(game)

