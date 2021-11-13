import pickle
import copy
import dictsort
from riskestimator_v2 import initialize, analyze
from probability import pb, pbx, conditional_pb_rv

initialize(r'fmea_mat')
analyze('SurfaceOps', ['Inaccurate'])

