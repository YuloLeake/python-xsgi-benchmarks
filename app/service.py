import asyncio

import numpy


class Service:
    async def pass_through_async(self, data):
        return data

    def pass_through_sync(self, data):
        return data
    
    async def calc_distance_async(self):
        # TODO: actually return the distance
        # TODO: get data from the request
        # Create a random array of 100,000 integers between 0 and 100
        a = numpy.random.randint(0, 100, 100_000)
        for x in a:
            await asyncio.sleep(0)
            abs(x - 50)
        return []

    def calc_distance_sync(self):
        # TODO: actually return the distance
        # TODO: get data from the request
        # Create a random array of 100,000 integers between 0 and 100
        a = numpy.random.randint(0, 100, 100_000)
        for x in a:
            abs(x - 50)
        return []