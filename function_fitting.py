import numpy, scipy, matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.optimize import differential_evolution
import warnings

title = ""
xData = numpy.array([<data>])
yData = numpy.array([<data>])

def func(x, a, b, n): # Sigmoid A With Offset from zunzun.com
    return  a + b*(x**-n)

# function for genetic algorithm to minimize (sum of squared error)
def sumOfSquaredError(parameterTuple):
    warnings.filterwarnings("ignore") # do not print warnings by genetic algorithm
    val = func(xData, *parameterTuple)
    return numpy.sum((yData - val) ** 2.0)

def generate_Initial_Parameters():
    # min and max used for bounds
    maxX = max(xData)
    minX = min(xData)
    maxY = max(yData)
    minY = min(yData)
    parameterBounds = []
    parameterBounds.append([-700, 500]) # search bounds for a
    parameterBounds.append([-700, 500]) # search bounds for b
    parameterBounds.append([-700, 500]) # search bounds for Offset
    # "seed" the numpy random number generator for repeatable results
    result = differential_evolution(sumOfSquaredError, parameterBounds, seed=3)
    return result.x

# generate initial parameter values
geneticParameters = generate_Initial_Parameters()

# curve fit the test data
fittedParameters, pcov = curve_fit(func, xData, yData, geneticParameters, maxfev=100000)
print('Parameters', fittedParameters)
modelPredictions = func(xData, *fittedParameters)
absError = modelPredictions - yData
SE = numpy.square(absError) # squared errors
MSE = numpy.mean(SE) # mean squared errors
RMSE = numpy.sqrt(MSE) # Root Mean Squared Error, RMSE
Rsquared = 1.0 - (numpy.var(absError) / numpy.var(yData))
print('RMSE:', RMSE)
print('R-squared:', Rsquared)

##########################################################
# graphics output section
def ModelAndScatterPlot(graphWidth, graphHeight):
    f = plt.figure(figsize=(graphWidth/100.0, graphHeight/100.0), dpi=100)
    axes = f.add_subplot(111)
    # first the raw data as a scatter plot
    axes.plot(xData, yData,  'D')
    # create data for the fitted equation plot
    xModel = numpy.linspace(min(xData), max(xData))
    yModel = func(xModel, *fittedParameters)
    # now the model as a line plot
    axes.plot(xModel, yModel)

    axes.set_title(title)
    axes.set_xlabel('$\eta$') # X axis data label
    axes.set_ylabel('Energy / Eh') # Y axis data label
    plt.savefig(title)
    plt.close('all') # clean up after using pyplot
graphWidth = 800
graphHeight = 600
ModelAndScatterPlot(graphWidth, graphHeight)
