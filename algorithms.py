import sys
import json

def main():
    try:
        data = json.loads(sys.stdin.readline())
        question = data.get("question", "")
        print(f"Python received: {question}")
    except Exception as e:
        print(f"Error in Python script: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()