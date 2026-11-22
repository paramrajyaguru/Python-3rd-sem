import csv
import json
import math
import random
import hashlib
from pathlib import Path
from collections import Counter

import matplotlib.pyplot as plt


# =========================================================
# SETTINGS
# =========================================================
OUTPUT_FOLDER = Path("hash_collision_output")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

SEED = 20261112
TRIALS = 2000
INPUT_SIZES = [300, 400, 500, 600, 800, 1000]
SIMULATION_BUCKETS = 65536
BUCKET_COUNTS = [256, 257, 512, 1024]


# =========================================================
# HELPER FUNCTIONS
# =========================================================
def save_csv(filename, rows):
    """Save a list of dictionaries as a CSV file."""
    if not rows:
        return

    path = OUTPUT_FOLDER / filename

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(rows[0].keys())
        )
        writer.writeheader()
        writer.writerows(rows)


def print_table(title, rows, columns):
    """
    columns: list of (dictionary key, display heading) pairs.
    """
    print("\n" + title)
    print("=" * len(title))

    formatted_rows = []

    for row in rows:
        formatted_row = []

        for key, heading in columns:
            value = row[key]

            if isinstance(value, float):
                formatted_row.append(f"{value:.6f}")
            else:
                formatted_row.append(str(value))

        formatted_rows.append(formatted_row)

    widths = []

    for index, (_, heading) in enumerate(columns):
        widths.append(
            max(
                [len(heading)]
                + [
                    len(row[index])
                    for row in formatted_rows
                ]
            )
        )

    header = " | ".join(
        heading.ljust(widths[index])
        for index, (_, heading) in enumerate(columns)
    )

    print(header)
    print("-" * len(header))

    for row in formatted_rows:
        print(
            " | ".join(
                value.ljust(widths[index])
                for index, value in enumerate(row)
            )
        )


def collision_metrics(bucket_labels, bucket_count):
    """Calculate collision and occupancy measures."""
    counts = Counter(bucket_labels)
    number_of_keys = sum(counts.values())

    return {
        "n": number_of_keys,
        "m": bucket_count,
        "U": len(counts),
        "D": number_of_keys - len(counts),
        "C": sum(
            count * (count - 1) // 2
            for count in counts.values()
        ),
        "L": max(counts.values(), default=0),
    }


def theoretical_values(number_of_keys, bucket_count):
    """Exact uniform-model probability and expected pairs."""
    if number_of_keys > bucket_count:
        probability = 1.0
    else:
        log_no_collision = sum(
            math.log1p(-i / bucket_count)
            for i in range(number_of_keys)
        )

        probability = -math.expm1(log_no_collision)

    expected_pairs = (
        number_of_keys
        * (number_of_keys - 1)
        / (2 * bucket_count)
    )

    return probability, expected_pairs


def hash_key(key, bucket_count, method):
    """Map an integer key into a bucket."""
    if method == "Modulo":
        return key % bucket_count

    if method == "SHA-256 reduced":
        digest = hashlib.sha256(
            str(key).encode("ascii")
        ).digest()

        return int.from_bytes(digest, "big") % bucket_count

    raise ValueError(f"Unknown hashing method: {method}")


# =========================================================
# CREATE AND SAVE THE DATASETS
# =========================================================
def create_datasets():
    # Each dataset has 600 distinct keys.
    sequential_keys = list(range(600))
    structured_keys = [256 * i for i in range(600)]

    assert len(set(sequential_keys)) == 600
    assert len(set(structured_keys)) == 600

    sequential_rows = [
        {"record_id": i + 1, "key": key}
        for i, key in enumerate(sequential_keys)
    ]

    structured_rows = [
        {"record_id": i + 1, "key": key}
        for i, key in enumerate(structured_keys)
    ]

    save_csv("dataset_sequential.csv", sequential_rows)
    save_csv("dataset_stride_256.csv", structured_rows)

    print_table(
        "Sequential dataset: first 10 of 600 records",
        sequential_rows[:10],
        [
            ("record_id", "Record ID"),
            ("key", "Key"),
        ],
    )

    print_table(
        "Structured dataset: first 10 of 600 records",
        structured_rows[:10],
        [
            ("record_id", "Record ID"),
            ("key", "Key"),
        ],
    )

    print("\nThe complete datasets are saved in CSV files.")

    return {
        "Sequential": sequential_keys,
        "Stride 256": structured_keys,
    }


