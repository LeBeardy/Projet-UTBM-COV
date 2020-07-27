from Modules.crawler.manager import Manager
from Modules.LDA.generateLDA import GenerateLDA
from Modules.LDA.Evaluator import Evaluator

#m = Manager()

#m.launch_spider()

#g = GenerateLDA()

#g.generateLDA()

e = Evaluator()

print(e.get_recommendations("expansion China"))
