
# coding: utf-8

# In[54]:


import os
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation


# In[55]:


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()


# In[56]:


data_path = os.path.join(os.getcwd(), 'data', 'to_analyse')
dataset = load_files(data_path, shuffle=False, categories=['hits'])
print("n_samples: %d" % len(dataset.data))


# In[57]:


n_samples = 1000
n_features = 1000
n_topics = 10
n_top_words = 20

data_samples = dataset.data #[:n_samples]


# In[58]:


tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
                                   max_features=n_features,
                                   stop_words='english')
tfidf = tfidf_vectorizer.fit_transform(data_samples)


# In[59]:


tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                max_features=n_features,
                                stop_words='english')
tf = tf_vectorizer.fit_transform(data_samples)
print(tf.shape)


# In[60]:


print("Fitting the NMF model with tf-idf features, "
      "n_samples=%d and n_features=%d..."
      % (n_samples, n_features))
nmf = NMF(n_components=n_topics, random_state=1,
          alpha=.1, l1_ratio=.5).fit(tfidf)


# In[61]:


print("\nTopics in NMF model:")
tfidf_feature_names = tfidf_vectorizer.get_feature_names()
print_top_words(nmf, tfidf_feature_names, n_top_words)


# In[62]:


print("Fitting LDA models with tf features, "
      "n_samples=%d and n_features=%d..."
      % (n_samples, n_features))
lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
lda.fit(tf)


# In[63]:


print("\nTopics in LDA model:")
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)


# In[78]:


from textacy.tm import TopicModel
model = TopicModel('lda', n_topics=10)
model.fit(tf)
model


# In[80]:


import matplotlib.pyplot as plt
model.termite_plot(tf, tf_feature_names, topics=-1, n_terms=50, highlight_topics=[2, 3, 4, 8])
plt.show()


# In[82]:


from textacy.tm import TopicModel
model = TopicModel('lda', n_topics=7)
model.fit(tf)


# In[77]:


import matplotlib.pyplot as plt
model.termite_plot(tf, tf_feature_names, topics=-1, n_terms=50, highlight_topics=[2, 3, 4, 5])
plt.show()


# In[85]:


from textacy.tm import TopicModel
model = TopicModel('lda', n_topics=6)
model.fit(tf)


# In[94]:


import matplotlib.pyplot as plt
model.termite_plot(tf, tf_feature_names, topics=-1, n_terms=50, highlight_topics=list(range(0,6)))
plt.show()

