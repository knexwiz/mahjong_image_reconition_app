from enum import Enum
from math import ceil

class Suit(Enum):
  BAMBOO = "BAMBOO"
  DOT = "DOT"
  NUMBER = "NUMBER"
  HONOR = "HONOR"
  BLANK = "BLANK"
  
  def __str__(self):
    return self.value

ssort = {
  "BAMBOO": 10,
  "DOT": 20,
  "NUMBER": 30,
  "HONOR": 40,
  "BLANK": 0
}
sfind = {
  "b": Suit.BAMBOO,
  "d": Suit.DOT,
  "n": Suit.NUMBER,
  "h": Suit.HONOR
}

rsort = {
  "GREEN-DRAGON" : 1,
  "RED-DRAGON" : 2,
  "WHITE-DRAGON" : 3,
  "EAST-WIND" : 4,
  "SOUTH-WIND" : 5,
  "WEST-WIND" : 6,
  "NORTH-WIND" : 7,
}
class Rank(Enum):
  BLANK = "BLANK"
  
  ONE = 1
  TWO = 2
  THREE = 3
  FOUR = 4
  FIVE = 5
  SIX = 6
  SEVEN = 7
  EIGHT = 8
  NINE = 9
  
  GREEN = "GREEN-DRAGON"
  RED = "RED-DRAGON"
  WHITE = "WHITE-DRAGON"

  EAST = "EAST-WIND"
  SOUTH = "SOUTH-WIND"
  WEST = "WEST-WIND"
  NORTH = "NORTH-WIND"

  def is_blank (self):
    return self.value == "BLANK"
  
  def is_num (self):
    return self.value.__class__ is int
    
  def is_honor (self):
    return not self.is_blank() and not self.value.__class__ is int
    
  def is_terminal (self):
    return self.is_num() and (self == 1 or self == 9)

  def is_dragon (self):
    if self.is_honor():
      return self.value.endswith("DRAGON")
    return False

  def is_wind (self):
    if self.is_honor():
      return self.value.endswith("WIND")
    return False

  def next (self):
    if self.is_num():
      q = self.value + 1
      if q > 9: q = 1
      return Rank(q)
    if self.is_honor():
      if self.value == "GREEN-DRAGON": return Rank.RED
      if self.value == "RED-DRAGON": return Rank.WHITE
      if self.value == "WHITE-DRAGON": return Rank.GREEN
        
      if self.value == "EAST-WIND": return Rank.SOUTH
      if self.value == "SOUTH-WIND": return Rank.WEST
      if self.value == "WEST-WIND": return Rank.NORTH
      if self.value == "NORTH-WIND": return Rank.EAST

  def __eq__(self, other):
    if self.__class__ is other.__class__:
      return self.value == other.value
    if self.is_num() and other.__class__ is int:
      return self.value == other

    return NotImplemented

  def __gt__(self, other):
    if self.__class__ is other.__class__:
      return self.next() == other

    return NotImplemented

  def __ge__(self, other):
    if self.__class__ is other.__class__:
      return self.is_num and self.next() == other

    return NotImplemented
    
  def __str__(self):
    return str(self.value)

wfind = {
  "e": Rank.EAST,
  "s": Rank.SOUTH,
  "w": Rank.WEST,
  "n": Rank.NORTH,
}
dfind = {
  "g": Rank.GREEN,
  "r": Rank.RED,
  "h": Rank.WHITE
}

