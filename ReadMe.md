# Progressive Metrics — GitHub Pages + Actions

'src/metrics.py'에 통계 함수를 하나씩 추가하고 push하면,
CI(문법/테스트) 후 CD가 HTML을 다시 생성해 Pages에 반영합니다.

tools/build_site.py는 **이번 예제의 핵심 “자동화 빌드 스크립트”**입니다. GitHub Actions에서 배포 단계(CD) 때 호출되어 실제로 Pages에 올라갈 HTML을 만들어 주는 역할을 합니다.

# 역할 요약
단계	            동작
1. CSV 읽기	        data/ 안의 CSV 파일들을 스캔해서 데이터를 수집합니다.
2. 통계 계산	    src/metrics.py에 있는 함수들을 동적으로 불러와 각 CSV의 통계를 계산합니다.
3. HTML 생성	    docs/index.template.html의 자리표시자({{TABLES}}, {{UPDATED_AT}})를 실제 값으로 치환해 site/index.html을 만듭니다.
4. Pages로 배포	    GitHub Actions의 upload-pages-artifact가 이 site/ 폴더를 가져가 GitHub Pages로 배포합니다.
# CSV나 코드 → CI/CD → 자동 HTML 생성 → Pages 배포
즉 CI는 코드 품질 확인, build_site.py는 CD의 빌드 단계라고 볼 수 있습니다.

# 왜 필요한가?
GitHub Pages는 기본적으로 정적 파일을 올리는 공간이기 때문에,
CSV 데이터나 Python 계산 결과를 런타임에 서버에서 동적으로 보여줄 수 없습니다.
그래서 Actions가 빌드 시점에 Python을 실행해 HTML을 생성해 두고, 그걸 Pages에 올려야 합니다.
이런 “빌드 스크립트”가 없으면, CSV를 바꿔도 Pages에는 자동 반영되지 않습니다(정적 파일 그대로 배포).

### Try
1) `metrics.py`에 `median(values)` 추가 후 push  
2) (선택) `tests/test_metrics.py`에 테스트도 추가  
3) Actions 성공 후, Pages에서 표에 새 행이 나타나는지 확인


## 수업 시나리오
- **Step 1**: mean만 있는 상태로 push → 페이지에 Mean만 뜸
- **Step 2**: median 추가 후 push → Median 행 추가
- **Step 3**: min_value 추가 후 push → Min 행 추가
- **Step 4**: max_value, stdev 추가…

CI/CD가 코드/테스트/페이지를 연동하는 감각을 체험할 수 있습니다.

