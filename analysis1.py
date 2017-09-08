
# coding: utf-8

# In[2]:


import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn import metrics


# In[3]:


data_path = os.path.join(os.getcwd(), 'data', 'to_analyse')
dataset = load_files(data_path, shuffle=False)
print("n_samples: %d" % len(dataset.data))
print(dataset.target)


# In[96]:


# split the dataset in training and test set using a specific seed for reproducibility
docs_train, docs_test, y_train, y_test = train_test_split(
    dataset.data, dataset.target, test_size=0.25, random_state=42)


# In[97]:


# Vectorise to extract features and filter out tokens that are too rare or too frequent
pipeline = Pipeline([
    ('vect', TfidfVectorizer(min_df=3, max_df=0.95)),
    ('clf', LinearSVC(C=1000)),
])


# In[98]:


# Use grid search to find out whether unigrams, bigrams, or tri-grams are more useful.
# Fit the pipeline on the training set using grid search for the parameters
parameters = {
    'vect__ngram_range': [(1, 1), (1, 2), (1, 3)],
}
grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1)
grid_search.fit(docs_train, y_train)


# In[99]:


# Print the mean and std for each candidate along with the parameter
# settings for all the candidates explored by grid search.
n_candidates = len(grid_search.cv_results_['params'])
for i in range(n_candidates):
    print(i, 'params - %s; mean - %0.2f; std - %0.2f'
             % (grid_search.cv_results_['params'][i],
                grid_search.cv_results_['mean_test_score'][i],
                grid_search.cv_results_['std_test_score'][i]))


# In[100]:


# Predict the outcome on the testing set 
y_predicted = grid_search.predict(docs_test)


# In[101]:


# How did the classifier perform?
print(metrics.classification_report(y_test, y_predicted,
                                    target_names=dataset.target_names))


# In[102]:


cm = metrics.confusion_matrix(y_test, y_predicted)
print(cm)


# In[103]:


import matplotlib.pyplot as plt
import scikitplot.plotters as skplt


# In[109]:


skplt.plot_learning_curve(grid_search, docs_train, y_train)
plt.show()


# In[90]:


from newspaper import Article
url = 'https://deepmind.com/blog/cognitive-psychology/'
article = Article(url)
article.download()
article.parse()
hit1 = article.text
url = 'https://theconversation.com/teaching-machines-to-understand-and-summarize-text-78236'
article = Article(url)
article.download()
article.parse()
hit2 = article.text
url = 'https://www.theguardian.com/football/2017/jul/07/chelsea-romelu-lukaku-offer-match-manchester-united'
article = Article(url)
article.download()
article.parse()
miss1 = article.text
url = 'https://arstechnica.com/business/2017/07/renewables-have-briefly-exceeded-nuclear-for-the-first-time-in-decades/'
article = Article(url)
article.download()
article.parse()
miss2 = article.text


# In[104]:


docs_new = [hit1, hit2, miss1, miss2]
predicted = grid_search.predict(docs_new)
print(predicted)
for doc, category in zip(['hit1', 'hit2', 'miss1', 'miss2'], predicted):
     print('%r => %s' % (doc, dataset.target_names[category]))


# In[105]:


from sklearn.naive_bayes import BernoulliNB
pipeline = Pipeline([
    ('vect', TfidfVectorizer(ngram_range=(1, 2), min_df=3, max_df=0.95, stop_words='english')),
    ('clf', BernoulliNB()),
])
pipeline.fit(docs_train, y_train)


# In[106]:


y_predicted = pipeline.predict(docs_test)
print(metrics.classification_report(y_test, y_predicted,
                                    target_names=dataset.target_names))


# In[107]:


cm = metrics.confusion_matrix(y_test, y_predicted)
print(cm)


# In[108]:


docs_new = [hit1, hit2, hit3, miss1, miss2]
predicted = pipeline.predict(docs_new)
print(predicted)
for doc, category in zip(['hit1', 'hit2', 'hit3', 'miss1', 'miss2'], predicted):
     print('%r => %s' % (doc, dataset.target_names[category]))