# =========================================================
# EXPERIMENT A: UNIFORM RANDOM ASSIGNMENTS
# =========================================================
def experiment_a():
    rng = random.Random(SEED)

    summary_rows = []
    trial_rows = []

    for number_of_keys in INPUT_SIZES:
        collision_trials = 0
        total_pairs = 0

        for trial_number in range(1, TRIALS + 1):
            # Key identities are distinct: 0, 1, ..., n-1.
            # Bucket labels are sampled WITH replacement.
            labels = [
                rng.randrange(SIMULATION_BUCKETS)
                for _ in range(number_of_keys)
            ]

            metrics = collision_metrics(
                labels,
                SIMULATION_BUCKETS
            )

            collision_trials += int(metrics["C"] > 0)
            total_pairs += metrics["C"]

            trial_rows.append({
                "n": number_of_keys,
                "trial": trial_number,
                "m": SIMULATION_BUCKETS,
                "occupied_buckets": metrics["U"],
                "excess_insertions": metrics["D"],
                "colliding_pairs": metrics["C"],
                "maximum_occupancy": metrics["L"],
            })

            # Save one full example assignment per input size.
            # All trials can be regenerated using the fixed seed.
            if trial_number == 1:
                assignment_rows = [
                    {
                        "key": key,
                        "bucket": bucket,
                    }
                    for key, bucket in enumerate(labels)
                ]

                save_csv(
                    f"uniform_sample_n_{number_of_keys}.csv",
                    assignment_rows,
                )

                if number_of_keys == INPUT_SIZES[0]:
                    print_table(
                        "Uniform assignment sample: first 10 records",
                        assignment_rows[:10],
                        [
                            ("key", "Distinct key"),
                            ("bucket", "Assigned bucket"),
                        ],
                    )

        probability, expected_pairs = theoretical_values(
            number_of_keys,
            SIMULATION_BUCKETS,
        )

        summary_rows.append({
            "n": number_of_keys,
            "m": SIMULATION_BUCKETS,
            "trials": TRIALS,
            "collision_trials": collision_trials,
            "observed_probability": collision_trials / TRIALS,
            "theoretical_probability": probability,
            "observed_mean_pairs": total_pairs / TRIALS,
            "theoretical_mean_pairs": expected_pairs,
        })

    save_csv("experiment_a_results.csv", summary_rows)
    save_csv("experiment_a_trial_metrics.csv", trial_rows)

    print_table(
        "Experiment A: Collision probability",
        summary_rows,
        [
            ("n", "Keys"),
            ("collision_trials", "Collision trials"),
            ("observed_probability", "Observed probability"),
            ("theoretical_probability", "Theoretical probability"),
        ],
    )

    print_table(
        "Experiment A: Mean colliding pairs",
        summary_rows,
        [
            ("n", "Keys"),
            ("observed_mean_pairs", "Observed mean"),
            ("theoretical_mean_pairs", "Theoretical mean"),
        ],
    )

    return summary_rows


# =========================================================
# EXPERIMENT B: HASHING METHOD COMPARISON
# =========================================================
def experiment_b(datasets):
    summary_rows = []
    assignment_rows = []

    for dataset_name, keys in datasets.items():
        for bucket_count in BUCKET_COUNTS:
            for method in ["Modulo", "SHA-256 reduced"]:
                labels = [
                    hash_key(key, bucket_count, method)
                    for key in keys
                ]

                metrics = collision_metrics(
                    labels,
                    bucket_count
                )

                # Verify pigeonhole bounds.
                assert metrics["D"] >= max(
                    0, metrics["n"] - bucket_count
                )

                assert metrics["L"] >= math.ceil(
                    metrics["n"] / bucket_count
                )

                summary_rows.append({
                    "dataset": dataset_name,
                    "method": method,
                    **metrics,
                })

                # Retain every key-to-bucket mapping.
                for key, bucket in zip(keys, labels):
                    assignment_rows.append({
                        "dataset": dataset_name,
                        "method": method,
                        "bucket_count": bucket_count,
                        "key": key,
                        "assigned_bucket": bucket,
                    })

    save_csv("experiment_b_results.csv", summary_rows)
    save_csv("experiment_b_assignments.csv", assignment_rows)

    print_table(
        "Experiment B: Hash collision results",
        summary_rows,
        [
            ("dataset", "Dataset"),
            ("method", "Method"),
            ("m", "Buckets"),
            ("U", "Occupied"),
            ("D", "Excess"),
            ("C", "Pairs"),
            ("L", "Max occupancy"),
        ],
    )

    print("\nResult meanings:")
    print("U = number of occupied buckets")
    print("D = insertions after the first in each bucket")
    print("C = unordered pairs of keys sharing a bucket")
    print("L = maximum number of keys in one bucket")

    return summary_rows


