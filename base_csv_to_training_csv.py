# convert_mt_bench_csv_with_qid.py
import pandas as pd

INPUT_FILE = "mt_bench_human_judgements.csv"
OUTPUT_FILE = "mt_bench_training.csv"

def process_csv(input_file, output_file):
    # Load CSV
    df = pd.read_csv(input_file)

    # New dataframe rows will go here
    new_rows = []

    for _, row in df.iterrows():
        turn = row["turn"]
        winner = row["winner"]
        qid = row["question_id"]

        # Resolve winner to actual model name or "tie"
        if winner == "model_a":
            winner_model = row["model_a"]
            prefix = "conversation_a"
        elif winner == "model_b":
            winner_model = row["model_b"]
            prefix = "conversation_b"
        else:
            winner_model = "tie"
            prefix = "conversation_a"  # If tie data corresponding to model a is populated.

        # Build new row depending on turn and winner
        if turn == 1:
            if winner_model == "tie":
                new_row = {
                    "question_id": qid,
                    "turn": turn,
                    "turn_1_query": row[f"{prefix}_turn_1_query"],
                    "turn_1_answer": None,
                    "turn_2_query": None,
                    "winner": "tie"
                }
            else:
                new_row = {
                    "question_id": qid,
                    "turn": turn,
                    "turn_1_query": row[f"{prefix}_turn_1_query"],
                    "turn_1_answer": None,
                    "turn_2_query": None,
                    "winner": winner_model
                }

        elif turn == 2:
            if winner_model == "tie":
                new_row = {
                    "question_id": qid,
                    "turn": turn,
                    "turn_1_query": row[f"{prefix}_turn_1_query"],
                    "turn_1_answer": row[f"{prefix}_turn_1_answer"],
                    "turn_2_query": row[f"{prefix}_turn_2_query"],
                    "winner": "tie"
                }
            else:
                new_row = {
                    "question_id": qid,
                    "turn": turn,
                    "turn_1_query": row[f"{prefix}_turn_1_query"],
                    "turn_1_answer": row[f"{prefix}_turn_1_answer"],
                    "turn_2_query": row[f"{prefix}_turn_2_query"],
                    "winner": winner_model
                }
        else:
            continue  # skip unexpected turn values

        new_rows.append(new_row)

    # Convert to dataframe
    new_df = pd.DataFrame(new_rows, columns=[
        "question_id", "turn", "turn_1_query", "turn_1_answer", "turn_2_query", "winner"
    ])

    # Save to CSV
    new_df.to_csv(output_file, index=False)
    print(f"[INFO] Processed CSV saved to {output_file}")

if __name__ == "__main__":
    process_csv(INPUT_FILE, OUTPUT_FILE)
