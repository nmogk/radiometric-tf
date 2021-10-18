import numpy as np

class RadiometricTransferFunction:
    """
    Classes:
        DateHelper: Provide calendar conversions and printing support for calendar dates

        UCHelper: Provide uniformitarian chronostratigraphic column names and printing support of radiometric ages

    Functions:
        set_rtf: set the radiometric transfer function

        H: radiometric transfer function

        Xi: acceleration factor (derivative of H)

        invert: inverse of H

        flood_radiometric_range: lower and upper radiometric bounds of the Flood event

        creation_radiometric_range: lower and upper radiometric bounds of the Creation event

        antediluvian_radiometric_range: lower and upper radiometric bounds of the Antediluvian period

        modern_radiometric_range: lower and upper radiometric bounds of the modern period

        erodeozoic_radiometric_range: lower and upper radiometric bounds of the erosive event

        plot_standard: get a standard set of plots for viewing models
    """

    class DateHelper:
        """
        DateHelper objects take calendar dates and allow them to be converted to other calendars or pretty-printed.

        The string output of the DateHelper object includes all calendar systems.

        Numerical dates can be obtained from the object by using the ybp, am, ad, and bc attributes.

        Functions:
            get_ad_bc: Get the time in the standard calendar format with the year and date label (AD/BC) in a 2-tuple.

            get_special: Get the time string in terms of days of the Creation or Flood events if applicable.
        """

        def __init__(self, outer, ybp, present=2000): 
            """
            Initialize DateHelper object from numerical date and parent object with event calendar information.

            Args:
                outer: an object which includes event calendar information, such as a RadiometricTransferFunction object or another DateHelper

                ybp: the input time in years before present

                present: time of 0 ybp, default 2000(AD)
            """

            self.ybp = ybp
            self.present = present
            self.flood_start_ybp = outer.flood_start_ybp
            self.flood_end_ybp = outer.flood_end_ybp
            self.max_ybp = outer.max_ybp
            self.am = self.max_ybp - self.ybp + 1 # Calendar systems do not have year 0
            self.ad = self.present - self.ybp + 1  # Calendar systems do not have year 0
            self.bc = self.ybp - self.present + 1  # Calendar systems do not have year 0

        def __float__(self):
            return self.ybp

        def __repr__(self):
            return 'DateHelper({})'.format(self.ybp)

        def __str__(self):
            year, adbc = self.get_ad_bc()
            special = self.get_special()
            return '{} YBP\n{} AM\n{} {}{}'.format(int(self.ybp), int(self.am), year, adbc, '\n' + special if len(special) > 0 else special)

        def __add__(self, other):
            return RadiometricTransferFunction.DateHelper(self, self.ybp + float(other))

        def __sub__(self, other):
            return RadiometricTransferFunction.DateHelper(self, self.ybp - float(other))

        def get_ad_bc(self):
            """
            Get the time in the standard calendar format with the year and date label (AD/BC) in a 2-tuple.
            """

            if self.bc >= 1:
                return (int(self.bc), 'BC')
            else:
                return (int(self.ad), 'AD')

        def get_special(self):
            """
            Get the time string in terms of days of the Creation or Flood events if applicable.
            """

            day = 1/365.2425
            if  self.max_ybp - self.ybp <= 7 * day:
                return 'Creation Day {}'.format(int(1+(self.max_ybp - self.ybp)/day))
            elif self.ybp <= self.flood_start_ybp and self.ybp >= self.flood_end_ybp:
                return 'Flood day {}'.format(int(1+(self.flood_start_ybp - self.ybp)/day))
            else:
                return ''

    class UCHelper:
        """
        UCHelper objects take radiometric dates and finds UC time period information.

        The string representation is the numerical value of the object labeled in Ma. Not all UC time
        intervals are defined. Only in the Cenozoic and Carboniferous are Epochs defined. Ediacaran
        is the only preCambrian period, and there are no Archean Eras defined. If a particular unit
        is defined, all of the longer units are also defined. Attributes corresponding to units in 
        decreasing significance are eon, era, period, epoch.

        Functions:
            get_brackets: returns a 2-tuple with the UC bounding dates of the enclosing unit.

            get_unit: returns the name of the enclosing UC unit
        """

        def __init__(self, age):
            self.age = age

            if age <= 11700:
                self.epoch = 'Holocene'
            elif age <= 2.58e6:
                self.epoch = 'Pleistocene' 
            elif age <= 5.333e6:
                self.epoch = 'Pliocene' 
            elif age <= 23.03e6:
                self.epoch = 'Miocene' 
            elif age <= 33.9e6:
                self.epoch = 'Oligocene' 
            elif age <= 56e6:
                self.epoch = 'Eocene' 
            elif age <= 66e6:
                self.epoch = 'Paleocene' 
            elif age > 298.9e6 and age <= 323.2e6:
                self.epoch = 'Pennsylvanian'
            elif age > 298.9e6 and age <= 358.9e6:
                self.epoch = 'Mississippian'

            if age <= 2.58e6:
                self.period = 'Quaternary'
            elif age <= 23.3e6:
                self.period = 'Neogene' 
            elif age <= 66e6:
                self.period = 'Paleogene' 
            elif age <= 145e6:
                self.period = 'Cretaceous' 
            elif age <= 201.6e6:
                self.period = 'Jurassic' 
            elif age <= 251.902e6:
                self.period = 'Triassic' 
            elif age <= 298.9e6:
                self.period = 'Permian' 
            elif age <= 358.9e6:
                self.period = 'Carboniferous' 
            elif age <= 419.2e6:
                self.period = 'Devonian' 
            elif age <= 443.8e6:
                self.period = 'Silurian' 
            elif age <= 485.4e6:
                self.period = 'Ordovician' 
            elif age <= 541e6:
                self.period = 'Cambrian' 
            elif age <= 635e6:
                self.period = 'Ediacaran'

            if age <= 66e6:
                self.era = 'Cenozoic'
            elif age <= 251.9e6:
                self.era = 'Mesozoic'
            elif age <= 541e6:
                self.era = 'Paleozoic' 
            elif age <= 1000e6:
                self.era = 'Neo-proterozoic' 
            elif age <= 1600e6:
                self.era = 'Meso-proterozoic' 
            elif age <= 2500e6:
                self.era = 'Paleo-proterozoic'

            if age <= 541e6:
                self.eon = 'Phanerozoic'
            elif age <= 2500e6:
                self.eon = 'Proterozoic'
            elif age <= 3600e6:
                self.eon = 'Archean'
            elif age <= 4600e6:
                self.eon = 'Hadean'

        def __float__(self):
            return self.age 

        def __repr__(self):
            return 'UCHelper({})'.format(self.age)

        def __str__(self):
            return '{} Ma'.format(self.age/1e6)

        def get_brackets(self, level='period'):
            """
            Get a 2-tuple with the lower and upper UC bounding dates of the enclosing unit.

            Args:
                level: specifies which level of unit to form brackets for. One of "eon", "era", "period" (default) or "epoch".

            Raises:
                ValueError: if the specified level has not been defined.

            Returns:
                A 2-tuple with the lower and upper bounds of the UC unit in anum
            """

            if not hasattr(self, level):
                raise ValueError('Age must be have unit defined to get {}.'.format(level))

            # Epoch only defined for Cenozoic and Carboniferous
            epoch_brackets = [0, 11700, 2.58e6, 5.333e6, 23.03e6, 33.9e6, 56e6, 66e6, 298.9e6, 323.2e6, 358.9e6]

            # Periods not defined earlier than Ediacaran
            period_brackets = [2.58e6, 23.3e6, 66e6, 145e6, 201.6e6, 251.902e6, 298.9e6, 358.9e6, 419.2e6, 443.8e6, 485.4e6, 541e6, 635e6]

            # Eras not defined before Proterozoic
            era_brackets = [0, 66e6, 251.9e6, 541e6, 1000e6, 1600e6, 2500e6]

            eon_brackets = [0, 541e6, 2500e6, 3600e6, 4600e6]

            if level == 'epoch':
                bracket = epoch_brackets
            elif level == 'period':
                bracket = period_brackets
            elif level == 'era':
                bracket = era_brackets
            else:
                bracket = eon_brackets

            for i in range(len(bracket)-1):
                if self.age > bracket[i] and self.age <= bracket[i+1]:
                    return bracket[i], bracket[i+1]

        def get_unit(self, subdivide = True, level = None):
            """
            Get the name of the UC unit represented by this object.

            Args:
                subdivide: flag which tells the function to interpret relative positions within the unit as "Start", "Early", "Middle", "Late", or "End". Default True

                level: specifies which level of unit to form brackets for. One of "eon", "era", "period" or "epoch". If left as None, then the default is to use the
                smalled defined unit.

            Returns:
                2-tuple with name of unit and the name of the unit type
            """

            if level is not None:
                reportable = level
            elif hasattr(self, 'epoch'):
                reportable = 'epoch'
            elif hasattr(self, 'period'):
                reportable = 'period'
            elif hasattr(self, 'era'):
                reportable = 'era'
            else:
                reportable = 'eon'

            if subdivide:
                brackets = self.get_brackets(reportable)
                percentage = (self.age - brackets[0])/(brackets[1] - brackets[0])

                if percentage < 0.05:
                    decorator = 'End '
                elif percentage <= 0.3:
                    decorator = 'Late '
                elif percentage <= 0.7:
                    decorator = 'Middle '
                elif percentage <= 0.95:
                    decorator = 'Early '
                else:
                    decorator = 'Start '  
            else:
                decorator = ''

            return '{}{}'.format(decorator, self.__dict__[reportable]), reportable

    def __init__(self, **kwargs):
        '''
        Create a RadiometricTransferFunction object

        This constructor sets attributes required for the RTF object with defaults that just work, but
        don't provide much extra information in the description fields. Conversions using the RTF object
        cannot be done after initialization until the set_rtf function is called. All user supplied
        keywords are added to the object irregardless of their use in this module, so objects can be
        extended with additional information. Note that tiepoints, max_measured_age, and laws are reset
        by set_rtf when called.

        Args:
            **name: the name of the model

            **reference: published reference which describes the model

            **description: a description of how the model is constructed
            
            **family: the family of models to which this one belongs

            **model_class: characteristics of accelerated nuclear decay with respect to the Flood

            **termination: time period of accelerated nuclear decay termination

            **laws: number of decay regimes in the model

            **isotope_system: isotopic system to which model applies 

            **max_ybp: maximum calendar years before present in the model domain

            **flood_start_ybp: calendar year with fraction of the start of the Flood

            **flood_end_ybp: calendar year with fraction of the end of the Flood

            **max_measured_age: maximum radiometric age in the range of the model

            **tiepoints: list of time points which separate the function into its component regimes
        '''

        # Set default values
        self.name = 'User-defined model'
        self.reference = 'n/a'
        self.description = 'This is a default model which does not include accelerated nuclear decay. Set a model by calling the set_rtf function.'
        self.family = 'n/a'
        self.model_class = 'uniform'
        self.termination = 'n/a'
        self.laws = 1
        self.isotope_system = 'generic'
        self.max_ybp = 6000.
        self.flood_start_ybp = 4301.
        self.flood_end_ybp = self.flood_start_ybp - 1
        self.max_measured_age = self.max_ybp
        self.scale_factor = 1.
        self.tiepoints = [0, self.max_ybp]
        self.H = lambda: (_ for _ in ()).throw(Exception('H: set_rtf must be called before attempting to use a convertion'))
        self.__invert__ = self.__binary_search_invert__
        self.__xi__ = self.__forward_difference_xi__

        # Hoover up all of the input arguments
        self.__dict__.update(kwargs)

    def set_rtf(self, conditions = [0], laws = [lambda t:t], inverse = None, derivative = None):
        """
        Set the underlying model of the radiometric transfer function with inverse and derivative defined piecewise.

        This function must be called on a RadiometricTransferFunction instance before use. It is up to the user to 
        prepare the necessary functions which will be set. Minimally, the forward model must be set. There are default
        approaches to determining the inverse and derivative function. However, for high precision, the user may additionally
        specify the inverse and derivative functions to use. It is up to the use to ensure the consistency of these 
        other functions with the forward model.

        Derivatives that are constant must be formulated to give an array consisting of that constant for each input point
        Ex.
        > lambda t: [1 for x in t]

        Calling set_rft with no arguments will generate a uniform decay model over the entire domain as defined by the
        constructor, which has its own defaults for the necessary attributes.

        Args:
            conditions: list of points which separate the function into its component pieces. Including the minimum and maximum
            bounds, the number of segments between the conditions list should match the number of laws.

            laws: a list of functions which define the behavior of the RadiometricTransferFunction over the entire domain.

            inverse: a list of functions which define the piecewise inverse of laws. Defaults to None.

            derivative: a list of functions which define the piecewise derivative of laws. Defaults to None.

        Raises:
            ValueError: if the number of conditions or inverse or derivative functions do not match the number of laws.

        The attributes set by this function are listed below,
        Side Effects:
            H: callable radiometric transfer function defined by the conditions and laws.

            tiepoints: a list of points which separate the different conditions of the piecewise function. These may be
            modified from the input by appending the minimum and maximum bounds to the array.

            max_measured_age: the age returned by the H function at the maximum domain value.

            laws: the number of functions which defines H over its entire domain.

            inverse_tiepoints: the list of points which separate different conditions in the inverse of H. These are evaluated
            by running tiepoints through H. This is only set if an inverse is given in the input.

            invert: if an inverse is given in the input, then the invert function is set to use the given inverse rather than the default.

            xi: if a derivative is given in the input, then the xi function is set to use the given derivative rather than the default.
        """
        
        # Checks to ensure that the number of brackets for the piecewise function matches the number of functions to combine
        def check_numercy(ties, lawlist):
            if len(ties) - len(lawlist) != 1:
                raise ValueError('set_rtf: tiepoints brackets ({}) and laws ({}) do not match in number'.format(len(ties) - 1, len(lawlist)))

        # Takes a list of tiepoints and produces binary arrays for each test point representing which zone each falls into
        # Generator that gives an x by n array, where n is the number of piecewise function brackets
        def yield_conditions(x, ties):
            x = np.asanyarray(x, dtype=float)
            for i in range(len(ties) - 1):
                if i == 0:
                    yield ((x <= ties[i+1]))
                else:
                    yield ((x > ties[i]) & (x <= ties[i+1]))

        # Takes a list of laws (functions) and ties them together into a new list of functoins suth that they are piecewise continuous
        # Adds an offset to both the domain and the range to make it match up with the end of the prevoius neighbor
        def yield_laws(lawlist, ties):
            running_sum = 0
            for i, law in enumerate(lawlist):
                yield lambda z: law(z - ties[i]) + running_sum
                running_sum = running_sum + law(ties[i+1] - ties[i])

        # Same as above, but with no running sum since this the derivative is not necessarily continuous
        def yield_derivative_laws(lawlist, ties):
            for i, law in enumerate(lawlist):
                yield lambda z: law(z - ties[i])

        # Generates a function which evaluates inputs in a piece-wise manner defined by the tiepoints and the equations (laws) applicable at each time
        def piecewise(ties, lawlist):
            return lambda x: np.concatenate([func(np.asanyarray(x, dtype=float)[cond]) for cond, func in zip(yield_conditions(x, ties), yield_laws(lawlist, ties))])

        # Ensure that tie-points are in order from smallest to largest. Should be already, so "stable" sort is quick on an already sorted list
        sorted = np.sort(conditions, kind='stable') 

        # Check that the tiepoints do not go outside the domain
        if sorted[0] < 0. or sorted[-1] > self.max_ybp:
            raise ValueError('set_rtf: tiepoints brackets ({},{}) outside of maximum or minimum bounds ({},{})'.format(sorted[0], sorted[-1], 0, self.max_ybp))
        
        # Append the minimum and maximum values of the domain to the tiepoints if they are not already there.
        if 0. not in sorted:
            sorted = np.insert(sorted, 0, 0.)
        if self.max_ybp not in sorted:
            sorted = np.append(sorted, self.max_ybp)

        check_numercy(sorted, laws)
        
        # Update object values related to forward model (inverse must be done after this)
        self.tiepoints = sorted
        self.H = piecewise(self.tiepoints, laws) 
        self.max_measured_age = self.H(self.max_ybp)
        self.laws = len(laws)

        # Inverse and derivative follow the same pattern as the forward model
        if inverse is not None:
            self.inverse_tiepoints = self.H(self.tiepoints)

            if len(inverse) != len(laws):
                raise ValueError('set_rtf: The number of forward ({}) and reverse ({}) laws must be the same.'.format(self.laws, len(inverse)))
            check_numercy(self.inverse_tiepoints, inverse) # Technically this check catches the above, but the previous one is more helpful

            self.__invert__ = piecewise(self.inverse_tiepoints, inverse)

        if derivative is not None:
            if len(derivative) != len(laws):
                raise ValueError('set_rtf: The number of functions ({}) and derivatives ({}) must be the same.'.format(self.laws, len(derivative)))
            check_numercy(self.tiepoints, derivative) # Technically this check catches the above, but the previous one is more helpful

            self.__xi__ = lambda x: np.concatenate([func(np.asanyarray(x, dtype=float)[cond]) for cond, func in zip(yield_conditions(x, self.tiepoints), yield_derivative_laws(derivative, self.tiepoints))])

    def Xi(self, t = None, points = 100):
        """
        Find the acceleration factor (derivative of radiometric transfer function).

        Unless a derivative function has been explicitly set in set_rtf, this funtion uses the forward difference 
        algorithm to compute an approximate derivative of the radiometric transfer function. Forward difference
        causes the last input point to be excised in the output.

        Args:
            t: time points to evaluate the acceleration factor at.  If no domain points
            are specified by the user, then the funciton returns points from the entire domain spaced such that there
            are an equal number of points in each law regime.

            points: number of points to allocate for each regime with default t argument.

        Returns:
            A 2-tuple of lists with the actual t value used and the value of xi at each point.
        """

        if t is not None:
            tval = t
        else:
            tval = np.concatenate([np.linspace(a, b, points, endpoint=False) for a, b in zip(self.tiepoints[:-1], self.tiepoints[1:])])
            tval = np.append(tval, self.tiepoints[-1])

        results = self.__xi__(tval)
        if len(results) < len(tval):
            tval = tval[:-1] # Trim the t if using forward difference and it chopped one off
        return tval, results

    def __forward_difference_xi__(self, t):
        data = self.H(t) # Get the values to perform the difference on
        diff = (data[1:] - data[:-1])/(t[1:] - t[:-1])
        return diff # Forward difference drops the last value, trip input to match
        
    def flood_radiometric_range(self):
        """Get the lower and upper bound radiometric dates for the Flood event."""
        return self.H(self.flood_end_ybp)[0], self.H(self.flood_start_ybp)[0]

    def creation_radiometric_range(self):
        """Get the lower and upper bound radiometric dates for the Creation event."""
        return self.H(self.max_ybp - 7/365.2425)[0], self.H(self.max_ybp)[0]

    def antediluvian_radiometric_range(self):
        """Get the lower and upper bound radiometric dates for the Antediluvian era."""
        return self.H(self.max_ybp)[0], self.H(self.flood_start_ybp)[0]

    def modern_radiometric_range(self):
        """Get the lower and upper bound radiometric dates for the Modern era."""
        return self.H(0)[0], self.H(self.flood_end_ybp)[0]

    def erodeozoic_radiometric_range(self):
        """Get the lower and upper bound radiometric dates for the erosive later half of the Flood event."""
        return self.H(self.flood_end_ybp+(self.flood_start_ybp - self.flood_end_ybp)/2.)[0], self.H(self.flood_end_ybp)[0]

    def invert(self, measured_date, meas_error=None, **kwargs):
        """
        Convert a measured radiometric date to a calendar date.

        Args:
            measured_date: numerical radoimetric date
            meas_error: symmetrical or two-sided error value of the measured date. Two-sided error should be (lower, upper). Defaults to None.
            **tol: error tolerance for the default binary search invert algorithm evalutated against measured_date. Defaults to 0.001.
            **max_iterations: maximum iterations for the default binary search algorithm

        Returns:
            measured_date converted to calendar time. All results are returned as DateHelper objects which provide convenience 
            methods for converting between calendar systems.

            If meas_error is specified, invert will additionally return a 2-tuple of the lower and upper dates, as DateHelper objects.

        Raises:
            ValueError: if the measured date is outside the defined radiometric range of the model.
        """
        
        if measured_date < 0 or measured_date > self.max_measured_age:
            raise ValueError('invert: {} is outside of the boundary dates ({}, {})'.format(measured_date, 0, self.max_measured_age))

        if hasattr(self, 'inverse_tiepoints'):
            center_result = self.__invert__(measured_date)
        else:
            center_result = self.__invert__(measured_date, start=0, end=self.max_ybp, **kwargs)

        if meas_error is None:
            return self.DateHelper(self, center_result)
        
        err_array = np.array(meas_error)
        left = measured_date - err_array[0]
        right = measured_date - err_array[0 if len(err_array) == 1 else 1]

        if hasattr(self, 'inverse_tiepoints'):
            return self.DateHelper(self, center_result), (self.DateHelper(self, self.__invert__(left)), self.DateHelper(self, self.__invert__(right)))
        else:
            return self.DateHelper(self, center_result), (self.DateHelper(self, self.__invert__(left, 0, center_result, **kwargs)), self.DateHelper(self, self.__invert__(right, center_result, self.max_ybp, **kwargs)))
        
    def __binary_search_invert__(self, measured_date, start, end, tol=0.001, max_iterations=100):
        # This is a default binary search implementation of an inverse function. This is possible because the RTF is 
        # guaranteed to be a bijection and strictly increasing. This function will be overridden by an explicit inverse being set
        check = True
        mid = 0
        count = 0
        while check: # Do while loop
            count += 1
            mid = (end - start)/2. + start
            value = self.H(mid)[0]
            if value < measured_date:
                start = mid
            else:
                end = mid

            # Ends when either the found value is within tol or when the maximum iterations is encountered
            check = abs(value - measured_date) > tol and count < max_iterations

        return mid

    def __str__(self):
        import textwrap
        lables1 = ''.join(map(lambda s: s.ljust(29)+'{}\n',['Family:','Model Class:','Termination behavior:','Model Cardinality (Laws):','Isotope system:']))
        lables2 = ''.join(map(lambda s: s.ljust(29)+'{}\n',['Pre-Flood/Flood Boundary:', 'Flood/Post-Flood Boundary:']))
        lables3 = ''.join(map(lambda s: s.ljust(29)+'{:e}\n',['Start-Flood Radiometric Age:','Mid-Flood Radiometric Age:','End-Flood Radiometric Age:','Flood Radiometric Range:','Radiometric Spectrum Gap:']))

        values1 = [self.family, self.model_class, self.termination, self.laws, self.isotope_system]
        end, start= self.flood_radiometric_range()
        mid, _ = self.erodeozoic_radiometric_range()
        values2 = [self.UCHelper(start).get_unit()[0], self.UCHelper(end).get_unit()[0]]
        values3 = [start, mid, end, start-end, mid-end]

        allLabels = lables1 + '\n' + lables2 + lables3
        allValues = values1 + values2 + values3
        
        return 'Name: ' + self.name + '\n' + '=' * 80 + '\n' + textwrap.fill('Reference: ' + self.reference, width=80) + '\n\n' + textwrap.fill(self.description, width=80) + '\n' + '=' * 80 + '\n' + allLabels.format(*allValues)

    def __repr__(self):
        return 'RadiometricTransferFunction(name={}, tiepoints={}, max_measured_age={}, isotope_system={})'.format(self.name, self.tiepoints, self.max_measured_age, self.isotope_system)

    def plot_standard(self, style='ybp'):
        """
        Get standard Flood and Antediluvian period plots with the radiometric transfer function and acceleration factor displayed.

        Args:
            style: calendar system to display domain in, one of "ybp" (default), "bc", or "am".

        Returns:
            List of axes in the plots. You have to plt.show() yourself.
        """
        
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        import warnings
        # Unfortunately, this warning is coming from matplotlib directly. Not something I am using explicitly
        warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning) 
        
        t = np.linspace(self.flood_end_ybp-0.5, self.flood_start_ybp+0.5, 1000)
        t, x = self.Xi(t)
        y = self.H(t)
        t = [self.DateHelper(self, t).__getattribute__(style) for t in t]
        
        fig, ax_rtf = plt.subplots(num='RTF Flood')
        color1 = 'forestgreen'
        ax_rtf.set_xlabel('time ({})'.format(style.upper()))
        ax_rtf.set_ylabel('measured age (Ma)', color=color1)  
        ax_rtf.tick_params(axis='y', labelcolor=color1)
        ax_rtf.grid(True)
        ax_rtf.set_title('Flood view')

        flood_start_styled = self.DateHelper(self, self.flood_start_ybp).__getattribute__(style)
        flood_end_styled = self.DateHelper(self, self.flood_end_ybp).__getattribute__(style)
        ax_rtf.semilogy(t, y/1e6, color=color1)
        ax_rtf.plot((flood_end_styled, flood_start_styled), [y/1e6 for y in self.flood_radiometric_range()], 'bo')

        ax_rtf.annotate('Flood start\n{:.3e} Ma'.format(self.flood_radiometric_range()[1]/1e6),
            xy=(flood_start_styled, self.flood_radiometric_range()[1]/1e6),
            xytext=(00, -60), textcoords='offset pixels',
            horizontalalignment='right' if style == 'am' else 'left',
            verticalalignment='bottom',
            arrowprops=dict(arrowstyle="-"))

        ax_rtf.annotate('Flood end\n{:.3e} Ma'.format(self.flood_radiometric_range()[0]/1e6),
            xy=(flood_end_styled, self.flood_radiometric_range()[0]/1e6),
            xytext=(00, 60), textcoords='offset pixels',
            horizontalalignment='left' if style == 'am' else 'right',
            verticalalignment='top',
            arrowprops=dict(arrowstyle="-"))

        
        ax_rtf.set_facecolor('#FFFFFF00')
        
        ax_xi = ax_rtf.twinx()  # instantiate a second axes that shares the same x-axis

        color2 = 'tab:orange'
        ax_xi.set_ylabel('acceleration factor', color=color2) # we already handled the x-label with ax1
        ax_xi.tick_params(axis='y', labelcolor=color2)
        ax_xi.semilogy(t, x, '.', color=color2, zorder=15)
        ax_rtf.zorder = 20
        ax_xi.zorder = 10

        lbound = self.flood_start_ybp if style == 'am' else self.flood_end_ybp
        leftside = self.DateHelper(self, lbound).__getattribute__(style)
        
        rect = patches.Rectangle((leftside, 0), self.flood_start_ybp-self.flood_end_ybp, 1e15, facecolor='lightskyblue')
        limitsave = ax_xi.get_ylim()
        ax_xi.add_patch(rect)
        ax_xi.set_ylim(limitsave)
        
        fig.autofmt_xdate()
        fig.suptitle('{} Transfer Function'.format(self.name))

        #--------------------------------------------------------------------------------------------------

        t = np.concatenate((np.linspace(self.flood_start_ybp-301, self.flood_start_ybp, 10000, endpoint=False), np.linspace(self.flood_start_ybp, self.max_ybp, 1000)))
        t, x = self.Xi(t)
        y = self.H(t)
        t = [self.DateHelper(self, t).__getattribute__(style) for t in t]
        
        fig2, ax_rtfa = plt.subplots(num='RTF Antediluvian')
        ax_rtfa.set_xlabel('time ({})'.format(style.upper()))
        ax_rtfa.set_ylabel('measured age (Ma)', color=color1)  
        ax_rtfa.tick_params(axis='y', labelcolor=color1)
        ax_rtfa.grid(True)
        ax_rtfa.set_title('Antediluvian view')

        creation_start_styled = self.DateHelper(self, self.max_ybp).__getattribute__(style)
        creation_end_styled = self.DateHelper(self, self.max_ybp - 7/365.2425).__getattribute__(style)
        ax_rtfa.semilogy(t, y/1e6, color=color1)
        ax_rtfa.plot((creation_end_styled, creation_start_styled, flood_end_styled, flood_start_styled), [y/1e6 for y in np.concatenate((self.creation_radiometric_range(), self.flood_radiometric_range()))], 'bo')

        ax_rtfa.annotate('Flood start\n{:.3e} Ma'.format(self.flood_radiometric_range()[1]/1e6),
            xy=(flood_start_styled, self.flood_radiometric_range()[1]/1e6),
            xytext=(00, -90), textcoords='offset pixels',
            horizontalalignment='right' if style == 'am' else 'left',
            verticalalignment='bottom',
            arrowprops=dict(arrowstyle="-"))

        ax_rtfa.annotate('Creation end\n{:.3e} Ma'.format(self.creation_radiometric_range()[0]/1e6),
            xy=(creation_end_styled, self.creation_radiometric_range()[0]/1e6),
            xytext=(00, -60), textcoords='offset pixels',
            horizontalalignment='left' if style == 'am' else 'right',
            verticalalignment='top',
            arrowprops=dict(arrowstyle="-"))

        
        ax_rtfa.set_facecolor('#FFFFFF00')
        
        ax_xia = ax_rtfa.twinx()  # instantiate a second axes that shares the same x-axis

        ax_xia.set_ylabel('acceleration factor', color=color2) # we already handled the x-label with ax1
        ax_xia.tick_params(axis='y', labelcolor=color2)
        ax_xia.semilogy(t, x, '.', color=color2, zorder=15)
        ax_rtfa.zorder = 20
        ax_xia.zorder = 10

        lbound = self.flood_start_ybp if style == 'am' else self.flood_end_ybp
        leftside = self.DateHelper(self, lbound).__getattribute__(style)
        
        rect = patches.Rectangle((leftside, 0), self.flood_start_ybp-self.flood_end_ybp, 1e15, facecolor='lightskyblue')
        limitsave = ax_xia.get_ylim()
        ax_xia.add_patch(rect)
        ax_xia.set_ylim(limitsave)
        
        fig2.autofmt_xdate()
        fig2.suptitle('{} Transfer Function'.format(self.name))
        
        return [ax_rtf, ax_xi, ax_rtfa, ax_xia]

