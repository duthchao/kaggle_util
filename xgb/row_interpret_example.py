from xgb_util import get_row_interpret
import xgboost as xgb
from sklearn.datasets import load_boston


boston = load_boston()
dtr = xgb.DMatrix(boston.data,boston.target)
param = {}
param['objective'] = 'reg:linear'
param['silent'] = 1
param['nthread'] = 8
param['eval_metric'] = 'rmse'
param['base_score'] = 0.

param['learning_rate'] = 0.1
param['min_split_loss'] = 0.
param['min_child_weight'] = 1.
param['reg_lambda'] = 0.
param['reg_alpha'] = 0.
param['max_depth'] = 3
param['subsample'] = 1.
param['colsample_bylevel'] = 1.0
param['colsample_bytree'] = 1.0
param['seed']=2016 
num_round = 5
early_stopping_rounds = 50
evals = [(dtr,'tr')]

plst = list(param.items())
eval_rets = {}
bst = xgb.train(params = plst,dtrain = dtr, num_boost_round=num_round, 
                evals=evals, early_stopping_rounds=early_stopping_rounds, evals_result=eval_rets)

y_tr_prd = bst.predict(dtr)
y_tr_prd_leaf = bst.predict(dtr,pred_leaf=True)

bst.dump_model('model_00',with_stats=True)

print get_row_interpret(model='model_00',y_prd = y_tr_prd,y_prd_leaf=y_tr_prd_leaf,ins=0)