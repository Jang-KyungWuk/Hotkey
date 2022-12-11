#!/usr/bin/env python
# coding: utf-8

# In[1]:


import preprocess as pp


# In[7]:


def spam_filter(plaintext):
    return (pp.preprocess(plaintext, returnPlain=True), True)

