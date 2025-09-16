import json
import pandas as pd

# Input and output file paths
INPUT_FILE = "Task_1_Dataset_Preparation\mt_bench_human_judgements.jsonl"
OUTPUT_FILE = "mt_bench_human_judgements.csv"

def extract_content(conv_list, index):
    """
    Helper to safely extract 'content' from conv_list[index],
    returns empty string if missing.
    """
    if conv_list and len(conv_list) > index and isinstance(conv_list[index], dict):
        return conv_list[index].get("content", "")
    return ""

def jsonl_to_csv(input_file, output_file):
    records = []

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)

            conv_a = obj.get("conversation_a", [])
            conv_b = obj.get("conversation_b", [])

            row = {
                "split": obj.get("split", ""),
                "question_id": obj.get("question_id", ""),
                "model_a": obj.get("model_a", ""),
                "model_b": obj.get("model_b", ""),
                "winner": obj.get("winner", ""),
                "judge": obj.get("judge", ""),
                "turn": obj.get("turn", ""),
                # Conversation A breakdown (only 'content')
                "conversation_a_turn_1_query": extract_content(conv_a, 0),
                "conversation_a_turn_1_answer": extract_content(conv_a, 1),
                "conversation_a_turn_2_query": extract_content(conv_a, 2),
                "conversation_a_turn_2_answer": extract_content(conv_a, 3),
                # Conversation B breakdown (only 'content')
                "conversation_b_turn_1_query": extract_content(conv_b, 0),
                "conversation_b_turn_1_answer": extract_content(conv_b, 1),
                "conversation_b_turn_2_query": extract_content(conv_b, 2),
                "conversation_b_turn_2_answer": extract_content(conv_b, 3),
            }

            records.append(row)

    # Convert to DataFrame
    df = pd.DataFrame(records)

    # Save as CSV
    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"[INFO] Successfully converted {input_file} → {output_file}")

if __name__ == "__main__":
    jsonl_to_csv(INPUT_FILE, OUTPUT_FILE)