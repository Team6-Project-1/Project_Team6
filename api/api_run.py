import subprocess
import sys

subprocess.run([sys.executable, "_04_insert_station_data.py"], check=True)
subprocess.run([sys.executable, "_05_insert_route_data.py"], check=True)

print("데이터 적재 완료")