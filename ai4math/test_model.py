import unittest
from datetime import date
from model import velocity, smooth, EDGES

class BaselineTests(unittest.TestCase):
    def event(self, **changes):
        e = dict(id='test', status='verified', type='open_problem_resolution',
                 verified_available='2026-11-27', fields={'0': 1}, difficulty=2,
                 ai_role='collaborative')
        e.update(changes)
        return e

    def test_time_boundaries(self):
        t = date(2026, 11, 27)
        for when, expected in [('2026-11-27', 365/90), ('2026-08-29', 0), ('2026-11-28', 0)]:
            self.assertAlmostEqual(velocity([self.event(verified_available=when)], t, 90)[0], expected)

    def test_unverified_and_wrong_endpoint_excluded(self):
        for e in [self.event(status='unverified'), self.event(type='bound_improvement')]:
            self.assertEqual(sum(velocity([e], date(2026, 11, 27), 180)), 0)

    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            velocity([self.event(), self.event()], date(2026, 11, 27), 180)

    def test_fractional_assignment_conserves_total(self):
        v = velocity([self.event(fields={'0': .25, '1': .75})], date(2026,11,27), 365)
        self.assertAlmostEqual(v[0], .25)
        self.assertAlmostEqual(v[1], .75)
        self.assertAlmostEqual(sum(v), 1)

    def test_invalid_assignment_rejected(self):
        with self.assertRaises(ValueError):
            velocity([self.event(fields={'0': 1, '1': 1})], date(2026,11,27), 365)

    def test_smoothing(self):
        v = [1., 0., 2., 0., 4., 0.]
        self.assertEqual(smooth(v, 0), v)
        s = smooth(v, 2)
        self.assertAlmostEqual(sum(s), sum(v))
        self.assertTrue(all(min(v) <= x <= max(v) for x in s))
        # Verify the defining linear equation independently.
        for i in range(len(v)):
            laplacian = sum(s[i] - s[b if a == i else a] for a, b in EDGES if i in (a,b))
            self.assertAlmostEqual(s[i] + 2 * laplacian, v[i])

    def test_constant_and_disconnected_graph(self):
        for x in smooth([3.] * 6, 2): self.assertAlmostEqual(x, 3.)
        self.assertEqual(smooth([1., 2.], 2, edges=[]), [1., 2.])

if __name__ == '__main__':
    unittest.main()
