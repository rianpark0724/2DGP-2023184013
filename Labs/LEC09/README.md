# LEC09 애니메이션 뷰어

`sonic-sprite.png`의 16개 동작, 76개 프레임을 자동으로 재생한다. 각 동작을 5회 반복한 뒤 마지막 프레임에서 1초 대기하고 다음 동작으로 넘어간다. 마지막 동작 이후 처음부터 계속 반복한다.

## 실행

Python 3.10 이상과 pico2d가 필요하다. 실제 검증 환경은 Windows, Python 3.12.14, pico2d 1.5.1이다.

```powershell
python -m pip install pico2d==1.5.1
python animation_viewer.py
```

LEC09 폴더에서 실행한다. 다른 폴더에서는 `animation_viewer.py`의 경로를 지정하면 된다. 이미지는 작업 디렉터리와 관계없이 스크립트 옆에서 찾는다. `animation_viewer.py`와 `sonic-sprite.png`를 같은 폴더에 유지한다.

이번 작업에서 만든 전용 검증 환경으로 실행하려면 `2dgame` 폴더에서 다음 명령을 사용한다.

```powershell
.\.lec09-venv\Scripts\python.exe .\2DGP-2023184013\Labs\LEC09\animation_viewer.py
```

이 가상환경은 Git 저장소 외부에 있으며 다른 PC에는 포함되지 않는다. 다른 PC에서는 위의 Python 및 pico2d 설치 방법을 사용한다.

## 동작과 설정

- 종료: Escape 또는 창 닫기. 대기 중에도 사용할 수 있다.
- 화면: 800×600, 단색 배경, 종횡비를 유지한 4배 확대.
- 속도: 초당 10프레임. 지상 동작은 하단 중앙, 공중·회전 동작은 중심을 정렬한다.
- 긴 처리 지연: 한 번에 여러 프레임·동작을 건너뛰지 않으며, 실제 재생 시간이 길어질 수 있다.
- 오류: 이미지를 찾거나 읽을 수 없으면 실패한 경로를 출력하고 종료 코드 1로 끝난다.

실행 코드는 `animation_viewer.py` 하나이며, 프레임 데이터도 그 안에 들어 있다. 동작 목록과 포함·제외 근거는 `ANIMATION_NOTES`, 실제 좌표는 `ANIMATIONS`에 있다. `SCALE`, `FPS`, `CANVAS_WIDTH`, `CANVAS_HEIGHT`는 화면·속도 기본값이다. 반복 횟수와 대기 시간은 PRD 필수값이므로 유지한다.

동작 이름은 시각적 분류이며 공식 명칭을 보장하지 않는다. 제목과 제작자 표기, 크레딧 영역의 노랑·갈색 부가 캐릭터는 재생 대상에서 제외했다. 본문에 있는 파란 캐릭터의 76개 포즈는 단일 프레임 동작까지 모두 포함했다.

개발 과정과 검증 결과는 [DEVELOPMENT_REPORT.md](DEVELOPMENT_REPORT.md), 요구사항은 [PRD.md](PRD.md)를 참고한다.
