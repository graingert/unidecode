# -*- coding: utf-8 -*-
import unittest
import sys
from unidecode import unidecode

# workaround for Python < 2.7
if not hasattr(unittest, 'skipIf'):
	def skipIf(condition, reason):
		def d(f):
			def df(*args):
				if condition:
					print "skipped %r" % (reason,)
				else:
					return f(*args)
			return df
		return d
	unittest.skipIf = skipIf

class TestUnidecode(unittest.TestCase):
	def test_ascii(self):
		for n in xrange(0,128):
			t = chr(n)

			self.failUnlessEqual(unidecode(t), t)

	def test_bmp(self):
		for n in xrange(0,0x10000):
			# Just check that it doesn't throw an exception
			t = unichr(n)
			unidecode(t)

	def test_circled_latin(self):
		# 1 sequence of a-z
		for n in xrange(0, 26):
			a = chr(ord('a') + n)
			b = unidecode(unichr(0x24d0 + n))

			self.failUnlessEqual(b, a)

	@unittest.skipIf(sys.maxunicode < 0x10000, "narrow build")
	def test_mathematical_latin(self):
		# 13 consecutive sequences of A-Z, a-z with some codepoints
		# undefined. We just count the undefined ones and don't check
		# positions.
		empty = 0
		for n in xrange(0x1d400, 0x1d6a4):
			if n % 52 < 26:
				a = chr(ord('A') + n % 26)
			else:
				a = chr(ord('a') + n % 26)
			b = unidecode(unichr(n))

			if not b:
				empty += 1
			else:
				self.failUnlessEqual(b, a)

		self.failUnlessEqual(empty, 24)

	@unittest.skipIf(sys.maxunicode < 0x10000, "narrow build")
	def test_mathematical_digits(self):
		# 5 consecutive sequences of 0-9
		for n in xrange(0x1d7ce, 0x1d800):
			a = chr(ord('0') + (n-0x1d7ce) % 10)
			b = unidecode(unichr(n))

			self.failUnlessEqual(b, a)

	def test_specific(self):

		TESTS = [
				(u"Hello, World!", 
				"Hello, World!"),

				(u"'\"\r\n",
				 "'\"\r\n"),

				(u"ČŽŠčžš",
				 "CZSczs"),

				(u"ア",
				 "a"),

				(u"α",
				"a"),

				(u"а",
				"a"),

				(u'ch\xe2teau',
				"chateau"),

				(u'vi\xf1edos',
				"vinedos"),
				
				(u"\u5317\u4EB0",
				"Bei Jing "),

				(u"Efﬁcient",
				"Efficient"),

				# https://github.com/iki/unidecode/commit/4a1d4e0a7b5a11796dc701099556876e7a520065
				(u'příliš žluťoučký kůň pěl ďábelské ódy',
				'prilis zlutoucky kun pel dabelske ody'),

				(u'PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ PĚL ĎÁBELSKÉ ÓDY',
				'PRILIS ZLUTOUCKY KUN PEL DABELSKE ODY'),

				# Table that doesn't exist
				(u'\ua500',
				''),
				
				# Table that has less than 256 entriees
				(u'\u1eff',
				''),
			]

		for input, output in TESTS:
			self.failUnlessEqual(unidecode(input), output)

	@unittest.skipIf(sys.maxunicode < 0x10000, "narrow build")
	def test_specific_wide(self):

		TESTS = [
				# Non-BMP character
				(u'\U0001d5a0',
				'A'),

				# Mathematical
				(u'\U0001d5c4\U0001d5c6/\U0001d5c1',
				'km/h'),
			]

		for input, output in TESTS:
			self.failUnlessEqual(unidecode(input), output)

if __name__ == "__main__":
    unittest.main()