# =========================================================
# GENERATE, SAVE AND DISPLAY GRAPHS
# =========================================================
def create_graphs(results_a, results_b):
    input_sizes = [row["n"] for row in results_a]

    # GRAPH 1: Collision probability
    fig1, ax1 = plt.subplots(figsize=(9, 5))

    ax1.plot(
        input_sizes,
        [
            row["theoretical_probability"]
            for row in results_a
        ],
        marker="o",
        label="Theoretical probability",
    )

    ax1.plot(
        input_sizes,
        [
            row["observed_probability"]
            for row in results_a
        ],
        marker="s",
        linestyle="--",
        label="Observed probability",
    )

    ax1.set_title("Collision Probability: Theory vs Experiment")
    ax1.set_xlabel("Number of distinct keys")
    ax1.set_ylabel("Probability of at least one collision")
    ax1.set_ylim(0, 1.05)
    ax1.grid(alpha=0.3)
    ax1.legend()

    fig1.tight_layout()
    fig1.savefig(
        OUTPUT_FOLDER / "graph_1_collision_probability.png",
        dpi=300,
    )

    # GRAPH 2: Mean colliding pairs
    fig2, ax2 = plt.subplots(figsize=(9, 5))

    ax2.plot(
        input_sizes,
        [
            row["theoretical_mean_pairs"]
            for row in results_a
        ],
        marker="o",
        label="Theoretical expected pairs",
    )

    ax2.plot(
        input_sizes,
        [
            row["observed_mean_pairs"]
            for row in results_a
        ],
        marker="s",
        linestyle="--",
        label="Observed mean pairs",
    )

    ax2.set_title("Colliding Pairs: Theory vs Experiment")
    ax2.set_xlabel("Number of distinct keys")
    ax2.set_ylabel("Mean number of colliding pairs")
    ax2.grid(alpha=0.3)
    ax2.legend()

    fig2.tight_layout()
    fig2.savefig(
        OUTPUT_FOLDER / "graph_2_colliding_pairs.png",
        dpi=300,
    )

    # GRAPH 3: Compare methods for each dataset
    fig3, axes = plt.subplots(1, 2, figsize=(12, 5))

    for ax, dataset_name in zip(
        axes,
        ["Sequential", "Stride 256"],
    ):
        for method in ["Modulo", "SHA-256 reduced"]:
            rows = [
                row
                for row in results_b
                if row["dataset"] == dataset_name
                and row["method"] == method
            ]

            ax.plot(
                [str(row["m"]) for row in rows],
                [row["C"] + 1 for row in rows],
                marker="o",
                label=method,
            )

        ax.set_title(f"{dataset_name} Keys")
        ax.set_xlabel("Number of buckets")
        ax.set_ylabel("Colliding pairs + 1 (log scale)")
        ax.set_yscale("log")
        ax.grid(alpha=0.3)
        ax.legend()

    fig3.suptitle("Hashing Method Comparison")
    fig3.tight_layout()

    fig3.savefig(
        OUTPUT_FOLDER / "graph_3_hashing_comparison.png",
        dpi=300,
    )

    print("\nAll three graphs have been saved as PNG files.")
    print(f"Output folder: {OUTPUT_FOLDER.resolve()}")

    plt.show()


# =========================================================
# MAIN PROGRAM
# =========================================================
def main():
    print("PIGEONHOLE PRINCIPLE AND HASH COLLISION ANALYSIS")

    # Validate collision calculations with a known example.
    assert collision_metrics([0, 0, 0, 1], 2) == {
        "n": 4,
        "m": 2,
        "U": 2,
        "D": 2,
        "C": 3,
        "L": 3,
    }

    datasets = create_datasets()

    print("\nRunning Experiment A...")
    results_a = experiment_a()

    print("\nRunning Experiment B...")
    results_b = experiment_b(datasets)

    with (OUTPUT_FOLDER / "results.json").open(
        "w", encoding="utf-8"
    ) as file:
        json.dump(
            {
                "seed": SEED,
                "trials": TRIALS,
                "experiment_a": results_a,
                "experiment_b": results_b,
            },
            file,
            indent=2,
        )

    create_graphs(results_a, results_b)


if __name__ == "__main__":
    main()