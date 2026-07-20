#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from statistics import median


def read_jsonl(path):
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def read_split(path):
    return {line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()}


def load_ground_truth(captions_path, split_path, task):
    split_ids = read_split(split_path)
    captions = [row for row in read_jsonl(captions_path) if row["video_id"] in split_ids]
    if task == "t2v":
        return {row["caption_id"]: {row["video_id"]} for row in captions}
    if task == "v2t":
        gt = {}
        for row in captions:
            gt.setdefault(row["video_id"], set()).add(row["caption_id"])
        return gt
    raise ValueError(f"Unsupported task: {task}")


def rank_of_first_positive(predictions, positives):
    for rank, item in enumerate(predictions, start=1):
        if item in positives:
            return rank
    return None


def evaluate(gt, pred_rows, ks):
    ranks = []
    missing = 0
    for query_id, positives in gt.items():
        row = pred_rows.get(query_id)
        if row is None:
            missing += 1
            ranks.append(None)
            continue
        rank = rank_of_first_positive(row, positives)
        ranks.append(rank)

    valid_ranks = [r for r in ranks if r is not None]
    n = len(gt)
    metrics = {
        "num_queries": n,
        "missing_predictions": missing,
        "not_found_in_predictions": n - missing - len(valid_ranks),
    }
    recalls = {}
    for k in ks:
        recalls[f"R@{k}"] = sum(1 for r in valid_ranks if r <= k) / n if n else 0.0
    metrics.update(recalls)
    metrics["mR"] = sum(recalls.values()) / len(recalls) if recalls else 0.0
    metrics["median_rank"] = median(valid_ranks) if valid_ranks else None
    metrics["mean_rank"] = sum(valid_ranks) / len(valid_ranks) if valid_ranks else None
    return metrics


def main():
    parser = argparse.ArgumentParser(description="Evaluate AirVT-15k text-video retrieval predictions.")
    parser.add_argument("--captions", required=True, help="Path to metadata/captions.jsonl")
    parser.add_argument("--split", required=True, help="Path to metadata/splits/*.txt")
    parser.add_argument("--predictions", required=True, help="Prediction JSONL file")
    parser.add_argument("--task", choices=["t2v", "v2t"], required=True)
    parser.add_argument("--ks", default="1,5,10", help="Comma-separated recall cutoffs")
    args = parser.parse_args()

    ks = [int(x) for x in args.ks.split(",") if x.strip()]
    gt = load_ground_truth(args.captions, args.split, args.task)
    pred_rows = {}
    for row in read_jsonl(args.predictions):
        query_id = row["query_id"]
        predictions = row.get("predictions") or row.get("results") or []
        pred_rows[query_id] = predictions

    print(json.dumps(evaluate(gt, pred_rows, ks), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
