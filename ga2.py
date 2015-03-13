"""The Genetic Algorithm module.

"""

import random
import time
import signal
import sys

class GA:
    """A Genetic Algorithm.
    """
    def __init__(self, find_fitness, genome, population=10000,
                 local_size=10, tourney_size=3, verbose=True):
        """Constructor of GA.

        """
        self.iterations = 0
        self.population = population
        self.local_size = local_size
        self.tourney_size = tourney_size
        self.best_found = 0
        self.best_genome = None
        self.best_fitness = 0
        self.last_eden = 0
        self.userstop = False
        self.find_fitness = find_fitness
        self.pop = []
        self.first_genome = genome
        self.verbose = verbose
        
        self.start_state()
        
    def start_state(self):
        
        self.best_fitness = 0
        self.last_eden = self.iterations
        self.best_genome = None
        self.pop = []
        for _ in xrange(self.population):
            self.pop.append(self.first_genome.fresh())

        for guy in self.pop:
            self.find_best_genome(guy)

    
    def find_best_genome(self, genome):
        """Calculate fitness of genome and check if it is the best found so far.

        """
        genome.fitness = self.find_fitness(genome)
        if genome.fitness < self.best_fitness or self.best_genome is None:
            self.best_fitness = genome.fitness
            self.best_genome = genome.copy()
            self.best_found = self.iterations - self.last_eden
            if self.verbose:
                print 'Optimal fitness = ', genome.fitness
                print "best solution so far : ",self.best_genome.genes
            sys.stdout.flush()

    def _choose(self):
        """Choose a number of genomes to compete.

        """
        if not self.local_size:
            return [random.randrange(len(self.pop))
                    for _ in xrange(self.tourney_size)]

        midpoint = random.randrange(len(self.pop))
        chosen = [midpoint]
        for _ in xrange(self.tourney_size - 1):
            i = midpoint + random.randrange(-self.local_size, self.local_size)
            i %= len(self.pop) 
            chosen.append(i)
        return chosen

    def evolve(self, seconds=0, target_fitness=None, use_restarts=True):
       
        start = time.time()

        self.userstop = False
        def stop(signum, frame):
            """A Ctrl-C signal handler"""
            self.userstop = True
            if self.verbose:
                print '\nexit'
        oldhandler = signal.signal (signal.SIGINT, stop)

        try:
            while ((not seconds) or time.time() - start < seconds) and \
                    not self.userstop and \
                    (self.best_fitness > target_fitness or \
                         target_fitness is None):

                max_inactive = max(self.best_found * 2, self.population * 10)
                thisrun = self.iterations - self.last_eden
                if use_restarts and thisrun > max_inactive:
                    if self.verbose:
                        print 'Restart!'
                    self.start_state()

                self.iterations += 1

                fids = [(self.pop[i].fitness, i) for i in self._choose()]
                fids.sort()
            
                self.pop[fids[-1][1]] = self._make_child(fids[0][1], fids[1][1])

                self.find_best_genome(self.pop[fids[-1][1]])
        finally:
            signal.signal(signal.SIGINT, oldhandler)

        return self.best_genome, self.best_fitness



    def _make_child(self, genome1, genome2):
        """Create a new child from genomes with genome1 and genome2.
        """

        return self.pop[genome1].spawn(self.pop[genome2])

