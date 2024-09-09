import subprocess
import sys


def run_command(command):
    try:
        print(f"명령어 실행중: {command}")
        result = subprocess.run(
            command, shell=True, check=True, text=True, capture_output=True
        )
        print("출력: ", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"명령어 '{command}' 실행 중 오류 발생: {e}")
        print("오류 출력: ", e.stderr)
        return False

def read_commands_from_file(filename):
    try:
        with open(filename, "r") as file:
            return [
                line.strip()
                for line in file
                if line.strip() and not line.startswith("#")
            ]
    except IOError as e:
        print(f"파일 {filename} 읽기 오류: {e}")
        return None

def execute_commands_sequentially(commands):
    for cmd in commands:
        success = run_command(cmd)
        if not success:
            print(f"명령어 실행 실패. 시퀀스를 중단합니다.")
            return False
        print("명령어가 성공적으로 완료되었습니다. 다음 명령어로 이동합니다.\n")
    return True

def main(command_file):
    print(f"파일에서 명령어 읽는 중: {command_file}")
    commands = read_commands_from_file(command_file)

    if commands is None:
        print("명령어를 읽는데 실패했습니다. 종료합니다.")
        sys.exit(1)

    if not commands:
        print("파일에서 명령어를 찾을 수 없습니다. 종료합니다.")
        sys.exit(0)

    print(f"실행할 명령어 {len(commands)}개를 찾았습니다.\n순차적 명령어 실행을 시작합니다...")

    if execute_commands_sequentially(commands):
        print("모든 명령어가 성공적으로 실행되었습니다.")
    else:
        print("오류로 인해 명령어 시퀀스가 중단되었습니다.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python script.py <명령어_파일>")
        sys.exit(1)
    command_file = sys.argv[1]
    main(command_file)
