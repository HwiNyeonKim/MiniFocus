# Mini-Focus

OmniFocus의 라이트 버전을 만들어보는 것을 목표로 한다.

## 1. 기능

### 1.1 프로젝트 관리

1. 사용자는 새로운 프로젝트를 생성할 수 있다.
   - 프로젝트는 제목, 설명, 마감일, 상태, 플래그 상태를 가진다.
   - 프로젝트는 다른 프로젝트의 하위 프로젝트가 될 수 있다.
   - 프로젝트는 삭제할 수 있다.

2. 사용자는 기존 프로젝트를 수정할 수 있다.
   - 프로젝트의 제목, 설명, 마감일, 상태, 플래그 상태를 변경할 수 있다.
   - 프로젝트의 계층 구조를 변경할 수 있다.

### 1.2 태스크 관리

1. 사용자는 새로운 태스크를 생성할 수 있다.
   - 태스크는 제목, 설명, 마감일, 상태, 플래그 상태를 가진다.
   - 태스크는 프로젝트에 속할 수 있다.
   - 프로젝트가 지정되지 않은 태스크는 자동으로 'Inbox' 프로젝트에 할당된다.
   - 태스크는 삭제할 수 있다.

2. 사용자는 기존 태스크를 수정할 수 있다.
   - 태스크의 제목, 설명, 마감일, 상태, 플래그 상태를 변경할 수 있다.
   - 태스크의 소속 프로젝트를 변경할 수 있다.

### 1.3 특별 프로젝트

1. 'Inbox' 프로젝트
   - Default Project로 삭제 불가능하다.
   - 프로젝트가 지정되지 않은 모든 태스크가 여기에 할당된다.

## 2. 기술 스택

### 2.1 Frontend  (예정)

- React
- TypeScript
- Docker

### 2.2 Backend

- Python
- FastAPI
- SQLAlchemy (with SQLite)
- Alembic (DB Migrations)
- Poetry (의존성 관리)
- pytest
- Docker
- Code Quality Tools
  - black (코드 포매터)
  - isort (import 정렬)
  - flake8 (린터)

## 3. 프로젝트 구조

```bash
minifocus/
├── fe/                    # React Frontend. Skip for now.
│
├── be/                   # FastAPI 백엔드
│   ├── alembic/         # DB Migrations
│   │   ├── versions/    # Migration files
│   │   └── env.py       # Alembic environment configuration
│   │
│   ├── app/             # 백엔드 애플리케이션
│   │   ├── api/        # API 엔드포인트
│   │   │   ├── endpoints/
│   │   │   │   ├── tasks.py     # Task API
│   │   │   │   └── projects.py  # Project API
│   │   │   └── dependencies.py  # API dependencies
│   │   │
│   │   ├── config/     # 설정 관련 파일
│   │   │   └── settings.py     # 환경 설정
│   │   │
│   │   ├── db/        # 데이터베이스
│   │   │   └── session.py      # DB 세션
│   │   │
│   │   ├── models/    # DB 모델
│   │   │   ├── base.py        # Base 모델
│   │   │   ├── task.py        # Task 모델
│   │   │   ├── project.py     # Project 모델
│   │   │   └── status.py      # Status Enum
│   │   │
│   │   └── schemas/   # Pydantic 스키마
│   │       ├── task.py        # Task 스키마
│   │       └── project.py     # Project 스키마
│   │
│   ├── tests/         # pytest 테스트
│   │   ├── api/      # API 테스트
│   │   └── conftest.py # 테스트 설정
│   │
│   ├── scripts/       # 유틸리티 스크립트
│   │   └── lint.sh   # 린트 실행 스크립트
│   │
│   ├── Dockerfile    # 백엔드 Docker 설정
│   ├── pyproject.toml # Poetry 의존성 관리
│   └── alembic.ini   # Alembic 설정
│
└── docker-compose.yaml # Docker Compose 설정
```

## 4. 실행 방법

1. 프로젝트 클론

   ```bash
   git clone https://github.com/HwiNyeonKim/MiniFocus.git
   cd minifocus
   ```

2. 로컬 개발 환경 설정

   각 서비스는 독립적인 Docker 컨테이너에서 실행한다.

   - Backend:

   ```bash
   # 백엔드 서비스 빌드 및 실행
   docker compose build backend
   docker compose up backend
   ```

   - Frontend:

   ```bash
   # 프론트엔드 서비스 빌드 및 실행
   docker compose build fronted
   docker compose up frontend
   ```

   - 모든 서비스를 한 번에 실행:

   ```bash
   docker compose up --build
   ```

3. 접속

   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8000](http://localhost:8000)
   - API 문서: [http://localhost:8000/docs](http://localhost:8000/docs)

## 5. 개발 관련

### 5.1. Docker 컨테이너 관리

개발 중 자주 사용하는 Docker 명령어:

```bash
# 특정 서비스의 로그 확인
docker compose logs -f be  # 백엔드 로그
docker compose logs -f fe  # 프론트엔드 로그

# 특정 서비스 재시작
docker compose restart be  # 백엔드 재시작
docker compose restart fe  # 프론트엔드 재시작

# 컨테이너 내부 접속
docker compose exec be sh  # 백엔드 컨테이너 접속
docker compose exec fe sh  # 프론트엔드 컨테이너 접속

# 모든 컨테이너 중지 및 삭제
docker compose down
```

### 5.2. 코드 품질 관리

백엔드 코드의 품질을 관리하기 위해 다음 도구들을 사용한다:

1. black: Python 코드 포매터
2. isort: import 문 정렬
3. flake8: 코드 린터

lint 실행:

```bash
cd be
./scripts/lint.sh
```

각 도구는 다음과 같은 역할을 수행한다:

- black: 일관된 코드 스타일 적용
- isort: import 문을 일관된 순서로 정렬
- flake8: 코드 품질 검사
