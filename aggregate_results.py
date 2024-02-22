import json
from pathlib import Path

import pandas as pd


def main(results_dir: Path):
    results = [x for x in results_dir.iterdir() if x.is_file() and x.name.endswith("_stats.csv")]
    results = sorted(results)
    print(results)

    stats = []
    # responses = []
    responses_df = pd.DataFrame()
    for r in results:
        # TODO: put this in a function
        test_name = r.name.split("_", maxsplit=1)[0]
        test_config = test_name.split("-")
        test_config = {
            "test_name": test_name,
            "server_type": test_config[0],
            "worker_type": test_config[1],
            "framework": test_config[2],
            "exec_type": test_config[3],
        }

        with open(results_dir / f"{test_name}_response_time.json") as f:
            response_data = json.load(f)
        res_df = pd.DataFrame(data={"response time": response_data})
        for k in reversed(test_config.keys()):
            v = test_config[k]
            res_df.insert(0, k, v)
        responses_df = pd.concat([responses_df, res_df])

        stat_df = pd.read_csv(r)
        stat = pd.concat([pd.Series(test_config), stat_df.iloc[1]])
        stats.append(stat)
    stats_df = pd.DataFrame(stats)
    stats_df.to_csv("aggregated_stats.csv")

    responses_df = pd.DataFrame(responses_df)
    responses_df.to_csv("aggregated_responses.csv")


if __name__ == "__main__":
    dir_ = "results"
    main(Path(dir_))