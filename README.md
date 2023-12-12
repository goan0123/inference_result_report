# inference 결과 reporting tool 가이드
## inference 결과 레이블과 원본 레이블 비교 및 통계 결과 report

last modified: 2023-05-10

설명: 이미지의 inference 후 결과 레이블과 원본 레이블의 클래스와 박스의 위치를 비교한다. 정탐인 경우 초록색, 오탐인 경우는 빨간색, 미탐인 경우는 검정색으로 결과를 나타낸다.

### 1. 코드를 사용하는 방법
  from report import *

  #원본 레이블 디렉토리와 결과 레이블 디렉토리 선언
  
  dir_original=r"E:\Works\projects\3.ID\code\origin_label"
  dir_result=r"E:\Works\projects\3.ID\code\result_label"

  #return: report 결과 및 결과 디렉토리
  
  dir_report,report=report(dir_original, dir_result)

### 2. UI로 사용하는 방법
원본 레이블이 있는 디렉토리와 결과 레이블이 있는 디렉토리를 지정한 후 report 버튼을 누른다.

