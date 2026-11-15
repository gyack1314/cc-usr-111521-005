import copy
import unittest
from pathlib import Path
from decimal import Decimal
from financed.records import RecordBook,number,instant

ASOF='2026-11-15T00:00:00Z'
SAMPLE=Path(__file__).resolve().parents[1]/'data'/'sample.json'

class Base(unittest.TestCase):
    def setUp(self):
        self.book=RecordBook.load(SAMPLE)

class RecordTests(Base):
    def test_revision_and_deletion(self):
        first={'kind':'x','id':'a','revision':1,'known_at':'2026-10-01T00:00:00Z','data':{'v':1}}
        second={**first,'revision':2,'known_at':'2026-11-01T00:00:00Z','data':{'v':2}}
        third={**first,'revision':3,'known_at':'2026-11-10T00:00:00Z','deleted':True}
        b=RecordBook({'schema':1,'records':[third,first,second]})
        self.assertEqual(b.rows('x','2026-10-20T00:00:00Z')[0]['data']['v'],1)
        self.assertEqual(b.rows('x','2026-11-05T00:00:00Z')[0]['data']['v'],2)
        self.assertEqual(b.rows('x',ASOF),[])
    def test_views_are_copies(self):
        kind=self.book.document['records'][0]['kind'];a=self.book.rows(kind,ASOF)
        a[0]['data']['mutated']=True
        self.assertNotIn('mutated',self.book.rows(kind,ASOF)[0]['data'])
    def test_duplicate_revision(self):
        d=self.book.document;d['records'].append(copy.deepcopy(d['records'][0]))
        self.assertRaises(ValueError,RecordBook,d)
    def test_strict_numbers(self):
        self.assertEqual(number('0.1')+number('0.2'),Decimal('0.3'))
        self.assertRaises(ValueError,number,'NaN')
        self.assertRaises(ValueError,instant,'2026-11-01T00:00:00')
    def test_canonical_fingerprint(self):
        d=self.book.document;d['records'].reverse();other=RecordBook(d)
        kinds={r['kind'] for r in d['records']}
        self.assertEqual(self.book.fingerprint(kinds,ASOF),other.fingerprint(kinds,ASOF))

from financed.operations import direct_positions,disclosure
from financed.model import fund_graph,currency_rate

class DomainTests(Base):
    def test_direct_valuation(self):
        self.assertEqual(sum(x['value'] for x in direct_positions(self.book,ASOF)),Decimal(450))
    def test_unknown_is_not_cash(self):
        r=disclosure(self.book,ASOF)
        self.assertEqual(r['A']['undisclosed'],Decimal('0.1'))
        self.assertEqual(r['B']['undisclosed'],0)
    def test_cycle_is_preserved(self):
        graph=fund_graph(self.book,ASOF)
        self.assertIn(('A',Decimal('0.2'),'b-a'),graph['B'])
    def test_no_forward_fx(self):
        self.assertRaises(ValueError,currency_rate,self.book,ASOF,'USD','2026-11-02')
