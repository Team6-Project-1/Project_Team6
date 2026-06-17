import subprocess
import sys

subprocess.run([sys.executable, "create_route_api_json.py"], check=True)
subprocess.run([sys.executable, "create_station_api_json.py"], check=True)

print("JSON 저장 완료")