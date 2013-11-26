from openmdao.main.api import Assembly, Component
from openmdao.lib.drivers.api import DOEdriver
from openmdao.lib.doegenerators.api import FullFactorial
from openmdao.lib.casehandlers.api import DumpCaseRecorder
from openmdao.lib.datatypes.api import Float
from openmdao.lib.drivers.api import BroydenSolver

from pycycle.api import (FlightConditions, Inlet, SplitterBPR, Compressor, Duct,
    Nozzle, Burner, Turbine, Nozzle, FlowStationVar)

class Turbofan(Assembly): 
	
   def configure(self):

        #component definition
        fc = self.add('fc', FlightConditions())
        fc.alt = 35000
        fc.MN = .8
        fc.Wout = 100
        
        inlet = self.add('inlet', Inlet() )
        
        fan = self.add('fan', Compressor())
        fan.eff = .867
        fan.PR = 1.645
        
        split = self.add( 'split', SplitterBPR())
        split.BPR = 5.041
        
        bypduct = self.add( 'bypduct', Duct())
        
        bypnoz = self.add( 'bypnoz', Nozzle())
        self.connect('fc.Fl_O.Ps', 'bypnoz.PsExh')       
        
        lpc = self.add( 'lpc', Compressor())
        lpc.eff = .868
        lpc.PR = 2.488       
        

        hpc = self.add( 'hpc', Compressor())
        hpc.eff = .865
        hpc.PR = 2.0424        
               
        
        burner = self.add( 'burner', Burner())
        burner.ID_fuel = 5
        burner.hFuel = -1200
        burner.Wfuel = 1.899
        
        hpt = self.add( 'hpt', Turbine())
        hpt.eff = .913
        hpt.PR = 4
        
        lpt = self.add( 'lpt', Turbine())
        lpt.eff = .93
        lpt.PR = 4
        
        prinoz = self.add( 'prinoz', Nozzle())
        self.connect('fc.Fl_O.Ps', 'prinoz.PsExh')    
        
        
        #inter component connections
        self.connect( 'fc.Fl_O', 'inlet.Fl_I' )
        self.connect( 'inlet.Fl_O', 'fan.Fl_I' )
        self.connect( 'fan.Fl_O', 'split.Fl_I' )
        self.connect( 'split.Fl_O2', 'bypduct.Fl_I' )
        self.connect( 'bypduct.Fl_O', 'bypnoz.Fl_I' )
        self.connect( 'split.Fl_O1', 'lpc.Fl_I' )
        self.connect( 'lpc.Fl_O', 'hpc.Fl_I' )
        self.connect( 'hpc.Fl_O', 'burner.Fl_I' )
        self.connect( 'burner.Fl_O',  'hpt.Fl_I')
        self.connect( 'hpt.Fl_O', 'lpt.Fl_I' )
        self.connect( 'lpt.Fl_O', 'prinoz.Fl_I' )
        self.connect( 'hpc.Fl_bld1', 'hpt.Fl_bld1' )
        self.connect( 'hpc.Fl_bld2', 'hpt.Fl_bld2' )
     
        driver = self.driver
        comp_list = ['fc','inlet', 'fan',
            'split','bypduct','bypnoz',
            'lpc']
            #'hpc' ]
            #'burner']
            #'hpt', 'lpt', 'prinoz']

        solver = self.add('solver',BroydenSolver())

        solver.workflow.add( comp_list )
        driver.workflow.add('solver')

from collections import OrderedDict
TF1 = Turbofan()

TF1.run()

print TF1.fc.Fl_O.Ps
print TF1.bypduct.Fl_O.ht
print TF1.bypduct.Fl_O.Tt
print TF1.bypduct.Fl_O.Pt