class Tile ():
  @staticmethod
  def from_str(str):
    if str[0].isdigit():
      suit = sfind[str[1]]
      rank = Rank(int(str[0]))
    else:
      suit = Suit.HONOR
      if str[1] == "d": rank = dfind[str[0]]
      else: rank = wfind[str[0]]
    return Tile(suit = suit, rank = rank, red = len(str) == 3, is_called = False)

  @staticmethod
  def is_meld(meld):
    return Tile.is_triplet(meld) or Tile.is_seq(meld) or Tile.is_kan(meld)
  
  @staticmethod
  def is_triplet(meld):
    return len(meld) == 3 and meld[0].__class__ is Tile and meld[1].__class__ is Tile and meld[2].__class__ is Tile and meld[0] == meld[1] and meld[0] == meld[2]
  
  @staticmethod
  def is_seq(meld):
    return len(meld) == 3 and meld[0].__class__ is Tile and meld[1].__class__ is Tile and meld[2].__class__ is Tile and(
      (meld[0] >= meld[1] and meld[1] >= meld[2]) or
      (meld[0] >= meld[2] and meld[2] >= meld[1]) or
      (meld[1] >= meld[0] and meld[0] >= meld[2]) or
      (meld[1] >= meld[2] and meld[2] >= meld[0]) or
      (meld[2] >= meld[0] and meld[0] >= meld[1]) or
      (meld[2] >= meld[1] and meld[1] >= meld[0]) )
  
  @staticmethod
  def is_kan(meld):
    return len(meld) == 4 and meld[0].__class__ is Tile and meld[1].__class__ is Tile and meld[2].__class__ is Tile and meld[3].__class__ is Tile and meld[0] == meld[1] and meld[0] == meld[2] and meld[0] == meld[3]
  
  def __init__(self, *, suit = Suit.BLANK, rank = Rank.BLANK, red = False, is_called = False):
    self.suit = suit
    self.rank = rank
    self.is_called = is_called
    self.red = False
    if red and rank == 5:
      self.red = True
      
  def __str__(self):
    if self.is_blank(): return "BLANK"
    if self.is_num(): s = "{}-{}".format(self.rank, self.suit).title()
    else: s = self.rank.value.title()
    if self.red: s = "Red-" + s
    if self.is_called: s ="[{}]".format(s)
    return s

  def __eq__(self, other):
    if self.__class__ is other.__class__:
      return self.suit == other.suit and self.rank == other.rank 

    return NotImplemented

  def __gt__(self, other):
    if self.__class__ is other.__class__:
      return self.suit == other.suit and self.rank > other.rank

  def __ge__(self, other):
    if self.__class__ is other.__class__:
      return self.suit == other.suit and self.rank >= other.rank and self.rank != 9

    return NotImplemented

    

  def is_blank (self):
    return self.rank.is_blank()
  
  def is_num (self):
    return self.rank.is_num()
    
  def is_honor (self):
    return self.rank.is_honor()
    
  def is_terminal (self):
    return self.rank.is_terminal()

  def is_dragon (self):
    return self.rank.is_dragon()

  def is_wind (self):
    return self.rank.is_wind()


################################################################################
################################################################################
################################################################################

