# -*- coding: utf-8 -*-

from threading import Thread

import time
import random
import sys



class Node(Thread):

  def __init__ (self,n): 
    self.n=n
    Thread.__init__(self)
  # end def

  def run(self):
    for i in range(20):
#      time.sleep(random.random())
      time.sleep(0.5)
      print(self.n,end='')
      sys.stdout.flush()
    # end for
  # end def

# end class



if __name__ == '__main__':

  w1 = Node(0)
  w2 = Node(1)

  w1.start()
  w2.start()

  w1.join()
  w2.join()

  print("\nstop")
# end if




