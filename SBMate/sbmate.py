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

  def __init__(self, model_file=None, metric_calculator_classes=None):
    """
    Parameters
    ----------
    model_file: str
        Address/name of the .xml model file
    metric_calculator_classes: list-type
    """
    # model file can take None
    if model_file is None:
      self.annotations = None
      self.metrics_df = None
    else:
      self.annotations = sa.SortedSBMLAnnotation(file=model_file)
      if metric_calculator_classes is None:
        metric_calculator_classes = []
      metric_calculator_classes.append(MetricCalculator)
      # Calculate a DataFrame for each metric calculator
      dfs = []
      # in case model_file is given as a path, get the last file name
      index_model_name = model_file.split('/')[-1]
      for cls in metric_calculator_classes:
        calculator = cls(annotations=self.annotations, model_name=index_model_name)
        dfs.append(calculator.calculate())
      # Merge the DataFrames
      self.metrics_df = pd.concat(dfs, axis=1)

  def _getMetricsReport(self):
    """
    Create a string report for
    an AnnotationMetrics class.

    Returns
    -------
    '': str
        Report summarizing the metrics df.
    """
    report = ["Summary of Metrics (%s)\n----------------------\n"
        % self.metrics_df.index[0]]
    report = report + ["%s: %s\n" % (col, self.metrics_df[col][0])
        for col in self.metrics_df]
    report.append("----------------------\n")
    return ('').join(report)

  @classmethod
  def getMetrics(cls, file, output="report"):
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

    # Throws ValueError if the file argument type is incorrect. 
    flag = False
    if isinstance(file, str):
      file_list = [file]
    elif isinstance(file, list):
      if all([isinstance(one_file, str) for one_file in file]):
        file_list = file
      else:
        flag = True
    else:
      flag = True
    if flag:
      raise ValueError("Should be a valid file name.")

    annotation_metrics_list = [cls(model_file=one_file) 
                               for one_file in file_list]
    if output == "report":
      res_list = [m._getMetricsReport() for m in annotation_metrics_list]
      res = ('\n').join(res_list)
    elif output=="table":
      res_list = [m.metrics_df for m in annotation_metrics_list]
      res = pd.concat(res_list)
    return res
