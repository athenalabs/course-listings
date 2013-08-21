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

    # course name
    self.name = text(sel.find('.course-topbanner-name'))

    # organization
    self.org = sel.find('.course-topbanner').find('img').attr('alt').strip()
    self.org = ' '.join(map(str.capitalize, self.org.split(' ')))

    # instructor
    self.instructor = text(sel.find('.course-topbanner-instructor'))
    if self.instructor.startswith('by '):
      self.instructor = self.instructor[3:]

    # sections
    self.sections = map(Section, sel.find('.course-item-list-header').items())




class Section(Parsable):

  def parse(self, sel):

    # section name
    self.name = text(sel.find('h3'))

    # item list
    item_list = sel.next('.course-item-list-section-list').find('li')
    self.items = map(Item, item_list.items())



class Item(Parsable):

  def gen_links(self, links):
    for a in links.items():
      if a.attr('title').strip().startswith('Subtitles'):
        continue
      yield a.attr('title').strip(), a.attr('href')

  def parse(self, sel):
    self.name = text(sel.find('a.lecture-link'))
    self.video = sel.find('a.lecture-link').attr('href').strip()
    self.links = dict(list(self.gen_links(sel.find('a[title]'))))


def parse_index(index):
  if index.startswith('http'):
    return Course(PyQuery(url=index))
  else:
    return Course(PyQuery(filename=index))


def print_syllabus(course):

  print '# coursera /', course.name
  print ''
  print 'Title:', course.name
  print 'Instructor:', course.instructor
  print 'Organization:', course.org
  print 'Website:', course.website
  print ''

  for section in course.sections:
    print '##', section.name
    print ''

    for item in section.items:
      print '###', item.name
      print ''
      print '[Watch Lecture](%s)' % item.video
      for link_name, link_href in item.links.items():
        print '[%s](%s)' % (link_name, link_href)
      print ''
      print 'Precepts:'
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
