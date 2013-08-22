#!/usr/bin/env python

import re

link_prefix = 'https://athena.ai/'


def athena_link(name):
  name = re.sub('\s+', ' ', name).strip() # clean spaces
  link = link_prefix + name.replace(' ', '-').lower()
  return '[%s](%s)' % (name, link)


def add_athena_links(string):
  pattern = re.compile('\[([^\]]+)\]\(\)') # empty md links
  return pattern.sub(lambda m: athena_link(m.group(1)), string)



def main():
  import sys
  if '-h' in sys.argv:
    print 'Usage: %s [files]' % sys.argv[0]
    print 'Populates athena links in a file or stdin.'
    exit(0)

  def out(line):
    sys.stdout.write(line)
    sys.stdout.flush()

  import fileinput
  for line in fileinput.input():
    out(add_athena_links(line))


if __name__ == '__main__':
  main()
