from numpy import *
from dual_simplex_method import DualSimplexMethodSolver
from math import floor

class IntegerLinearProgrammingSolver(object):
  def __init__(self, A, b, c, d_low, d_high):
    self.A = A
    self.b = b
    self.c = c
    self.d_low = d_low
    self.d_high = d_high
    self.m, self.n = A.shape
    self.has_solution = False
    self.optimal_cost = -inf
    self.eps = 0.000001

  def is_integers(self, x):
    round_x = array([round(el) for el in x])
    return all(abs(round_x - x) < self.eps)

  def get_index_of_first_float(self, x):
    round_x = array([round(el) for el in x])
    return list(abs(round_x - x) < self.eps).index(False)

  def dfs(self, d_low, d_high, basic_indexes = None, nonbasic_indexes = None):
    try:
      res = DualSimplexMethodSolver(self.A, self.b, self.c, d_low, d_high, basic_indexes, nonbasic_indexes).solve()
      x = res.x
      raised = False
      cost = dot(self.c, x)
    except:
      raised = True
    if (raised or cost <= self.optimal_cost):
     return
    if (self.is_integers(x)):
      self.has_solution = True
      self.x = x
      self.optimal_cost = cost
    else:
      j0 = self.get_index_of_first_float(x)
      value = floor(x[j0])

      right = copy(d_high)
      right[j0] = value
      self.dfs(d_low, right, res.basic_indexes, res.nonbasic_indexes)

      left = copy(d_low)
      left[j0] = value + 1
      self.dfs(left, d_high, res.basic_indexes, res.nonbasic_indexes)

  def the_branch_and_bound_method(self):
    self.dfs(self.d_low, self.d_high)
    if self.has_solution:
      return self
    else:
      raise ValueError("This task has no solution.")

if __name__ == "__main__":
  A = array([
    array([1, 0, 1, 0, 0, 1], dtype=float64),
    array([1, 2, -1, 1, 1, 2], dtype=float64),
    array([-2, 4, 1, 0, 1, 0], dtype=float64),
  ])
  b = array([-3, 3, 13], dtype=float)
  c = array([-3, 2, 0, -2, -5, 2], dtype=float64)
  d_low = array([-2, -1, -2, 0, 1, -4], dtype=float64)
  d_high = array([2, 3, 1, 5, 4, -1], dtype=float64)
  x0 = IntegerLinearProgrammingSolver(A, b, c, d_low, d_high).the_branch_and_bound_method()
  print x0
  print dot(c, x0)
