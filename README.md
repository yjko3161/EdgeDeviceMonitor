# EdgeDeviceMonitor

## 📌 프로젝트 개요
EdgeDeviceMonitor는 **원격 엣지 장비(Luckfox 등)가 살아있는지(전원/OS/네트워크/서비스)**를  
로컬 PC에서 **장기간(365일 이상)** 감시하기 위한 **경량 장비 생존 모니터링 프로젝트**이다.

장비 내부 로직에 의존하지 않고,  
**외부(로컬 PC)에서 Ping + HTTP Health Check** 방식으로  
장비의 실제 생존 여부를 판단하는 것을 목표로 한다.

---

## 🎯 개발 목적
- 장비 전원 다운 / OS 크래시 / 네트워크 단절 여부 확인
- Flask 등 서비스 단위 장애와 장비 전체 장애 구분
- 365일 연속 가동 내구 테스트 증적 확보
- 장비 내부 크론/DB/헬스비트에 의존하지 않는 구조

---

## 🧩 전체 구조

[Local PC (Watcher)]
├─ 주기적 Ping 체크
├─ 주기적 HTTP Health 체크
├─ 결과 로그 저장
└─ (선택) 알림/DB 확장

[Edge Device (Luckfox)]
└─ Flask 서버 (/api/health 제공)

yaml
코드 복사

---

## 🔍 감시 방식

### 1️⃣ Ping 체크
- 대상: 장비 IP
- 목적: 전원 / OS / 네트워크 생존 여부 확인

### 2️⃣ HTTP Health Check
- 대상: `http://<device_ip>:5000/api/health`
- 목적: OS + 애플리케이션 정상 동작 여부 확인

### 상태 판정 기준

| Ping | HTTP | 상태 판단 |
|----|----|----|
| OK | OK | 장비 및 서비스 정상 |
| OK | FAIL | 장비 정상 / 서비스 장애 |
| FAIL | FAIL | 장비 다운 (전원/OS/네트워크) |

---

## 🛠 실행 환경
- 감시 PC: Windows / Ubuntu / macOS
- 언어: Python 3.x
- 필수 라이브러리:
  - `requests`

```bash
pip install requests
▶ 실행 방법
1️⃣ 설정 값 수정
python
코드 복사
HOST = "192.168.0.50"   # Edge 장비 IP
URL  = "http://192.168.0.50:5000/api/health"
2️⃣ 실행
bash
코드 복사
python luckfox_watch.py
📝 로그 포맷
text
코드 복사
[YYYY-MM-DD HH:MM:SS] PING=OK HTTP=OK
[YYYY-MM-DD HH:MM:SS] PING=OK HTTP=FAIL
[YYYY-MM-DD HH:MM:SS] PING=FAIL HTTP=FAIL
로그 파일: luckfox_watch.log

로그는 누적 저장되며, 장기간 내구 테스트 증적으로 활용 가능

📈 확장 계획 (선택)
 장비 다운 시 텔레그램/슬랙 알림

 DB 저장 (다운 횟수, 누적 다운 시간)

 다중 장비 동시 감시

 그래프/리포트 자동 생성

 Windows 작업 스케줄러 / Linux systemd 연동

⚠ 설계 원칙
장비 내부 코드 수정 최소화

장비가 완전히 다운된 상황에서도 외부에서 판별 가능

1년 이상 장기 운용 시에도 복잡도 증가 없이 안정성 유지

📄 라이선스
Internal Use / Research Purpose

✍️ 비고
본 프로젝트는 “장비가 뒤졌는지 아닌지”를 가장 단순하고 확실하게 확인하기 위한 도구이며,
과도한 모니터링 프레임워크를 지양하고 실전 운용을 최우선으로 한다.
