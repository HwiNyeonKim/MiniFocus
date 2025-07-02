# Mini-Focus

OmniFocus의 라이트 버전을 만들어보는 것을 목표로 한다.

## 1. 기능

### 1.1 사용자 인증 및 관리

1. 사용자는 계정을 등록하고 로그인할 수 있다.
   - 이메일과 비밀번호를 사용한 회원가입/로그인
   - JWT 토큰 기반 인증 시스템
   - 자동 토큰 갱신 기능
   - 사용자별 데이터 분리 및 보안

2. 사용자 등록 시 자동으로 기본 프로젝트가 생성된다.
   - 'Inbox' 프로젝트가 자동 생성됨
   - 프로젝트가 지정되지 않은 태스크는 자동으로 Inbox에 할당됨

### 1.2 프로젝트 관리

1. 사용자는 새로운 프로젝트를 생성할 수 있다.
   - 프로젝트는 제목, 설명, 마감일, 상태, 플래그 상태를 가진다.
   - 프로젝트는 다른 프로젝트의 하위 프로젝트가 될 수 있다.
   - 프로젝트는 삭제할 수 있다.
   - **각 사용자는 자신의 프로젝트만 생성/관리할 수 있다.**

2. 사용자는 기존 프로젝트를 수정할 수 있다.
   - 프로젝트의 제목, 설명, 마감일, 상태, 플래그 상태를 변경할 수 있다.
   - 프로젝트의 계층 구조를 변경할 수 있다.
   - **자신이 소유한 프로젝트만 수정할 수 있다.**

### 1.3 태스크 관리

1. 사용자는 새로운 태스크를 생성할 수 있다.
   - 태스크는 제목, 설명, 마감일, 상태, 플래그 상태를 가진다.
   - 태스크는 프로젝트에 속할 수 있다.
   - 프로젝트가 지정되지 않은 태스크는 자동으로 'Inbox' 프로젝트에 할당된다.
   - 태스크는 삭제할 수 있다.
   - **각 사용자는 자신의 프로젝트에만 태스크를 생성할 수 있다.**

2. 사용자는 기존 태스크를 수정할 수 있다.
   - 태스크의 제목, 설명, 마감일, 상태, 플래그 상태를 변경할 수 있다.
   - 태스크의 소속 프로젝트를 변경할 수 있다.
   - **자신이 소유한 태스크만 수정할 수 있다.**

### 1.4 특별 프로젝트

1. 'Inbox' 프로젝트
   - 사용자 등록 시 자동으로 생성되는 기본 프로젝트
   - 프로젝트가 지정되지 않은 모든 태스크가 여기에 할당된다.
   - 삭제 불가능한 시스템 프로젝트

## 2. 기술 스택

### 2.1 Frontend

- React 18
- TypeScript
- Tailwind CSS
- Vite (빌드 도구)
- Docker

### 2.2 Backend

- Python 3.11
- FastAPI (웹 프레임워크)
- SQLAlchemy (ORM)
- SQLite (데이터베이스)
- Alembic (DB Migrations)
- Poetry (의존성 관리)
- pytest (테스트)
- JWT (인증)
- Docker

### 2.3 개발 도구

- Docker Compose (컨테이너 오케스트레이션)
- Code Quality Tools
  - black (코드 포매터)
  - isort (import 정렬)
  - flake8 (린터)

## 3. 프로젝트 구조

