# KDA 계산기
# 실행시 사용자로부터 킬, 데스, 어시스트를 입력받아 KDA를 계산하여 출력하는 프로그램
## 입력 예시: 3 6 20
## 출력 예시: KDA: 3.83

kill = int(input())
death = int(input())
assit = int(input())
# kill, death, assist = map(int, input("킬 데스 어시스트 입력: ").split())

if death == 0:
    kda = kill + assist
else:
    kda = (kill + assist) / death
# kda = (kill + assist) / (death if death != 0 else 1)

print(kda)
# print(f"KDA: {kda:.2f}")
