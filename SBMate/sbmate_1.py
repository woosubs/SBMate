# sbmate.py
# calculate annotation scores

import pandas as pd
from SBMate import sbml_annotation as sa
from SBMate.metric_calculator import MetricCalculator


class AnnotationMetrics(object):
  """
  Collects model annotations
  calculates three scores:
  1. coverage
  2. consistency
  3. specificity

  Attributes
  ----------
  annotations: sbml_annotation.SortedSBMLAnnotation 
      Sorted annotations for each knowledge resource.
  calculatorDf: dataframe of metrics. 
  """
  def __init__(self, model_file, metric_calculator_cls=None):
    """
    Parameters
    ----------
    model_file: str 
        Address/name of the .xml model file
    """
    self.annotations = sa.SortedSBMLAnnotation(file=model_file)
    if metric_calculator_cls is None:
      metric_calculator_cls = MetricCalculator
    calculator = metric_calculator_cls(annotations=self.annotations, model_name=model_file)
    self.metrics_df = calculator.calculate()


def _getMetricsReport(metrics_df):
  """
  Create a string report for
  an AnnotationMetrics class.

  Parameters
  ----------
  metrics_df: pandas.DataFrame
      A one-row dataframe with metrics.
      Index is model name. 

  Returns
  -------
  '': str
      Report summarizing the metrics df.
  """
  # model_name = metrics_tuple[0]
  # metrics_class = metrics_tuple[1]
  report = ["Summary of Metrics (%s)\n----------------------\n" % metrics_df.index[0]]
  report = report + ["%s: %s\n" % (col, metrics_df[col][0]) for col in metrics_df]
  report.append("----------------------\n")
  return ('').join(report)

def _getMetricsTable(metrics_df):
  """
  Create a table (data frame) for
  an AnnotationMetrics class.

  Parameters
  ----------
  metrics_df: pandas.DataFrame
      A data frame with metrics.
      Index is model name. 

  Returns
  -------
  table: pandas.DataFrame
      DataFrame summarizing metrics
  """
  return metrics_df

def getMetrics(file, output="report"):
  """
  Using the AnnotationMetrics class,
  produces report on the three metrics.

  Parameters
  ----------
  file: str/str-list
      Address(es) of model file (.xml).
      Should be string or list of string.
  output: str
      The type of output ("report" or "table").

  Returns
  --------
  res: str / pandas.DataFrame / None
      Final report (summary) of the model. 
      Return None if input type is incorrect. 
  """

  if isinstance(file, str):
    file_list = [file]
  elif isinstance(file, list):
    if all([isinstance(one_file, str) for one_file in file]):
      file_list = file
    else:
      return None
  else:
    return None

  metrics_tuple_list = [AnnotationMetrics(model_file=one_file) for one_file in file_list]
  if output=="report":
    res_list = [_getMetricsReport(m.metrics_df) for m in metrics_tuple_list]
    res = ('\n').join(res_list)
  elif output=="table":
    res_list = [_getMetricsTable(m.metrics_df) for m in metrics_tuple_list]
    res = pd.concat(res_list)
  return res



