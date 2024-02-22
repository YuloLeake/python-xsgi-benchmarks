import json
import time

from locust import FastHttpUser, events, task, constant
import locust.stats


locust.stats.PERCENTILES_TO_REPORT = [0.25, 0.50, 0.66, 0.75, 0.80, 0.90, 0.95, 0.98, 0.99, 0.999, 0.9999, 1.0]


RESPONSE_TIME = []


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--capture-response-time", type=bool, default=False, help="Capture elapsed response time")

@events.test_stop.add_listener
def _(environment, **kw):
    capture_response_time = environment.parsed_options.capture_response_time
    csv_prefix = environment.parsed_options.csv_prefix
    print(capture_response_time)
    print(csv_prefix)
    if capture_response_time and csv_prefix:
        filepath = f"{csv_prefix}_response_time.json"
        print(f"saving response time data to {filepath}")
        with open(filepath, "w") as f:
            json.dump(RESPONSE_TIME, f)


class AbstractPassThroughUser(FastHttpUser):
    # Prevent FastHttpUser from completely overwhelming the apps
    # 0.00005 good
    # 0.000005 still good
    # 0.0000005 still good
    wait_time = constant(0.0000005)

    @property
    def endpoint(self) -> str:
        ...

    def get_data(self):
        # TODO
        return {}

    @task
    def invoke(self):
        start = time.time()
        res = self.client.post(self.endpoint, json=self.get_data())
        if res.status_code == 200:
            RESPONSE_TIME.append(time.time() - start)


class SyncPassThroughUser(AbstractPassThroughUser):
    @property
    def endpoint(self) -> str:
        return "/pass-through-sync"


class AsyncPassThroughUser(AbstractPassThroughUser):
    @property
    def endpoint(self) -> str:
        return "/pass-through-async"


class AbstractCalcDistanceUser(FastHttpUser):
    # TODO: create another layer of abstraction for the client caller and the 
    #       type of data it returns.
    #       i.e., AbstractUser -> AbstractPassThroughUser -> SyncPassThroughUser

    # Prevent FastHttpUser from completely overwhelming the apps
    # 0.00005 good
    # 0.000005 still good
    # 0.0000005 still good
    wait_time = constant(0.0000005)

    @property
    def endpoint(self) -> str:
        ...

    def get_data(self):
        # TODO return a random data
        return {}

    @task
    def invoke(self):
        start = time.time()
        res = self.client.post(self.endpoint, json=self.get_data())
        if res.status_code == 200:
            RESPONSE_TIME.append(time.time() - start)


class SyncCalcDistanceUser(AbstractCalcDistanceUser):
    @property
    def endpoint(self) -> str:
        return "/calc-distance-sync"


class AsyncCalcDistanceUser(AbstractCalcDistanceUser):
    @property
    def endpoint(self) -> str:
        return "/calc-distance-async"
