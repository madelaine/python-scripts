#!/usr/bin/env python

import os
from decimal import *

source_vocab = "vocabulaire.txt"
source_topic = "topic2.dat"
export_file = "export.txt"
divide_number = 10
precision = 5
getcontext().prec = 5

title = "Replace this with page title"
author = "Replace this with author's name and email"

vocab_dic = {}
sliced_topics = {}
topic_dic = []
first_part_words = []

def chunks(list, n):
  return [list[i:i+n] for i in range(0, len(list), n)]

class Topic(object):
  def __init__(self, num_line, original_value, calculated_value):
    object.__init__(self)
    self.num_line = num_line
    self.original_value = original_value
    self.calculated_value = calculated_value

class Word(object):
  def __init__(self, num_line, value):
    object.__init__(self)
    self.num_line = num_line
    self.value = value

with open(source_vocab) as vocab:
  for num_line, word_value in enumerate(vocab):
    vocab_dic.update({ num_line : Word(num_line, word_value) })

with open(source_topic) as topics:
  for num_line, topic_value in enumerate(topics):
    topic_dic.append(Topic(num_line, topic_value, Decimal(topic_value).exp()))

for i in range(divide_number):
  sliced_topics.update({ i : sorted(chunks(topic_dic, len(vocab_dic))[i], key=lambda x: x.calculated_value, reverse=True)[:15] })

  if (i == 0):
    for num_line, topic in enumerate(sliced_topics[0]):
      first_part_words.append(vocab_dic[topic.num_line])

with open(export_file, "wb") as export:
  export.writelines("\n".join([title ,author]))

  for i in range(divide_number):
    export.write("\n\n")
    export.write("Part " + str(i) + "\n")
    export.writelines("\n".join([" ".join([first_part_words[index].value.rstrip(), str(x.calculated_value)]) for index,x in enumerate(sliced_topics[i])]))