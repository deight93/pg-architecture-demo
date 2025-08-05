# pg-architecture-demo

PostgreSQL 클러스터링/샤딩/리플리케이션 + FastAPI 테스트

PostgreSQL 아키텍처 패턴  
**클러스터링, 샤딩, 리플리케이션**을  
Docker Compose와 FastAPI로 직접 실습할 수 있는 샘플 프로젝트

- 완전히 분리된 폴더와 docker-compose로 독립 실행
- FastAPI 앱은 uv 패키지 매니저를 사용하며, 테스트 API를 제공

---

## 폴더 구조

```
pg-architecture-demo/
├── clustering/
│   ├── docker-compose.yml
│   ├── app/
│   │   └── main.py
│   ├── Dockerfile
│   ├── init.sql
│   ├── pyproject.toml
│   └── uv.lock
├── sharding/
│   ├── docker-compose.yml
│   ├── shard1/
│   │   └── init.sql
│   ├── shard2/
│   │   └── init.sql
│   ├── app/
│   │   └── main.py
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── uv.lock
└── replication/
    ├── docker-compose.yml
    ├── master/
    │   └── init.sql
    ├── app/
    │   └── main.py
    ├── Dockerfile
    ├── pyproject.toml
    └── uv.lock
````

---

## 빠른 시작

각 실습별 폴더로 이동하여 컨테이너를 실행하세요.

### 1. Clustering

```bash
cd clustering
docker-compose up -d --build
````

### 2. Sharding

```bash
cd sharding
docker-compose up -d --build
```

### 3. Replication

```bash
cd replication
docker-compose up -d --build
```

---

### Clustering (클러스터링)

* **클러스터링**은 특정 인덱스를 기준으로 테이블 데이터를 **물리적으로 정렬**하는 작업입니다.
* 범위 검색 등에서 디스크 접근 효율을 높일 수 있습니다.
* DB 서버 클러스터(여러 서버 연결)가 아니라, 한 테이블 내 레코드 정렬 방식입니다.

---

### Sharding (샤딩)

* **샤딩**은 데이터를 여러 DB 서버(노드)에 **수평적으로 분산 저장**하는 구조입니다.
* 데이터의 일부만 각 샤드에 저장되며, 샤드 키(예: user\_id)에 따라 데이터를 나눕니다.
* 대용량 서비스에서 데이터베이스의 **확장성(Scale-out)** 확보를 위해 주로 사용합니다.

---

### Replication (리플리케이션)

* **리플리케이션**은 한 DB(Master)의 데이터를 여러 서버(Replica)에 **동일하게 복제**하는 구조입니다.
* 장애 대응, 읽기 부하 분산, 데이터 안전성 확보 등이 주요 목적입니다.
* PostgreSQL에서는 Streaming Replication(스트리밍 복제) 등이 널리 사용됩니다.
