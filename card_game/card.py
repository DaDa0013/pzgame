import pgzrun
import math
import random 
import pygame
import time

WIDTH = 963 
HEIGHT = 464

CARD_WIDTH = 71
CARD_HEIGHT = 96
GAP = 20
   
ROWMAX = 4
COLMAX = 13

SCORE_A=0
SCORE_B=0
GAMESTATE=0
position=0
doMouseClick=False

selCard1=None
selCard2=None

first=None
second=None

class CardTile:
  def __init__(self, x, y, w, h):
    self.x = x
    self.y = y
    self.width = w
    self.height = h

  def contains(self, px, py):
    return self.x < px and px < self.x+self.width and self.y < py and py < self.y+self.height

cardNames = [
  "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "cj", "cq", "ck",
  "d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8", "d9", "d10", "dj", "dq", "dk",
  "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "sj", "sq", "sk",
  "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "h10", "hj", "hq", "hk"
  ]

cardSprites = [Actor(card) for card in cardNames]
cardSpritesDic = {}
for card in cardNames:
  cardSpritesDic[card] = Actor(card)
cardSpritesDic["back"] = Actor("b1fv")

WHITE = (255,255,255)
BACK_GROUND = (0x00, 0x66, 0x33)


TOP_LEFT = 0
CW2 = CARD_WIDTH / 2
CH2 = CARD_HEIGHT / 2

tile2d = [None]*COLMAX*ROWMAX
for i in range(ROWMAX):
  for j in range(COLMAX):
    tile2d[i*COLMAX+j] = CardTile(j*CARD_WIDTH+GAP, i*CARD_HEIGHT+GAP, CARD_WIDTH, CARD_HEIGHT)

cardStatus = cardNames[:]
cardStatusOpen = [False]*COLMAX*ROWMAX

#for i in range(ROWMAX):
#  for j in range(COLMAX):
#    print(cardStatus[i*COLMAX + j], end =" ")
#  print ()

def suffle(count):
  for _ in range(count):
    r1 = math.floor(random.random() * ROWMAX)
    r2 = math.floor(random.random() * ROWMAX)
    c1 = math.floor(random.random() * COLMAX)
    c2 = math.floor(random.random() * COLMAX)
    card1 = cardStatus[r1*COLMAX + c1]
    cardStatus[r1*COLMAX + c1] = cardStatus[r2*COLMAX + c2]
    cardStatus[r2*COLMAX + c2] = card1

def display_score():
    font= pygame.font.SysFont('hyhwpeq',20)
    text_score_A = font.render(f'  PlayerA : {SCORE_A}',True,WHITE)
    text_score_B = font.render(f'  PlayerB: {SCORE_B}',True,WHITE)
    screen.blit(text_score_A,[200,420])
    screen.blit(text_score_B,[560,420])

def draw():
  screen.fill(WHITE)
  screen.draw.filled_rect(Rect(TOP_LEFT,TOP_LEFT,TOP_LEFT+WIDTH,TOP_LEFT+HEIGHT),BACK_GROUND)
  for loc, tile in enumerate(tile2d):
    card = cardStatus[loc]
    if card == None:
      continue
    isopen = cardStatusOpen[loc]
    sprite = cardSpritesDic[card] if isopen else cardSpritesDic["back"]
    sprite.pos = tile.x+CW2, tile.y+CH2
    sprite.draw()
    display_score()

def update():
  global position
  global GAMESTATE
  global selCard1
  global selCard2
  global first
  global second
  global doMouseClick
  global SCORE_A
  global SCORE_B
  if doMouseClick:
    if GAMESTATE == 0:
      first=position
      selCard1 = cardStatus[position]
      GAMESTATE = 1
      if selCard1 == None:
        GAMESTATE = 0

    elif GAMESTATE == 1:
      second=position
      selCard2=cardStatus[position]
      if selCard2 == None:
        GAMESTATE = 1
      elif first == second:
        GAMESTATE = 1
      elif selCard1[1]==selCard2[1]:
        SCORE_A += 1
        cardStatus[first] = None
        cardStatus[second] = None
        GAMESTATE = 2
      else:
        time.sleep(0.5)
        cardStatusOpen[first] = False
        cardStatusOpen[second] = False
        GAMESTATE = 2

    elif GAMESTATE == 2:
      first = position
      selCard1 = cardStatus[position]
      GAMESTATE = 3
      if selCard1 == None:
        GAMESTATE = 2

    elif GAMESTATE == 3:
      second=position
      selCard2=cardStatus[position]
      if selCard2 == None:
        GAMESTATE = 3
      elif first == second:
        GAMESTATE = 3
      elif selCard1[1]==selCard2[1]:
        SCORE_B+=1
        cardStatus[first] = None
        cardStatus[second] = None
        GAMESTATE = 0
      else:
        time.sleep(0.5)
        cardStatusOpen[first]=False
        cardStatusOpen[second] = False
        GAMESTATE = 0
    doMouseClick = False

def find_mouse_point_tile(px, py):
  for i, ti in enumerate(tile2d):
    if ti.contains(px, py):
      return i
  return -1

def on_mouse_down(pos):
  px, py = pos
  pos = find_mouse_point_tile(px, py)
  cardStatusOpen[pos] = True
  return pos

def on_mouse_up(pos):
  global position
  global doMouseClick
  px, py = pos
  pos = find_mouse_point_tile(px, py)
  position = pos
  doMouseClick=True
  return pos
  
suffle(1000)
pgzrun.go()