def init_from_file(filename):
    """
    Import a radiometric transfer function model from a JSON file.
    
    Args:
        filename: name of the file to load a model from. 

    Returns:
        ready-to-use instance of the RadiometricTransferFunction model

    Raises:
        IOError: If the input file does not exist

        TypeError: If the input file does not contain the specific JSON attributes expected. See below.
    
    The contents of the file must be a JSON object with the "tiepoints" and "model" attributes. If these are not present
    a TypeError is raised. "tiepoints" must be a list of floats representing the boundaries of the piecewise model
    definition. "model" must be a list of strings with lambda functions defining the functions for each segment. Offsets
    to make the model continuous (including on the domain) are calculated automatically and are not required.

    All other attributes of the JSON file are passed to the constructor. This function initializes the RadiometricTransferFunction
    object and calls set_rtf on it with the supplied model information and returns the ready-to-use object.

    WARNING! This function runs eval() on the items in the "model" attribute. Do not use on untrusted files.
    """

    # Only import these if the user needs them
    import json
    import os

    # Check for file existence
    if not os.path.isfile(filename):
        raise IOError('init_from_file: Error! {} doesn\'t exist'.format(filename))
    with open(filename, 'r') as read_file:
        indata = json.load(read_file)

    # This is the minimum info needed to instantiate the model. The defaults are otherwise usable
    if not isinstance(indata, dict) or 'tiepoints' not in indata or not isinstance(indata['tiepoints'], list) or 'model' not in indata or not isinstance(indata['model'], list):
        raise TypeError('init_from_file: This is not a recognized file type')
        
    model = RadiometricTransferFunction(**indata) # Pass all of the JSON attributes to the constructor

    if 'inverse' in indata and isinstance(indata['inverse'], list):
        eval_inverse = [eval(func) for func in indata['inverse']]
    else:
        eval_inverse = None

    if 'derivative' in indata and isinstance(indata['derivative'], list):
        eval_derivative = [eval(func) for func in indata['derivative']]
    else:
        eval_derivative = None

    model.set_rtf(indata['tiepoints'], [eval(func) for func in indata['model']], eval_inverse, eval_derivative) # Set the model info

    # To catch models which include a primordial signature, which is considered a law, but not part of the acceleration regime
    if 'laws' in indata and isinstance(indata['laws'], int):
        model.laws = indata['laws'];

    return model

