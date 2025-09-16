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

        def build_row(prefix, winner_model):
            """Helper to build one row for the given conversation prefix and winner model."""
            if turn == 1:
                return {
                    "question_id": qid,
                    "turn": turn,
                    "turn_1_query": row[f"{prefix}_turn_1_query"],
                    "turn_1_answer": None,
                    "turn_2_query": None,
                    "winner": winner_model
                }
            elif turn == 2:
                return {
                    "question_id": qid,
                    "turn": turn,
                    "turn_1_query": row[f"{prefix}_turn_1_query"],
                    "turn_1_answer": row[f"{prefix}_turn_1_answer"],
                    "turn_2_query": row[f"{prefix}_turn_2_query"],
                    "winner": winner_model
                }
            else:
                return None

        # Case 1: Clear winner
        if winner == "model_a":
            new_rows.append(build_row("conversation_a", row["model_a"]))
        elif winner == "model_b":
            new_rows.append(build_row("conversation_b", row["model_b"]))

        # Case 2: Tie → create TWO rows (one per model)
        elif str(winner).strip().lower() == "tie":
            row_a = build_row("conversation_a", row["model_a"])
            row_b = build_row("conversation_b", row["model_b"])
            if row_a: new_rows.append(row_a)
            if row_b: new_rows.append(row_b)

    # Convert to dataframe
    new_df = pd.DataFrame(new_rows, columns=[
        "question_id", "turn", "turn_1_query", "turn_1_answer", "turn_2_query", "winner"
    ])

    # Save to CSV
    new_df.to_csv(output_file, index=False)
    print(f"[INFO] Processed CSV saved to {output_file}")

if __name__ == "__main__":
    process_csv(INPUT_FILE, OUTPUT_FILE)