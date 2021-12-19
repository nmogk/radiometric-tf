import numpy as np
from scipy.integrate import quad

class Sample:
    def __init__(self, parent, sample_time, inheritance = 0):
        self.parent = parent
        self.sample_time = sample_time
        self.inheritance = inheritance

    def initial_excess(self, model):
        return 0 if self.inheritance == 0 else self.inheritance * self.parent.get_apparent_age(model, self.sample_time)

    def get_apparent_age(self, model, time = 0):
        return model.H(self.sample_time) + self.initial_excess(model) - model.H(time) if time <= self.sample_time else self.parent.get_apparent_age(model, time)

    def get_apparent_ybp(self, model, time = 0):
        return model.invert(self.get_apparent_age(model, time))

class Reservoir(Sample):
    def __init__(self, parent, sample_time, inheritance = 0, relaxation = 0):
        Sample.__init__(self, parent, sample_time, inheritance)
        self.relaxation = relaxation

    def get_sample(self, sample_time, inheritance = 0):
        return Sample(self, sample_time, inheritance)

    def derive_reservoir(self, sample_time, inheritance = 0, relaxation = 0):
        return Reservoir(self, sample_time, inheritance, relaxation)

    def get_apparent_age(self, model, time = 0):
        if time > self.sample_time: # If requested time is before the sampling event, then ask the parent first
            return self.parent.get_apparent_age(model, time)

        initial_excess = model.H(self.sample_time) + self.initial_excess(model) # Saving the value, as this call traverses a tree with integrations
        initial_relaxation = initial_excess * ( 1 - np.exp( self.relaxation * (time - self.sample_time) ))
        episodic_relaxation = -self.relaxation * np.exp(self.relaxation * time) * quad( lambda tau: np.exp( -self.relaxation * tau ) * model.H(tau), time, self.sample_time )[0]
        return initial_excess - initial_relaxation - episodic_relaxation - model.H(time)

class PrimordialSource(Reservoir):
    def __init__(self, initial_apparent_age = 0, initial_time = 0):
        # An initial time of 0 causes this object to ignore model analysis and remains perpetually at the set initial_apparent_age
        self.initial_time = initial_time
        self.initial_apparent_age = initial_apparent_age

    def get_apparent_age(self, model, time = 0):
        if self.initial_time == 0:
            return self.initial_apparent_age
        return self.initial_apparent_age + model.H(self.initial_time) - model.H(time)