def __commmand_line_interface__():
    # TODO prettier output, tabular view to compare two different models
    import argparse, textwrap
    parser = argparse.ArgumentParser(description='This is a program for working with radiometric transfer function models')
    parser.add_argument('infile', help='Name of formatted JSON file containing model description')
    parser.add_argument('-i', '--info', default=False, action='store_true', help="Print a table with standard model evaluation information")
    parser.add_argument('-c', '--cal2rad', nargs='*', metavar='DATE_YBP', help='Perform a conversion of the given dates to radiometric ages')
    parser.add_argument('-r','--rad2cal', nargs='*', metavar='RADM_AGE', help='Perform a conversion of the given radiometric ages to dates')
    parser.add_argument('-x','--accel', nargs='*', metavar='DATE_YBP', help='Get the acceleration factor for the given dates')
    parser.add_argument('-p', '--plot', default=False, action='store_true', help="Generate standard plots of the transfer function and acceleration factor")
    parser.add_argument('-f', '--format', choices=['am', 'bc', 'ybp'], default='ybp', help='Selects the calendar system used for displaying years. Default YBP (2000)')
    parser.add_argument('-w', default=True, action='store_false', help="Supress untrusted source warning.")
    # parser.add_argument('--verbose', default=False, action='store_true') # As of now, I have nothing to be wordy about
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args()
    
    if args.w:
        print(textwrap.fill('rtf.py: Warning! You are about to load info from a file which contains code that will be evaluated. \
This can harm your computer. Do not load files from an untrusted source. Manually inspect file for malicious code. \
You can supress this message and continue by invoking with the -w option', width=80))
        return

    cli_rtf = init_from_file(args.infile)

    if args.info:
        print(cli_rtf)

    if args.cal2rad is not None:
        print(cli_rtf.H(np.array(args.cal2rad, dtype=float)))

    if args.rad2cal is not None:
        print(cli_rtf.invert(np.array(args.rad2cal, dtype=float)).__getattribute__(args.format))

    if args.accel is not None:
        # Xi needs adjacent points to calculate the forward distance
        _, accel = cli_rtf.Xi(t=np.concatenate([np.linspace(x, x+0.001, 2) for x in np.array(args.accel, dtype=float)]))
        # Every other element contains the slope at our input values
        print(accel[::2])

    if args.plot:
        import matplotlib.pyplot as plt
        cli_rtf.plot_standard(style=args.format)
        plt.show()

if __name__ == '__main__':
    __commmand_line_interface__()