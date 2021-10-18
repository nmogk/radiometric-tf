<!-- markdownlint-disable -->

<a href="..\rtf.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `rtf`





---

<a href="..\rtf.py#L732"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `init_from_file`

```python
init_from_file(filename)
```

Import a radiometric transfer function model from a JSON file. 



**Args:**
 
 - <b>`filename`</b>:  name of the file to load a model from.  



**Returns:**
 ready-to-use instance of the RadiometricTransferFunction model 



**Raises:**
 
 - <b>`IOError`</b>:  If the input file does not exist 


 - <b>`TypeError`</b>:  If the input file does not contain the specific JSON attributes expected. See below. 

The contents of the file must be a JSON object with the "tiepoints" and "model" attributes. If these are not present a TypeError is raised. "tiepoints" must be a list of floats representing the boundaries of the piecewise model definition. "model" must be a list of strings with lambda functions defining the functions for each segment. Offsets to make the model continuous (including on the domain) are calculated automatically and are not required. 

All other attributes of the JSON file are passed to the constructor. This function initializes the RadiometricTransferFunction object and calls set_rtf on it with the supplied model information and returns the ready-to-use object. 

WARNING! This function runs eval() on the items in the "model" attribute. Do not use on untrusted files. 


---

<a href="..\rtf.py#L3"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `RadiometricTransferFunction`
Classes:  DateHelper: Provide calendar conversions and printing support for calendar dates 

 UCHelper: Provide uniformitarian chronostratigraphic column names and printing support of radiometric ages 

Functions:  set_rtf: set the radiometric transfer function 

 H: radiometric transfer function 

 Xi: acceleration factor (derivative of H) 

 invert: inverse of H 

 flood_radiometric_range: lower and upper radiometric bounds of the Flood event 

 creation_radiometric_range: lower and upper radiometric bounds of the Creation event 

 antediluvian_radiometric_range: lower and upper radiometric bounds of the Antediluvian period 

 modern_radiometric_range: lower and upper radiometric bounds of the modern period 

 erodeozoic_radiometric_range: lower and upper radiometric bounds of the erosive event 

 plot_standard: get a standard set of plots for viewing models 

<a href="..\rtf.py#L288"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(**kwargs)
```

Create a RadiometricTransferFunction object 

This constructor sets attributes required for the RTF object with defaults that just work, but don't provide much extra information in the description fields. Conversions using the RTF object cannot be done after initialization until the set_rtf function is called. All user supplied keywords are added to the object irregardless of their use in this module, so objects can be extended with additional information. Note that tiepoints, max_measured_age, and laws are reset by set_rtf when called. 



**Args:**
 
 - <b>`**name`</b>:  the name of the model 


 - <b>`**reference`</b>:  published reference which describes the model 


 - <b>`**description`</b>:  a description of how the model is constructed 


 - <b>`**family`</b>:  the family of models to which this one belongs 


 - <b>`**model_class`</b>:  characteristics of accelerated nuclear decay with respect to the Flood 


 - <b>`**termination`</b>:  time period of accelerated nuclear decay termination 


 - <b>`**laws`</b>:  number of decay regimes in the model 


 - <b>`**isotope_system`</b>:  isotopic system to which model applies  


 - <b>`**max_ybp`</b>:  maximum calendar years before present in the model domain 


 - <b>`**flood_start_ybp`</b>:  calendar year with fraction of the start of the Flood 


 - <b>`**flood_end_ybp`</b>:  calendar year with fraction of the end of the Flood 


 - <b>`**max_measured_age`</b>:  maximum radiometric age in the range of the model 


 - <b>`**tiepoints`</b>:  list of time points which separate the function into its component regimes 




---

<a href="..\rtf.py#L468"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Xi`

```python
Xi(t=None, points=100)
```

Find the acceleration factor (derivative of radiometric transfer function). 

Unless a derivative function has been explicitly set in set_rtf, this funtion uses the forward difference  algorithm to compute an approximate derivative of the radiometric transfer function. Forward difference causes the last input point to be excised in the output. 



**Args:**
 
 - <b>`t`</b>:  time points to evaluate the acceleration factor at.  If no domain points are specified by the user, then the funciton returns points from the entire domain spaced such that there are an equal number of points in each law regime. 


 - <b>`points`</b>:  number of points to allocate for each regime with default t argument. 



**Returns:**
 A 2-tuple of lists with the actual t value used and the value of xi at each point. 

---

<a href="..\rtf.py#L511"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `antediluvian_radiometric_range`

```python
antediluvian_radiometric_range()
```

Get the lower and upper bound radiometric dates for the Antediluvian era. 

---

