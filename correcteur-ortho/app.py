# -*- coding: utf-8 -*-
#!/usr/bin/python3.2
#
#Copyright (C) 2012 Yassine Zenati, released under the MIT license.
#
#dependencies:
# > termcolor.
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files
#(the "Software"), #to deal in the Software without restriction, including without limitation the rights to use, copy, modify,
#merge, publish, distribute, sublicense, #and/or sell copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

import sys
import fileinput
import difflib
import itertools
import argparse

from sys import stdout
from termcolor import colored, cprint
from collections import Counter
#from guess_language import guessLanguageName, guessLanguage

parser = argparse.ArgumentParser()
parser.add_argument('-f', help='fichier à selectionner.')
parser.add_argument('-s', help='afficher la liste des suggéstions.', action="store_true", default=False)
parser.add_argument('-i', help='mode intéractif.', action="store_true", default=False)
parser.add_argument('-g', help='mode graphique.', action="store_true", default=False)
parser.add_argument('--version', action='version', version='%(prog)s 0.0.1')
results = parser.parse_args()

list_of_values_from_dictionary = []
list_of_lines_from_text = []
words_to_correct = {}
chars = ['',' ', ',', '!', '.', ';', '?', '%', '.', ':',";","l'","s'","s’","«","»","(",")",'"', '“', '”']

detected_language = ''
__source__ = {
  'fr' : 'fr_dic',
  'en' : 'en_dic',
  'es' : 'es_dic',
  'it' : 'it_dic'
}

class Line(object):
  def __init__(self, value, num_line, words = []):
    object.__init__(self)
    self.value = value
    self.num_line = num_line
    self.words = words

  def print_and_highlight_word(self, word):
    self.value.replace(word.value, colored(word.value, 'white', 'on_red'))

  def print_words(self):
    return ' '.join([str(x) for x in self.words])

  def replace_word(self, word, correction):
    self.value = self.value.replace(word, correction)

class Word(object):
  def __init__(self, value, num_line, corrected = False, suggested_corrections = []):
    object.__init__(self)
    self.value = value
    self.num_line = num_line
    self.corrected = corrected
    self.suggested_corrections = suggested_corrections

  def __str__(self):
    return self.value

  def return_detail(self):
    return '[Ligne %s] : [%s]' % (self.num_line, self.value)

  def set_value(self, value):
    self.value = value

  def set_corrected(self, boolean):
    self.corrected = boolean

  def set_suggested_corrections(self, list_of_suggested_words):
    self.suggested_corrections = list_of_suggested_words

def levenshtein(s1, s2):
  if len(s1) < len(s2):
      return levenshtein(s2, s1)
  if not s1:
      return len(s2)
      
  previous_row = range(len(s2) + 1)
  for i, c1 in enumerate(s1):
      current_row = [i + 1]
      for j, c2 in enumerate(s2):
          insertions = previous_row[j + 1] + 1
          deletions = current_row[j] + 1
          substitutions = previous_row[j] + (c1 != c2)
          current_row.append(min(insertions, deletions, substitutions))
      previous_row = current_row
  return previous_row[-1]

def find_closest_words_to(word):
  hash_data = {}
  [hash_data.update({x : levenshtein(word, x)}) for x in list_of_values_from_dictionary]
  return sorted(hash_data.items(), key=lambda x: x[1])

def create_list_of_words_from_line(list_of_values, num_line):
  list = []
  for id, value in enumerate(list_of_values.split()):
    list.append(Word(value, num_line))
  return list

def double_print():
  print()
  print()

def clean(text):
  for i, j in enumerate(chars):
    text = text.replace(j, '')
  return text

def check_int(s):
  return s.isdigit()

print()
if results.f:
  with open(results.f) as text:
    detected_language = 'fr'
    print (colored('Lecture et traitement du fichier texte...', 'white', 'on_blue'), end=' ')
    print (colored('[détecté: %s]' % detected_language, 'white', 'on_blue'), end=' ')
    text.seek(0)
    for num_line, line in enumerate(text):
      list_of_lines_from_text.append(Line(line, num_line, create_list_of_words_from_line(line, num_line)))
    print (colored('[Terminé]', 'white', 'on_blue'), end='\n')

  with open(__source__[detected_language]) as mots:
    print (colored('Chargement du dictionnaire...', 'white', 'on_blue'), end=' ')
    for num_line, value in enumerate(mots):
      list_of_values_from_dictionary += value.lower().split()
    print (colored('[Terminé]', 'white', 'on_blue'), end='\n')

  total_words = 0
  total_checked_words = 0
  for id, line in enumerate(list_of_lines_from_text):
    total_words += len(line.words)

  for id, line in enumerate(list_of_lines_from_text):
    for id2, word in enumerate(line.words):
      total_checked_words += 1
      stdout.write("\r%s" % colored('Traitement en cours... ' + str(total_checked_words) + '/' + str(total_words), 'white', 'on_blue'))
      stdout.flush()

      if not (clean(word.value).lower() in list_of_values_from_dictionary) and not check_int(clean(word.value)) and not (clean(word.value) in chars):
        if word.num_line in words_to_correct:
          words_to_correct.update({ word.num_line : words_to_correct.get(word.num_line) + [word] })
        else:
          words_to_correct.update({ word.num_line : [word] })

    print()
    print()

  with open(__source__[detected_language], 'a') as dic_:
    for id, number_of_line in enumerate(sorted(words_to_correct)):
      print (colored('Ligne ' + str(number_of_line), 'white', 'on_magenta', attrs=['bold']), colored(', '.join([clean(str(x)) for x in words_to_correct[number_of_line]]), 'white', 'on_magenta'), end='\n\n')
      
      for id, word in enumerate([line for line in list_of_lines_from_text if line.num_line == number_of_line][0].words):
        if word in words_to_correct[number_of_line]:
          print (word.value.replace((word.value), colored((word.value), 'white', ('on_yellow' if word.corrected else 'on_red'), attrs=['bold'])), end=' ')
        else:
          print (word, end=' ')
          
      print()
      print()

      if results.s:
        for id, word in enumerate(words_to_correct[number_of_line]):
          if not word.corrected:
#            word.set_suggested_corrections(find_closest_words_to(word.value)[:3])
            word.set_suggested_corrections(difflib.get_close_matches(word.value, list_of_values_from_dictionary))
            print (colored(clean(word.value), 'white', 'on_magenta'), end=' ')
            if (len(word.suggested_corrections) == 0):
              print (colored('aucune suggéstion', 'white', 'on_green'), end=' ')
            else:
              for id, suggestion in enumerate(word.suggested_corrections):
                print (colored(suggestion, 'white', 'on_green'), end=' ')
            
            if not results.i:
              double_print()
            else:
              old_value = word.value
              corrected_value = input("Correction: ")

              word.set_value(corrected_value)

              if not (corrected_value in list_of_values_from_dictionary):
                dic_.write("%s\n" % corrected_value)

              for id, word_object in enumerate(list(itertools.chain(*words_to_correct.values()))):
                if clean(old_value) == clean(word_object.value):
                  word_object.set_value(corrected_value)
                  word_object.set_corrected(True)
              print()