class Hand ():
  def __init__ (self):
    self.closed_tiles = []
    self.open_melds = []
    self.closed_kans = []

  def __str__(self):
    s = "hand:\n"
    for meld in self.open_melds:
      if len(meld) == 3:
        s += "[{} / {} / {}]\n".format(*meld)
      else:
        s += "[{} / {} / {} / {}]\n".format(*meld)
    for meld in self.closed_kans:
      s += "---{} / {} / {} / {}---\n".format(*meld)

  def add_from_str(self, *strings):
    for ss in strings:
      for s in ss.split(" "):
        if len(s) > 3:
          if s[3].isdigit():
            suit = sfind[s[4]]
            rank = Rank(int(s[3]))
          else:
            suit = Suit.HONOR
            if s[4] == "d": rank = dfind[s[3]]
            else: rank = wfind[s[3]]
          if s.startswith("chi"):
            self.add_open_meld([
              Tile(suit = suit, rank = rank, red = len(s) == 6, is_called = False),
              Tile(suit = suit, rank = rank.next(), red = len(s) == 6, is_called = False),
              Tile(suit = suit, rank = rank.next().next(), red = len(s) == 6, is_called = False)])
          elif s.startswith("pon"):
            self.add_open_meld([
              Tile(suit = suit, rank = rank, red = len(s) == 6, is_called = False),
              Tile(suit = suit, rank = rank, red = False, is_called = False),
              Tile(suit = suit, rank = rank, red = False, is_called = False)])
          elif s.startswith("kan"):
            self.add_open_meld([
              Tile(suit = suit, rank = rank, red = len(s) == 6, is_called = False),
              Tile(suit = suit, rank = rank, red = False, is_called = False),
              Tile(suit = suit, rank = rank, red = False, is_called = False),
              Tile(suit = suit, rank = rank, red = False, is_called = False)])
          elif s.startswith("clk"):
            self.add_closed_kan([
              Tile(suit = suit, rank = rank, red = len(s) == 6, is_called = False),
              Tile(suit = suit, rank = rank, red = False, is_called = False),
              Tile(suit = suit, rank = rank, red = False, is_called = False),
              Tile(suit = suit, rank = rank, red = False, is_called = False)])
        else:
          self.add_closed_tile(Tile.from_str(s))
          
          

  def add_closed_tile (self, *tiles):
    self.closed_tiles.extend(tiles)

  def remove_closed_tile (self, *tiles):
    for tile in tiles:
      if tile in self.closed_tiles: self.closed_tiles.remove(tile)

  def add_open_meld (self, *melds):
    self.open_melds.extend(melds)

  def add_closed_kan (self, *melds):
    self.closed_kans.extend(melds)



    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Sorting ~~~~#
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
  
  
  
  def score(self, winning_tile, dora_ind = [], tsumo = False, prevalent_wind = Rank.EAST, seat_wind = Rank.EAST, riichi = False, double_riichi = False, ippatsu = False, kan_win = False, last_draw_win = False):
    kan_count = 0
    for meld in [*self.open_melds, *self.closed_kans]:
      if Tile.is_kan(meld): kan_count += 1
      elif not Tile.is_meld(meld): 
        raise Exception("Invalid Meld")

    all_tiles = [ *self.closed_tiles, winning_tile]
    for meld in [*self.open_melds, *self.closed_kans]:
      all_tiles.extend(meld)

    if len(all_tiles) != 14 + kan_count: raise Exception("Incorect Number of Tiles" + str(all_tiles))
    
    if self.open_melds == []: closed = True
    else: closed = False
    
    
    han_str = ""
    han = 0
    yakuman = 0
    yakuman_str = "Yakuman!"

    ####################################################### Yaku ################## Riichi #####
    if riichi and closed:
      if double_riichi:
        han += 2
        han_str += "\n  2 Double Riichi"
      else:
        han += 1
        han_str += "\n  1 Riichi"
      if ippatsu:
        han += 1
        han_str += "\n  1 Ippatsu"

    ####################################################### Yaku ######## Menzenchin Tsumo #####
    if tsumo and closed:
      han += 1
      han_str += "\n  1 Menzenchin Tsumo"
    
    ####################################################### Yaku ##### Under the Sea/River #####
    if last_draw_win:
      han += 1
      if tsumo: han_str += "\n  1 Under the Sea"
      else: han_str += "\n  1 Under the River"
    
    ####################################################### Yaku ####### After/Robbing Kan #####
    if kan_win:
      han += 1
      if tsumo: han_str += "\n  1 Rinshan Kaihou"
      else: han_str += "\n  1 Robbing a Kan"
    
    ####################################################### Yaku ############# Seven Pairs #####
    seven_pairs = False
    if closed and kan_count == 0:
      seven_pairs = True
      for tile in all_tiles:
        f = list(filter(lambda t: t == tile, all_tiles))
        if len(f) != 2: seven_pairs = False
    
    ####################################################### Yakuman ########### 13 Orphans #####
    orphans = False
    if closed and kan_count == 0:
      h = ["HONORGREEN-DRAGON", "HONORRED-DRAGON", "HONORWHITE-DRAGON",
          "HONOREAST-WIND", "HONORSOUTH-WIND", "HONORWEST-WIND", "HONORNORTH-WIND",
          "BAMBOO1", "BAMBOO9", "DOT1", "DOT9", "NUMBER1", "NUMBER9"]
      i = 0
      f = False
      p = False
      while not f and i < 14:
        s = all_tiles[i].suit.value + str(all_tiles[i].rank.value)
        if s in h:
          h.remove(s)
        elif not p:
          if all_tiles[i].suit == Suit.HONOR or all_tiles[i].rank == 1 or all_tiles[i].rank == 9:
            p = True
          else: f = True
        else: f = True
        i += 1
      if p and not f:
        yakuman += 1
        yakuman_str += "\n13 Orphans"
        orphans = True
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Sorting ~~~~#
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    closed_melds = []
    pair = None

    try:
      c = self.closed_tiles.copy()
      c.append(winning_tile)
      c.sort(key=lambda t: ssort[t.suit.value] + (t.rank.value if t.is_num() else rsort[t.rank.value]))
      
      while c != []:
        i = 1
        while i < len(c) and (c[i-1] == c[i] or c[i-1] >= c[i]): i += 1
        if i == 1: raise Exception("Lone closed tile {}".format(c[0]))
        elif i == 2: 
          if pair == None:
            if c[0] == c[1]:
              pair = c[0:2]
            else:
              raise Exception("Bad Pair {} + {}".format(*c[0:2]))
          else:
            raise Exception("Double Pair")
        elif i == 3:
          if Tile.is_meld(c[0:3]): closed_melds.append(c[0:3])
          else: raise Exception("Bad Meld {} + {} + {}".format(*c[0:3]))
        elif i == 4:
          raise Exception("Bad Quad {} + {} + {} + {}".format(*c[0:4]))
        elif i == 5:
          if pair == None:
            if Tile.is_meld(c[0:3]) and c[3]==c[4]:
              closed_melds.append(c[0:3])
              pair = c[3:5]
            elif Tile.is_meld(c[2:5]) and c[0]==c[1]:
              closed_melds.append(c[2:5])
              pair = c[0:2]
            elif Tile.is_meld([c[0],c[1],c[4]]) and c[2]==c[3]:
              closed_melds.append([c[0],c[1],c[4]])
              pair = c[2:4]
            else: Exception("Bad 5 {} + {} + {} + {} + {}".format(*c[0:5]))
          else:
            raise Exception("Bad 5 Double pair {} + {} + {} + {} + {}".format(*c[0:5]))
        elif i == 6 or i == 9 or i == 12:
          melded = big_meld(c[0:i])
          if melded != None: closed_melds.extend(melded)
          else: Exception("Bad set")
        elif i == 7 or i == 10 or i == 13: raise Exception("Bad {}".format(i))
        elif i == 8 or i == 11 or i == 14:
          if pair == None:
            pairindex = 0
            while pairindex < i-1 and pair == None:
              if c[pairindex] == c[pairindex + 1]:
                melded = big_meld([*c[0:pairindex],*c[pairindex+2:i]])
                if melded != None:
                  closed_melds.extend(melded)
                  pair = [c[pairindex], c[pairindex + 1]]
                else: Exception("Bad set")
              pairindex += 1
          else: raise Exception("Bad {} Double pair".format(i))
        else: raise Exception("How?!?")
        c = c[i:len(c)]

      
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ print ~~~~#
    
      sss = "open:"
      for t in self.open_melds:
        sss += "\n  "
        for q in t:
          sss += " " + str(q)
      sss += "\n\nclosed:"
      for t in [*closed_melds, *self.closed_kans]:
        sss += "\n  "
        for q in t:
          sss += " " + str(q)
      sss += "\n\npair:\n  "
      for t in pair: sss += " "+str(t)
      print(sss)
      seven_pairs = False
    except Exception as e:
      if not seven_pairs and not orphans:
        raise e
      elif seven_pairs:
        han += 2
        han_str += "\n  2 Seven Pairs"
    
    all_melds = [*closed_melds, *self.closed_kans, *self.open_melds]
    ####################################################### Yaku ################### Pinfu #####
    pinfu = False
    if closed and not seven_pairs:
      seqs = 0
      wait = False
      for meld in closed_melds:
        if Tile.is_seq(meld):
          seqs += 1
          if winning_tile in meld:
            wt = meld.copy()
            wt.remove(winning_tile)
            if (wt[0] >= wt[1] or wt[1] >= wt[0]) and not (
              (winning_tile.rank == 3 and (wt[0].rank == 1 or wt[1].rank == 1)) or
              (winning_tile.rank == 7 and (wt[0].rank == 9 or wt[1].rank == 9)) ):
                wait = True
      if seqs == 4 and wait:
        han += 1
        han_str += "\n  1 Pinfu"
        pinfu = True

    ####################################################### Yaku ################ Iipeikou #####
    if closed and not seven_pairs:
      seqs = 0
      for meld in closed_melds:
        if Tile.is_seq(meld):
          for meld2 in closed_melds:
            if meld is not meld2 and meld[0] == meld2[0]:
              seqs += 1
      if seqs == 2 or seqs == 6:
        han += 1
        han_str += "\n  1 Pure Double Sequence"
      if seqs == 4 or seqs == 12:
        han += 3
        han_str += "\n  3 Twice Pure Double Sequence"

    ####################################################### Yaku ################# Yakuhai #####
    dargs = 0
    wmnds = 0
    for meld in all_melds:
      if meld[0].is_dragon():
        dargs += 1
        han += 1
        han_str += "\n  1 " + meld[0].rank.value.title()
      if meld[0].is_wind():
        wmnds += 1
        if meld[0].rank == prevalent_wind:
          han += 1
          han_str += "\n  1 Prevalent Wind"
        if meld[0].rank == seat_wind:
          han += 1
          han_str += "\n  1 Seat Wind"
    if dargs == 2 and pair[0].is_dragon():
      han += 2
      han_str += "\n  2 Little Three Dragons"
    if dargs == 3:
      yakuman += 1
      yakuman_str += "\nBig Three Dragons"
    if wmnds == 3 and pair[0].is_wind():
      yakuman += 1
      yakuman_str += "\nLittle Four Wins"
    if wmnds == 4:
      yakuman += 100
      yakuman_str += "\nBig Four Winds"
    
    ####################################################### Yaku # Mixed Trip Seq/Full Seq #####
    seq_starts = []
    for meld in all_melds:
      if Tile.is_seq(meld):
        if meld[0].rank.value < meld[1].rank.value and meld[0].rank.value < meld[2].rank.value:
          seq_starts.append(meld[0])
        elif meld[1].rank.value < meld[2].rank.value:
          seq_starts.append(meld[1])
        else:
          seq_starts.append(meld[2])
    
    
    if len(seq_starts) >= 3:
      
      trip_seq_check = lambda s1, s2, s3: s1.rank == s2.rank and s2.rank == s3.rank and s1 != s2 and s1 != s3 and s2 != s3
      if (len(seq_starts) == 3 and trip_seq_check(*seq_starts)) or (len(seq_starts) == 4 and (
        trip_seq_check(seq_starts[0],seq_starts[1],seq_starts[2]) or
        trip_seq_check(seq_starts[0],seq_starts[1],seq_starts[3]) or
        trip_seq_check(seq_starts[0],seq_starts[2],seq_starts[3]) or
        trip_seq_check(seq_starts[1],seq_starts[2],seq_starts[3])
      )):
        han += 2 if closed else 1
        han_str += "\n  {} Mixed Tripple Sequence".format("2 Closed" if closed else "1")

      def straight_check (s1, s2, s3):
        srk = [s1.rank.value,s2.rank.value,s3.rank.value]
        return s1.suit == s2.suit and s2.suit == s3.suit and 1 in srk and 4 in srk and 7 in srk 
      
      if (len(seq_starts) == 3 and straight_check(*seq_starts)) or (len(seq_starts) == 4 and (
        straight_check(seq_starts[0],seq_starts[1],seq_starts[2]) or
        straight_check(seq_starts[0],seq_starts[1],seq_starts[3]) or
        straight_check(seq_starts[0],seq_starts[2],seq_starts[3]) or
        straight_check(seq_starts[1],seq_starts[2],seq_starts[3])
      )):
        han += 2 if closed else 1
        han_str += "\n  {} Pure Straight".format("2 Closed" if closed else "1")
        
        
    ####################################################### Yaku ######### Simples/Outside #####
    if not orphans:
      outside = True
      simps = 0
      terms = 0
      hons  = 0
  
      for meld in [*all_melds,pair]:
        if Tile.is_seq(meld):
          if meld[0].is_terminal() or meld[1].is_terminal() or meld[2].is_terminal():
            simps += 2
            terms += 1
          else:
            simps += 3
            outside = False
        else:
          if meld[0].is_terminal():
            terms += 3
          elif meld[0].is_honor():
            hons += 3
          else:
            simps += 3
            outside = False
  
      if terms == 0 and hons == 0:
        han += 1
        han_str += "\n  1 All Simples"
  
      if outside:
        if hons == 0:
          if simps == 0:
            yakuman += 1
            yakuman_str += "\nAll Terminals"
          else:
            han += 3 if closed else 2
            han_str += "\n  {} Full Outside Hand".format("3 Closed" if closed else "2")
        elif terms == 0:
          yakuman += 1
          yakuman_str += "\nAll Honors"
        else:
          han += 2 if closed else 1
          han_str += "\n  {} Half Outside Hand".format("2 Closed" if closed else "1")

    
    ####################################################### Yaku ########### Triplets/Kans #####
    contrips = 0
    trips = 0
    kans = 0
    tripranks = []
    
    for meld in all_melds:
      if Tile.is_triplet(meld):
        trips += 1
        if meld not in self.open_melds and (tsumo or winning_tile not in meld or len(list(filter(lambda t: t == winning_tile, all_tiles)))):
          contrips += 1
        tripranks.append(meld[0])
      if Tile.is_kan(meld):
        trips += 1
        kans += 1
        if meld not in self.open_melds:
          contrips += 1
        tripranks.append(meld[0])

    if trips == 4:
      han += 2
      han_str += "\n  2 All Triplets"
    if contrips == 3:
      han += 2
      han_str += "\n  2 Three Conceald Triplets"
    if contrips == 4:
      if winning_tile in pair:
        yakuman += 100
        yakuman_str += "\nSingle Wait Four Conceald Triplets"
      else:
        yakuman += 1
        yakuman_str += "\nFour Conceald Triplets"
    if kans == 3:
      han += 2
      han_str += "\n  Three Kahns"
    if kans == 4:
      yakuman += 1
      yakuman_str += "\nFour Kass"
      
      
    if len(tripranks) >= 3:
      trip_trip_check = lambda s1, s2, s3: s1.rank == s2.rank and s2.rank == s3.rank and s1 != s2 and s1 != s3 and s2 != s3
      if (len(tripranks) == 3 and trip_trip_check(*tripranks)) or (len(tripranks) == 4 and (
        trip_trip_check(tripranks[0],tripranks[1],tripranks[2]) or
        trip_trip_check(tripranks[0],tripranks[1],tripranks[3]) or
        trip_trip_check(tripranks[0],tripranks[2],tripranks[3]) or
        trip_trip_check(tripranks[1],tripranks[2],tripranks[3])
      )):
        han += 2
        han_str += "\n  2 Tripple Triplets"

    
    ####################################################### Yaku ################# Flushes #####
    flush = True
    flushsuit = None
    allgreen = True
    fullflush = True
    gates = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

    for tile in all_tiles:
      if tile.is_num():
        if tile.suit != flushsuit:
          if flushsuit == None: flushsuit = tile.suit
          else: flush = False
        gates[tile.rank.value] += 1
        if tile.rank.value in [1,5,7,9]: allgreen = False
      else:
        fullflush = False
        if tile.rank != Rank.GREEN: allgreen = False


    if flush:
      if flushsuit == Suit.BAMBOO and allgreen:
        yakuman += 1
        yakuman_str += "\nAll Green"
      elif fullflush:
        if closed and gates[1] >= 3 and gates[9] >= 3 and len(list(filter(lambda v: v ==0, list(gates.values())))) == 0:
          if gates[winning_tile.rank.value] % 2 == 0:
            yakuman += 100
            yakuman_str += "\nTrue Nine Gates"
          else:
            yakuman += 1
            yakuman_str += "\nNine Gates"
        else:
          han += 6 if closed else 5
          han_str += "\n  {} Full Flush".format("6 Closed" if closed else "5")
      else:
        han += 3 if closed else 2
        han_str += "\n  {} Half Flush".format("3 Closed" if closed else "2")
          
    ################################################################################# DORA #####
    dora = 0
    for tile in all_tiles:
      for di in dora_ind:
        if di > tile: dora += 1
      if tile.red: dora += 1
    if dora != 0: han_str += "\n  {} Dora".format(dora)
    han += dora
    han_str = "Han {}:".format(han) + han_str
    
    ##base
    if yakuman > 0:
      if yakuman >= 100:
        han_str = "Double " + yakuman_str
        base = 16000
      else:
        han_str = yakuman_str
        base = 8000
    elif han == 5:
      base = 2000
      han_str = "Mangan!\n" + han_str
    elif han >= 6 and han <= 7:
      base = 3000
      han_str = "Haneman!\n" + han_str
    elif han >= 8 and han <= 10:
      base = 4000
      han_str = "Baiman!\n" + han_str
    elif han >= 11 and han <= 12:
      base = 6000
      han_str = "Sanbaiman!\n" + han_str
    elif han >= 13:
      base = 8000
      han_str = "Kazoe Yakuman!\n" + han_str
    else:
      fu = 20
      fu_str = "\n\nFu {}:\n  20 Base"
      #[*closed_melds, *self.closed_kans, *self.open_melds]
      if seven_pairs:
        fu = 25
        fu_str = "\n\n{} Fu - Seven Pairs"
      else:
        if closed and not tsumo:
          fu += 10
          fu_str += "\n  10 Menzen-Kafu"
  
        if tsumo and not pinfu:
          fu += 2
          fu_str += "\n  2 Tsumo"
          
        for meld in all_melds:
          b, bs = 0, ""
          if Tile.is_triplet(meld):
            b, bs = 2, "Triplet"
          if Tile.is_kan(meld):
            b, bs = 8, "Kan"
          if meld not in self.open_melds:
            b *= 2
            bs = "Closed " + bs
          if meld[0].is_honor() or meld[0].is_terminal():
            b *= 2
          if b > 0:
            fu += b
            fu_str += "\n  {} {}".format(b, bs)
            
        wait = winning_tile in pair
        for meld in all_melds:
          if winning_tile in meld:
            if Tile.is_seq(meld):
              wt = meld.copy()
              wt.remove(winning_tile)
              if not ((wt[0] >= wt[1] or wt[1] >= wt[0]) and not (
                (winning_tile.rank == 3 and (wt[0].rank == 1 or wt[1].rank == 1)) or
                (winning_tile.rank == 7 and (wt[0].rank == 9 or wt[1].rank == 9)) )):
                  wait = True
            else: wait = True
        if wait:
          fu += 2
          fu_str += "\n  2 Single Wait"
          
        if pair[0].is_dragon() or pair[0].rank == seat_wind or pair[0].rank == prevalent_wind:
          fu += 2
          fu_str += "\n  2 Yakuhai Pair"

        if fu == 20 and not closed:
          fu += 2
          fu_str += "\n  2 Open Pinfu"
      
        fu = r10(fu)
      
      base = fu * pow(2, 2 + han)
      han_str += fu_str.format(fu)

      if base >= 2000:
        base = 2000
        han_str = "Mangan!\n" + han_str
    han_str += "\n\nBase Points:{}\n\n".format(base)
    if tsumo:
      if seat_wind == Rank.EAST:
        han_str += "{} each player\n\n{} Total".format(r100(base*2),r100(base*2)*3)
      else:
        han_str += "{} from dealer\n{} from others\n\n{} Total".format(r100(base*2), r100(base), r100(base*2)+ r100(base)*2)
    else:
      if seat_wind == Rank.EAST:
        han_str += "{} Total".format(r100(base*6))
      else:
        han_str += "{} Total".format(r100(base*4))
        
      
    return han_str
    
    
      

