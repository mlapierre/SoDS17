Classifying Interesting Articles - Experiment 1
-----------------------------------------------

This is an experiment / proof of concept of a classifier that predicts whether an article will be interesting.

It's trained on a set of articles that are either interesting, or not. So its prediction will depend very much on who found the training set interesting. It's like a recommendation engine, just for me.

Note: As this is a proof of concept I haven't tidied up the code or data very much, nor I have put much effort into explanation. This is more of a lab journal than anything else.

For this experiment I've collected 660 interesting articles and 801 that I didn't find interesting.

I used Evernote to save the interesting articles whenever I read them in my RSS reader, or when I stumbled across them some other way. I exported them from Evernote manually and used `process_interesting_evernotes.py` to convert them to collection of plain text files.

I collected a set of less interesting articles from commoncrawl.org, rather than scraping web sites directly. To do that I used:
  1. `unique_sites.py` to extract a list of sites I found interesting articles on
  2. `collect_index_records.py` to fetch the most recent commoncrawl index records for each site. I included two sites that I don't find interesting at all, to increase the variety of uninteresting data.
  3. `collect_misses.py` to construct a set of up to 100 articles from each site, saved as plain-text files.
  4. `cleanup.py` to remove articles that were too short, or which matched any of the interesting articles.

Given this is a proof of concept there was a bit of manual work up to this point, and then a bit more to make sure none of the 'misses' were actually 'hits'. I.e., I didn't want interesting articles to turn up as misses, so I skimmed through all the misses to make sure they weren't coincidentally interesting (there were a few). The hits and misses then went into separate folders, ready to be loaded by scikit-learn.

Next `analysis1.ipynb` trains a linear support vector machine and a naive bayes classifier. Both showed reasonable precision and recall for a first attempt, but tests on new articles showed that the classifier tended to categorise articles as misses, even if I did find them interesting. This is not particular surprising; most articles I'm exposed to are not particularly interesting, and such simple models trained on a relatively small dataset are unlikely to be exceptionally accurate in identifying them.

Finally, `topic_analysis_hits.py` performs topic analyses of the interesting articles, comparing non-negative matrix factorization with latent dirichlet allocation. They do a reasonable job of identifying common themes, including brain research, health research, science, technology, politics, testing, and, of course, data science.

In my next experiment I plan to refine the predictions by paying more attention to cleaning and pre-processing the data. I'll also use the trained model to make ranked predictions rather than a simple binary classification. The dataset will also be a little bigger; now at around 800 interesting articles, and a few thousand not-so-interesting.
