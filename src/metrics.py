from statistics import fmean as _fmean, median as _median, pstdev as _pstdev

def mean(values):
    """평균값"""
    return _fmean(values)

# 아래 함수들은 수업 중 "추가"해 보세요.
# 추가 즉시 Pages 테이블에 새 행이 반영됩니다.

# def median(values):
#     """중앙값"""
#     return _median(values)

# def min_value(values):
#     """최솟값"""
#     return min(values)

# def max_value(values):
#     """최댓값"""
#     return max(values)

# def stdev(values):
#     """표준편차 (모집단)"""
#     if len(values) < 2:
#         return None
#     return _pstdev(values)
