#!/usr/bin/env python

import string
import logging

try:
  from pyquery import PyQuery
except:
  print 'Requries pyquery. Run:'
  print 'sudo pip install pyquery'
  exit(-1)


def text(sel):
  s = sel.text()
  s = filter(lambda c: c in string.printable, s)
  return s.strip()


class Parsable(object):

  def __init__(self, sel):
    assert sel is not None
    self.parse(sel)

  def parse(self, sel):
    pass



class Course(Parsable):

  def parse(self, sel):

    # course name + code
    title = text(sel.find('title')).replace('Course Materials | ', '')
    code, name = title.split(':', 1)

    self.name = name
    self.code = '/stanford/%s' % code

    # organization
    self.org = 'Stanford University'
    self.author = ''
    self.instructor = ''

    # sections
    self.sections = map(Section, sel.find('h3').items())




class Section(Parsable):

  def parse(self, sel):

    # section name
    self.name = text(sel)

    # item list
    item_list = sel.next('.course-section').find('li.course-list-item')
    self.items = map(Item, item_list.items())



class Item(Parsable):

  def parse(self, sel):
    title_sel = sel.find('h4')
    self.name = text(title_sel)
    self.links = {}

    link = title_sel.find('a').attr('href').strip()
    if '/videos/' in link:
      self.video = link
    if '/files/' in link and '.pdf' in link:
      self.links['PDF'] = link
    if '/problemsets/' in link:
      self.links['Problem Set'] = link


def parse_index(index):
  if index.startswith('http'):
    return Course(PyQuery(url=index))
  else:
    with open(index) as f:
      text = f.read()
    return Course(PyQuery(text))


def print_syllabus(course):

  print '#', course.name
  print ''
  print '- **Code**:', course.code
  print '- **Title**', course.name
  print '- **Author**:', course.author
  print '- **Instructor**:', course.instructor
  print '- **Institution**:', course.org
  print '- **Course Website**: [%s](%s)' % (course.website, course.website)
  print ''
  print ''
  print '## Table of Contents'
  print ''
  print '[tableofcontents]'
  print ''
  print '## Prerequisites'
  print ''
  print '- TODO'
  print ''
  print ''


  # sections are reversed in c2g
  for section in reversed(course.sections):
    print '##', section.name
    print ''

    for item in section.items:

      # for now, only list videos
      if not hasattr(item, 'video'):
        continue

      print '###', item.name
      print ''
      print '[Watch Lecture](%s)' % item.video
      for link_name, link_href in item.links.items():
        print '[%s](%s)' % (link_name, link_href)
      print ''
      print 'Concepts Required:'
      print ''
      print '- TODO'
      print ''
      print 'Concepts Taught:'
      print ''
      print '- TODO'
      print ''
      print ''
      print ''



def main():
  import sys

  try:
    index = sys.argv[1]
  except IndexError:
    print 'Usage: %s <course video lectures index url>' % sys.argv[0]
    exit(-1)

  course = parse_index(index)
  course.website = index
  print_syllabus(course)


if __name__ == '__main__':
  main()