```bash
minifocus/
├── fe/                    # React Frontend
│   ├── src/
│   │   ├── components/   # React 컴포넌트
│   │   │   ├── Home.tsx      # 메인 홈 화면
│   │   │   ├── Login.tsx     # 로그인/회원가입 화면
│   │   │   ├── ProjectTree.tsx # 프로젝트 트리 뷰
│   │   │   ├── TaskList.tsx  # 태스크 리스트
│   │   │   ├── TaskItem.tsx  # 개별 태스크 아이템
│   │   │   └── Toolbar.tsx   # 툴바 컴포넌트
│   │   ├── contexts/     # React Context
│   │   │   └── AuthContext.tsx # 인증 상태 관리
│   │   ├── services/     # API 서비스
│   │   │   └── api.ts        # 백엔드 API 호출
│   │   ├── types/        # TypeScript 타입 정의
│   │   │   ├── user.ts       # 사용자 타입
│   │   │   ├── project.ts    # 프로젝트 타입
│   │   │   └── task.ts       # 태스크 타입
│   │   ├── App.tsx       # 메인 앱 컴포넌트
│   │   └── main.tsx      # 앱 진입점
│   ├── package.json      # npm 의존성
│   ├── vite.config.ts    # Vite 설정
│   ├── tailwind.config.js # Tailwind CSS 설정
│   └── Dockerfile        # 프론트엔드 Docker 설정
│
├── be/                   # FastAPI 백엔드
│   ├── alembic/         # DB Migrations
│   │   ├── versions/    # Migration files
│   │   └── env.py       # Alembic environment configuration
│   │
│   ├── app/             # 백엔드 애플리케이션
│   │   ├── api/        # API 엔드포인트
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py      # 인증 API (로그인/회원가입)
│   │   │   │   ├── projects.py  # 프로젝트 API
│   │   │   │   └── tasks.py     # 태스크 API
│   │   │   └── dependencies.py  # API 의존성 (인증 등)
│   │   │
│   │   ├── config/     # 설정 관련 파일
│   │   │   └── settings.py     # 환경 설정
│   │   │
│   │   ├── core/       # 핵심 기능
│   │   │   └── security.py     # JWT 인증 및 보안
│   │   │
│   │   ├── db/        # 데이터베이스
│   │   │   ├── session.py      # DB 세션
│   │   │   ├── init_db.py      # DB 초기화
│   │   │   └── base.py         # Base 모델
│   │   │
│   │   ├── models/    # DB 모델
│   │   │   ├── base.py        # Base 모델
│   │   │   ├── user.py        # 사용자 모델
│   │   │   ├── project.py     # 프로젝트 모델
│   │   │   ├── task.py        # 태스크 모델
│   │   │   └── status.py      # 상태 Enum
│   │   │
│   │   ├── schemas/   # Pydantic 스키마
│   │   │   ├── user.py        # 사용자 스키마
│   │   │   ├── project.py     # 프로젝트 스키마
│   │   │   └── task.py        # 태스크 스키마
│   │   │
│   │   └── main.py    # FastAPI 앱 진입점
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
├── docker-compose.yaml # Docker Compose 설정
└── README.md          # 프로젝트 문서
```

## 4. 실행 방법

### 4.1 프로젝트 클론

```bash
git clone https://github.com/HwiNyeonKim/MiniFocus.git
cd minifocus
```

### 4.2 로컬 개발 환경 설정

각 서비스는 독립적인 Docker 컨테이너에서 실행한다.

#### Backend:

```bash
# 백엔드 서비스 빌드 및 실행
docker compose build backend
docker compose up backend
```

#### Frontend:

```bash
# 프론트엔드 서비스 빌드 및 실행
docker compose build frontend
docker compose up frontend
```

#### 모든 서비스를 한 번에 실행:

```bash
docker compose up --build
```

### 4.3 접속

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

### 5.3. 데이터베이스 관리

```bash
# 마이그레이션 생성
docker compose exec be alembic revision --autogenerate -m "description"

# 마이그레이션 적용
docker compose exec be alembic upgrade head

# 마이그레이션 롤백
docker compose exec be alembic downgrade -1
```

## 6. 보안 기능

### 6.1 인증 시스템

- JWT 토큰 기반 인증
- 비밀번호 해싱 (bcrypt)
- 토큰 자동 갱신
- 사용자별 데이터 분리

### 6.2 권한 관리

- 사용자는 자신의 프로젝트/태스크만 접근 가능
- API 레벨에서 권한 검증
- 403 Forbidden 응답으로 무단 접근 차단

## 7. TODOs

1. **프론트엔드 UI 개선**
   - Drag & Drop 으로 Task 및 Project 의 계층 구조 변경 가능하게 하기
   - Inbox 위쪽 Projects 글자 영역 클릭시 모든 Project와 Task를 계층에 맞게 한눈에 보이도록 표시

2. **태스크 관리**
   - 현재 상태가 WIP/Done 두개 뿐 -> Dropped 상태가 추가
   - 상태별 필터링 (특정 상태의 Task만 표시할 수 있도록 한다)
   - 특정 태스크를 다른 태스크의 하위/상위 태스크로 이동시킬 수 있도록 수정 (Drag & Drop)

3. **프로젝트 관리**
   - 특정 프로젝트를 다른 프로젝트의 하위/상위 프로젝트로 이동시킬 수 있도록 수정 (Drag & Drop)
     - 프로젝트 삭제 시 하위 프로젝트도 함께 삭제
   - 프로젝트 상태 추가 (WIP/Done/Dropped)
     - 프로젝트 상태 변경 시 하위 태스크의 상태도 변경되도록 수정
     - 프로젝트 상태 변경 시 하위 프로젝트의 상태도 변경되도록 수정
   - 프로젝트 상태별 표시 추가 (기본은 WIP. Done 및 Dropped 표시 여부 설정 추가)

4. **마감일 및 알림**
   - 태스크 마감일 관리
   - 알림 시스템
   - 캘린더 뷰 추가

5. **검색 및 필터링**
   - 프로젝트/태스크 검색 기능
   - 태그 시스템 추가

6. **데이터 백업 및 동기화**
   - 데이터 내보내기/가져오기 (기간으로 선택: 생성일 기준, 완료일 기준, 마감일 기준 등)
   - 클라우드 동기화?
   - 백업 기능
