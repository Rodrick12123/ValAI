from text_analysis import text_analyzer

def main():

    valai = text_analyzer()

    file_path = f"../docs/test.txt"

    text_sample = "The Democratic Party's actions had left many U.S. citizens feeling humiliated."
    text_sample2 = valai.read_file(file_path)

    model_response = valai.analyze_text_llm(text_sample)
    print("Response: ", model_response)

    parsed_response = valai.parse_json(model_response)
    print("Parsed Response: ", parsed_response)

    scores = valai.compute_overall_truth_bias(parsed_response)
    print("Scores: ", scores)

    improved_text = valai.display_improved_text(parsed_response)
    sources = valai.display_sources(parsed_response)

    print("Improved Text: ", improved_text)
    print("Sources: ", sources)

    




if __name__ == "__main__":
    main()