def euclidean_dist(result_vals,crowd_importance,min_importance,max_importance,SELECTED_MAXTEMP,SELECTED_MINTEMP):
    import pandas as pd
    import scipy
    from sklearn import preprocessing
    result = result_vals.drop(result_vals[result_vals['date'] < '2018-10-01' ].index)
    cos_df = result.loc[:,('yhat_x','yhat_y',"yhat")]
    crowd_imp = crowd_importance
    crowd = 10-crowd_imp
    min_imp = min_importance
    max_imp = max_importance
    least_crowded = min(result['yhat_x'])
    most_crowded = max(result['yhat_x'])
    optimal_crowd = least_crowded + (((most_crowded - least_crowded) / 10 )*crowd)
    weights = [crowd_importance,max_importance,min_importance]
    cos_array = cos_df.values
    ss = preprocessing.StandardScaler().fit(cos_array)
    features_std = ss.transform(cos_array)
    user_input = pd.DataFrame([[ optimal_crowd, SELECTED_MAXTEMP, SELECTED_MINTEMP]], columns=('yhat_x','yhat_y','yhat')) 
    user_input = user_input.values
    user_input = ss.transform(user_input)
    euc_dist= scipy.spatial.distance.cdist(user_input, features_std, metric='euclidean', w=weights)[0]
    topmatch = sorted(enumerate(euc_dist), key = lambda x: x[1], reverse = False)[0]
    top_result = result.iloc[topmatch[0]]
    top_result_time = top_result[2]
    top_result_max = top_result[3]
    top_result_min = top_result[4]
    month_rec = top_result_time.strftime('%B')
    year_rec = top_result_time.strftime('%Y')
    
    return month_rec, year_rec, top_result_max, top_result_min