<a href="..\rtf.py#L507"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `creation_radiometric_range`

```python
creation_radiometric_range()
```

Get the lower and upper bound radiometric dates for the Creation event. 

---

<a href="..\rtf.py#L519"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `erodeozoic_radiometric_range`

```python
erodeozoic_radiometric_range()
```

Get the lower and upper bound radiometric dates for the erosive later half of the Flood event. 

---

<a href="..\rtf.py#L503"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `flood_radiometric_range`

```python
flood_radiometric_range()
```

Get the lower and upper bound radiometric dates for the Flood event. 

---

<a href="..\rtf.py#L523"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `invert`

```python
invert(measured_date, meas_error=None, **kwargs)
```

Convert a measured radiometric date to a calendar date. 



**Args:**
 
 - <b>`measured_date`</b>:  numerical radoimetric date 
 - <b>`meas_error`</b>:  symmetrical or two-sided error value of the measured date. Two-sided error should be (lower, upper). Defaults to None. 
 - <b>`**tol`</b>:  error tolerance for the default binary search invert algorithm evalutated against measured_date. Defaults to 0.001. 
 - <b>`**max_iterations`</b>:  maximum iterations for the default binary search algorithm 



**Returns:**
 measured_date converted to calendar time. All results are returned as DateHelper objects which provide convenience  methods for converting between calendar systems. 

If meas_error is specified, invert will additionally return a 2-tuple of the lower and upper dates, as DateHelper objects. 



**Raises:**
 
 - <b>`ValueError`</b>:  if the measured date is outside the defined radiometric range of the model. 

---

<a href="..\rtf.py#L515"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `modern_radiometric_range`

```python
modern_radiometric_range()
```

Get the lower and upper bound radiometric dates for the Modern era. 

---

<a href="..\rtf.py#L603"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `plot_standard`

```python
plot_standard(style='ybp')
```

Get standard Flood and Antediluvian period plots with the radiometric transfer function and acceleration factor displayed. 



**Args:**
 
 - <b>`style`</b>:  calendar system to display domain in, one of "ybp" (default), "bc", or "am". 



**Returns:**
 List of axes in the plots. You have to plt.show() yourself. 

---

<a href="..\rtf.py#L349"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `set_rtf`

```python
set_rtf(
    conditions=[0],
    laws=[<function RadiometricTransferFunction.<lambda> at 0x000000000316C430>],
    inverse=None,
    derivative=None
)
```

Set the underlying model of the radiometric transfer function with inverse and derivative defined piecewise. 

This function must be called on a RadiometricTransferFunction instance before use. It is up to the user to  prepare the necessary functions which will be set. Minimally, the forward model must be set. There are default approaches to determining the inverse and derivative function. However, for high precision, the user may additionally specify the inverse and derivative functions to use. It is up to the use to ensure the consistency of these  other functions with the forward model. 

Derivatives that are constant must be formulated to give an array consisting of that constant for each input point Ex. > lambda t: [1 for x in t] 

Calling set_rft with no arguments will generate a uniform decay model over the entire domain as defined by the constructor, which has its own defaults for the necessary attributes. 



**Args:**
 
 - <b>`conditions`</b>:  list of points which separate the function into its component pieces. Including the minimum and maximum bounds, the number of segments between the conditions list should match the number of laws. 


 - <b>`laws`</b>:  a list of functions which define the behavior of the RadiometricTransferFunction over the entire domain. 


 - <b>`inverse`</b>:  a list of functions which define the piecewise inverse of laws. Defaults to None. 


 - <b>`derivative`</b>:  a list of functions which define the piecewise derivative of laws. Defaults to None. 



**Raises:**
 
 - <b>`ValueError`</b>:  if the number of conditions or inverse or derivative functions do not match the number of laws. 

The attributes set by this function are listed below, Side Effects: 
 - <b>`H`</b>:  callable radiometric transfer function defined by the conditions and laws. 


 - <b>`tiepoints`</b>:  a list of points which separate the different conditions of the piecewise function. These may be modified from the input by appending the minimum and maximum bounds to the array. 


 - <b>`max_measured_age`</b>:  the age returned by the H function at the maximum domain value. 


 - <b>`laws`</b>:  the number of functions which defines H over its entire domain. 


 - <b>`inverse_tiepoints`</b>:  the list of points which separate different conditions in the inverse of H. These are evaluated by running tiepoints through H. This is only set if an inverse is given in the input. 


 - <b>`invert`</b>:  if an inverse is given in the input, then the invert function is set to use the given inverse rather than the default. 


 - <b>`xi`</b>:  if a derivative is given in the input, then the xi function is set to use the given derivative rather than the default. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