r100 = lambda r: ceil( r / 100 ) * 100
r10 = lambda r: ceil( r / 10 ) * 10
fsi = [
  [1, 2],
  [1, 4],
  [1, 5],
  [2, 4],
  [2, 5],
  [2, 6]
]
def big_meld(c):
  if len(c) == 6:
    if Tile.is_meld(c[0:3]) and Tile.is_meld(c[3:6]):
      return [c[0:3], c[3:6]]
    elif Tile.is_meld([c[0],c[2],c[4]]) and Tile.is_meld([c[1],c[3],c[5]]):
      return [[c[0],c[2],c[4]], [c[1],c[3],c[5]]]
    elif Tile.is_meld([c[0],c[1],c[5]]) and Tile.is_meld(c[2:5]):
      return [[c[0],c[1],c[5]], c[2:5]]
    else:
      return None
  elif len(c) > 6 and len(c)%3 == 0:
    for q in fsi:
      seed = [c[0],c[q[0]],c[q[1]]]
      if Tile.is_meld(seed):
        smaller = big_meld([*c[1:q[0]],*c[q[0]+1:q[1]],*c[q[1]+1:len(c)]])
        if smaller != None:
          return [seed, *smaller]

di = [
  Tile.from_str("8b"),Tile.from_str("7n")
]

ha = Hand()
ha.add_from_str("1n 1n chi3nr 5n 5n 5n 7n 8n 8n 8n 9n")
score = ha.score(Tile.from_str("8n"),tsumo=False,seat_wind=Rank.EAST, dora_ind = di, riichi=True, ippatsu=True)
print("\n\n\n")
print(score)