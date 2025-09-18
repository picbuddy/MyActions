import unittest
from src.metrics import mean

class TestMetricsBase(unittest.TestCase):
    def test_mean(self):
        self.assertAlmostEqual(mean([1, 2, 3, 4]), 2.5)

# 팁: 새 함수를 추가할 때마다 테스트도 "같이" 추가해 보세요.
# 예)
# from src.metrics import median
# class TestMedian(unittest.TestCase):
#     def test_median(self):
#         self.assertAlmostEqual(median([1, 2, 3, 4]), 2.5)

if __name__ == "__main__":
    unittest.main()

