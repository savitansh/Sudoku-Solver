"""This module contains some standard genome types.

"""

import random

class BaseGenome:
   
    def __init__(self, spawn_chances):
        """Constructor of BaseGenome

        
        """
        self.spawn_chances = spawn_chances
        self.total_target = sum(chance for _, chance in spawn_chances)
        self.partner = None

    def spawn(self, partner):
        
        self.partner = partner
        rnd = random.randrange(self.total_target)
        for spawn_fun, chance in self.spawn_chances:
            if rnd <= chance:
                child = spawn_fun(self)
                break
            rnd -= chance

        del self.partner 
        return child

    # def fresh(self):
    #     pass



class PermutateGenome(BaseGenome):
    
    def __init__(self, initial, spawn_chances=None):
      
        self.genes = initial[:]

        if not spawn_chances:
            spawn_chances = ((PermutateGenome.copy, 1),
                             (PermutateGenome.fresh, 1),
                             (PermutateGenome.crossover, 2),
                             (PermutateGenome.swap, 6))

        BaseGenome.__init__(self, spawn_chances)

    def copy(self, genes=None):
        
        if not genes:
            genes = self.genes
        return PermutateGenome(genes, self.spawn_chances)

    def fresh(self):
        
        child = self.copy()
        random.shuffle(child.genes)
        return child

    def swap(self):
        
        child = self.copy()
        i = random.randrange(len(child.genes))
        j = random.randrange(len(child.genes))
        child.genes[i], child.genes[j] = child.genes[j], child.genes[i]
        return child

    def crossover(self):
        
        genes1 = self.genes[:]
        genes2 = self.partner.genes[:]

        result = []
        i = 0
        conflicts = []
        while i < len(genes1):
            if genes1[i] == genes2[i]:
                result.append(genes1[i])
                genes1.pop(i)
                genes2.pop(i)
            else:
                conflicts.append(len(result))
                result.append(None)
                i += 1

        for i in conflicts:
            if random.random() < 0.5:
                result[i] = genes1[0]
                genes2.remove(genes1.pop(0))
            else:
                result[i] = genes2[0]
                genes1.remove(genes2.pop(0))

        return self.copy(result)


