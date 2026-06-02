# 클라우드 기술 활동량 및 기술 조합 분석

## 프로젝트 개요
GitHub Archive 공개 이벤트 데이터를 활용하여 클라우드 기술의 활동량과 기술조합을 분석한 프로젝트이다.
Apache Spark를 이용하여 대용량 데이터를 처리하였고 Apache Hive를 이용하여 SQL 기반 분석을 하였다.

분석 기술 대상
- AWS
- Azure
- GCP
- Docker
- Kubernetes
- Helm
- Terraform
- Jenkins
- Prometheus
- Grafana

## 실행 방법

### 1. 데이터 수집
```bash
bash src/ingest/archive_download.sh
```

### 2. Spark 분석 수행

```bash
spark-submit src/pipeline/stack_combination.py
```

```bash
spark-submit src/pipeline/extract_hive.py
```

### 3. Hive 분석

```sql
SELECT *
FROM technology_count
ORDER BY cnt DESC
LIMIT 10;
```

```sql
SELECT *
FROM combination_count
WHERE combo_size = 2
ORDER BY cnt DESC
LIMIT 10;
```

```sql
SELECT *
FROM combination_count
WHERE combo_size = 3
ORDER BY cnt DESC
LIMIT 10;
```

```sql
SELECT *
FROM combination_count
WHERE combo_size >= 4
ORDER BY cnt DESC
LIMIT 10;
```

```sql
SELECT *
FROM combination_count
ORDER BY cnt DESC
LIMIT 10;
```




## 결과 요약

### 기술별 활동량 분석

| 기술 | 활동량 |
|--------|--------:|
| AWS | 739272 |
| Docker | 362096 |
| Terraform | 293710 |
| Azure | 289618 |
| Kubernetes | 139234 |
| Helm | 134540 |
| Jenkins | 120747 |
| Prometheus | 58153 |
| Grafana | 47762 |
| GCP | 24009 |

기술별 활동량 분석 결과 AWS가 739272건으로 가장 높은 활동량인 것을 확인하였으며, Docker, Terraform, Azure 순서로 나타났다. 
특히 클라우드 서비스와 인프라 자동화, 컨테이너 기술이 활발하게 활용되고 있음을 확인할 수 있었다

### 2개 기술 조합

| 기술 조합 | 빈도 |
|------------|-------:|
| AWS + Terraform | 62952 |
| Azure + Terraform | 19660 |
| Docker + Jenkins | 5589 |
| Azure + Kubernetes | 4282 |
| AWS + Kubernetes | 3699 |

2개 기술 조합 분석 결과 AWS + Terraform 조합이 62952건으로 가장 많이 나타났으며 Azure + Terraform, docker + Jenkins 순으로 나타났다. 
특히 클라우드 환경 구축시 Terraform을 이용한 인프라 자동화가 aws, azure와 함께 자주 사용되는 것을 확인 할 수 있었다


### 3개 기술 조합

| 기술 조합 | 빈도 |
|------------|-------:|
| Azure + Kubernetes + Terraform | 475 |
| Docker + Helm + Jenkins | 303 |
| AWS + Helm + Terraform | 302 |
| AWS + Jenkins + Terraform | 272 |
| Docker + Jenkins + Kubernetes | 150 |

3개 기술 조합 분석 결과 Azure + Kubernetes + Terraform 조합이 475건으로 가장 많이 나타났으며, Docker + Helm + Jenkins, AWS + Helm + Terraform 순으로 나타났다. 
특히 클라우드 서비스, 컨테이너 오케스트레이션, 인프라 자동화 기술이 함께 자주 사용되는 것을 확인하였다. 


### 4개 이상 기술 조합

| 기술 조합 | 빈도 |
|------------|-------:|
| Grafana + Helm + Jenkins + Kubernetes | 29 |
| AWS + Grafana + Prometheus + Terraform | 21 |
| Grafana + Helm + Jenkins + Kubernetes + Prometheus | 17 |
| Grafana + Helm + Kubernetes + Prometheus | 17 |
| Grafana + Jenkins + Kubernetes + Prometheus | 17 |

4개 이상 기술 조합 분석 결과 Grafana + Helm +Jenkins + Kubernetes 조합이 29건으로 가장 많이 나타났으며, AWS + Grafana + Prometheus + Terrafrom, Grafana + Helm + Jenkins + Kubernetes + Prometheus 순으로 나타났다.
특히 모니터링 기술과 컨테이너 오케스트레이션이 함께 사용되는 경우가 많은 것을 확인였다. 

### 전체 기술 조합 TOP 10

| 기술 조합 | 빈도 |
|------------|-------:|
| AWS + Terraform | 62952 |
| Azure + Terraform | 19660 |
| Docker + Jenkins | 5589 |
| Azure + Kubernetes | 4282 |
| AWS + Kubernetes | 3699 |
| AWS + Docker | 3025 |
| Kubernetes + Terraform | 2433 |
| GCP + Terraform | 1633 |
| Grafana + Prometheus | 1617 |
| Docker + Kubernetes | 1464 |

AWS + Terraform 조합이 가장 많이 등장하였으며, 클라우드 서비스와 IaC 기술이  자 주 함께  사용되는 것을 확인하였다.

### 시각화

analyze 디렉터리 안의 Python 스크립트들을 실행하여 기술별 활동량 및 기술 조합 결과들을 시각화한다.
