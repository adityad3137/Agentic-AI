from extract_data import *
from agent import Agent
from collections import deque
import sys

def main():

    agent = Agent()

    file_path = input("Please enter the file path here: ").strip()
    try:
        document = extract_Data(file_path)
    except FileNotFoundError as e:
        print(f"Error : {e}")
        print("Terminating program")
        sys.exit(1)
    
    prev_conversations = deque()
    MAX_PREV_CONVERSATIONS_ALLOWED = 5

    while True:

        query = input("> ").strip()

        if query == "exit":
            print("Conversation terminated successfully!")
            return

        route = agent.run("Router", query, document, prev_conversations)

        print(f"Routing to: {route}")

        answer = agent.run(route, query, document, prev_conversations)

        print(answer + "\n\n")

        if len(prev_conversations) == MAX_PREV_CONVERSATIONS_ALLOWED:
            prev_conversations.popleft()
        
        prev_conversations.append({query : answer})

if __name__ == "__main__":
    main()