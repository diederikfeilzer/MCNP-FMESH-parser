#!/usr/bin/env python

class MESHTAL:
	def __init__(self, filename):
		self.content = []
		self.cursor = 0
		with open(filename) as f:
			self.content = [x.strip() for x in f.readlines()]
		self.len = len(self.content)
	
	def readmesh(self):
		if self.skipTill(['Mesh', 'Tally', 'Number', False]) == False:
			return False, False, False
	  	
		tallynumber = self.getLineComponents()[3]
		self.skipLines(1)
		tallytype = self.getLine()
		self.skipTill(['X', 'direction:'])
		Xcomponents = map(float,self.getLineComponents()[2:])
		self.skipTill(['Y', 'direction:'])
		Ycomponents = map(float,self.getLineComponents()[2:])
		self.skipTill(['Z', 'direction:'])
		Zcomponents = map(float,self.getLineComponents()[2:])
		self.skipTill(['Energy', 'bin', 'boundaries:'])
		Ecomponents = map(float,self.getLineComponents()[3:])
		
		Xbins = len(Xcomponents) - 1
		Ybins = len(Ycomponents) - 1
		Zbins = len(Zcomponents) - 1
		Ebins = len(Ecomponents) - 1
		
		data = [[[0 for k in xrange(Xbins)] for j in xrange(Ybins)] for i in xrange(Zbins)]
		erro = [[[0 for k in xrange(Xbins)] for j in xrange(Ybins)] for i in xrange(Zbins)]
		
		# to make suitable for multiple energy bins, add E dimension
		
		for e in range(Ebins):
			self.skipTill(['Energy', 'Bin:', False, '-', False, 'MeV'])
			
			for z in range(Zbins):
				self.skipTill(['Z', 'bin:', False, '-', False])
				self.skipTill(['Tally', 'Results:'])
				self.skipLines(1)
				
				for y in range(Ybins):
					self.skipLines(1)
					data[z][y] = map(float,self.getLineComponents()[1:])
				
				self.skipTill(['Relative','Errors'])
				self.skipLines(1)
				
				for y in range(Ybins):
					self.skipLines(1)
					erro[z][y] = map(float,self.getLineComponents()[1:])
		
		return tallynumber, data, True
		
	def getLine(self):
		return self.content[self.cursor]
		
	def getLineComponents(self):
		return self.getLine().split()
			
	def skipLines(self, number):
		self.cursor += 1
			
	def skipTill(self, val):
		for cursor in range(self.cursor,len(self.content)):
			components = self.content[cursor].split()
			if self.matches(components, val):
				self.cursor = cursor
				return True
		self.cursor = self.len-1
		return False
	
	def matches(self, components, val):
		if len(components) < len(val):
			return False
		for i in xrange(len(val)):
			if val[i] != components[i] and val[i] != False:
				return False
		return True

#-----

import optparse, numpy, scipy.io

def main():
  p = optparse.OptionParser()
  options, arguments = p.parse_args()
  input = 'inputmsht'
  if len(arguments) > 0:
    input = arguments[0]
    
    if len(arguments) > 1:
      output = arguments[1]
    else:
      output = 'mesh.mat'

    obj = MESHTAL(input)
    dict = {};

    print 'Parsing FMESHES in %s....' % input
    
    while obj.cursor < obj.len - 1:
      tallynumber, data, suc = obj.readmesh()
      if suc == True:
        dict[('data'+tallynumber)] = data
        print 'Parsed FMESH%s into data%s variable.' % (tallynumber, tallynumber)

    scipy.io.savemat(output, mdict=dict, do_compression=True, oned_as='column', appendmat=True)

    print 'Saved variables in %s.' % (output)
      
  else:
    print '+-----------------------------------------------------------+'
    print '| MCNP FMESH output file parser.                            |'
    print '+-----------------------------------------------------------+'
    print '| Requirements:                                             |'
    print '| - rectangular FMESH type 4.                               |'
    print '| - one or no energy bins.                                  |'
    print '| - "OUT" set to "IJ" on the FMESH card.                    |'
    print '+-----------------------------------------------------------+'
    print '| usage:                                                    |'
    print '|                                                           |'
    print '| ./parse.py [input] [output]                               |'
    print '|                                                           |'
    print '|   input  :    the msht file location provided by MCNP     |'
    print '|   output :    the matlab export location defaults to:     |'
    print '|                 "./mesh.mat"                              |'
    print '+-----------------------------------------------------------+'
    print '| Diederik Feilzer - 2018 - GNU General Public License v3.0 |'
    print '+-----------------------------------------------------------+'
 
if __name__ == '__main__':
  main()
		



