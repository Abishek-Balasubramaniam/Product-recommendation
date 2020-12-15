from django.shortcuts import render
from django.http import HttpResponse

import numpy as np
import pandas as pd
import sklearn
from sklearn.decomposition import TruncatedSVD

amazon_ratings = pd.read_csv('Product_recommendation/assets/ratings_Beauty.csv')
amazon_ratings = amazon_ratings.dropna()
amazon_ratings1 = amazon_ratings.head(10000)
ratings_utility_matrix = amazon_ratings1.pivot_table(values='Rating', index='UserId', columns='ProductId', fill_value=0)
X = ratings_utility_matrix.T
X1 = X
SVD = TruncatedSVD(n_components=10)
decomposed_matrix = SVD.fit_transform(X)
correlation_matrix = np.corrcoef(decomposed_matrix)

def get_recommendation(id):
    product_names = list(X.index)
    product_ID = product_names.index(id)
    product_ID
    correlation_product_ID = correlation_matrix[product_ID]
    Recommend = list(X.index[correlation_product_ID > 0.90])
    Recommend.remove(id) 
    return Recommend[:10]

def recommend(request):
    if request.method=='POST':
        prods = get_recommendation(id=request.POST['title'])
        product_list=[]
        for prod in prods:
            p={}
            p['id'] = prod
            count=amazon_ratings['ProductId'].value_counts()[str(prod)]
            p['count'] = count
            df=amazon_ratings.loc[amazon_ratings['ProductId'] == str(prod)]
            p['ratings'] = dict(df['Rating'].value_counts())
            product_list.append(p)

        return render(request, 'product_recommendations.html', {'product_list':product_list})
    else:
        return render(request,'get_product.html')
