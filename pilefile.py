
"""
Une implementation simple des piles et des files  avec les listes de Python
"""

##### Classe pile

class Pile:
  def __init__(self):
    self._data = []  

  def taille(self):
    return len(self._data)

  def estvide(self):
    return self.taille() == 0

  def empile(self, s):
    self._data.append(s)

  def depile(self):
    if self.estvide(): 
      raise LookupError('La pile est vide')
    return self._data.pop()

  def sommet(self):
    if self.estvide(): 
      raise LookupError('La pile est vide')
    return self._data[-1]
  
  def change_sommet(self, s):
    if self.estvide(): 
      raise LookupError('La pile est vide')
    self._data[-1] = s
  
  def __str__(self):
    return 'Pile: ' + ', '.join([str(item) for item in self._data])

##### Classe file
  
class File:
  def __init__(self):
    self._data = []  

  def taille(self):
    return len(self._data)

  def estvide(self):
    return self.taille() == 0

  def enfile(self, s):
    self._data.append(s)

  def defile(self):
    if self.estvide(): 
      raise LookupError('La file est vide')
    return self._data.pop(0)

  def premier(self):
    if self.estvide(): 
      raise LookupError('La file est vide')
    return self._data[0]
  
  def change_premier(self, s):
    if self.estvide(): 
      raise LookupError('La file est vide')
    self._data[0] = s
    
  def __str__(self):
    return 'File: ' + ', '.join([str(item) for item in self._data])
