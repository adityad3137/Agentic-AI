from agent import SummarizerAgent, DataAnalyzerAgent, ContentCreatorAgent, CodeGeneratorAgent, RouterAgent
from extract_data import *

def main():

    router = RouterAgent()
    summarizer = SummarizerAgent()
    analytics = DataAnalyzerAgent()
    content = ContentCreatorAgent()
    coder = CodeGeneratorAgent()

    file_path = input("Please enter the file path here: ").strip()
    try:
        document = extract_Data(file_path)
    except FileNotFoundError as e:
        print(f"Error : {e}")
        print("Terminating program")
        sys.exit(1)
    
    while True:

        query = input("> ").strip()

        if query == "exit":
            print("Conversation terminated successfully!")
            return
        
        route = router.route(query)

        print(f"Routing to: {route}")

        if route == "SUMMARIZER":
            answer = summarizer.summarize(document + query)

        elif route == "DATA_ANALYTICS":
            answer = analytics.analyze_data(document + query)

        elif route == "CONTENT_CREATION":
            answer = content.create_content(document + query)

        elif route == "CODE_GENERATION":
            answer = coder.generate_code(document + query)

        else:
            answer = "Unable to determine agent."

        print(answer)

if __name__ == "__main__":
    main()