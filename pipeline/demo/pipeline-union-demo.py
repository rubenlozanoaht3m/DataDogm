from pipeline.backend.pipeline import PipeLine
from pipeline.component.dataio import DataIO
from pipeline.component.input import Input
from pipeline.component.intersection import Intersection
from pipeline.component.union import Union
from pipeline.interface.data import Data
from pipeline.interface.model import Model
from pipeline.backend.config import Backend
from pipeline.backend.config import WorkMode


guest = 9999
hosts = [10000, 10001]
arbiter = 10002

guest_train_data = {"name": "breast_b", "namespace": "hetero"}
host_train_data = [{"name": "breast_a", "namespace": "hetero"},
                   {"name": "breast_a", "namespace": "hetero"},
                   {"name": "breast_a", "namespace": "hetero"}]

input_0 = Input(name="train_data_0")
input_1 = Input(name="train_data_1")
print ("get input_0's init name {}".format(input_0.name))
print ("get input_1's init name {}".format(input_1.name))


pipeline = PipeLine().set_initiator(role='guest', party_id=9999).set_roles(guest=9999, host=hosts, arbiter=arbiter)
dataio_0 = DataIO(name="dataio_0")
dataio_1 = DataIO(name="dataio_1")

dataio_0.get_party_instance(role='guest', party_id=9999).algorithm_param(with_label=True, output_format="dense")
dataio_0.get_party_instance(role='host', party_id=[10000, 10001]).algorithm_param(with_label=False)

dataio_1.get_party_instance(role='guest', party_id=9999).algorithm_param(with_label=True, output_format="dense")
dataio_1.get_party_instance(role='host', party_id=[10000, 10001]).algorithm_param(with_label=False)

intersect_0 = Intersection(name="intersection_0")
intersect_1 = Intersection(name="intersection_1")

union_0 = Union(name="union_0")

print ("get input_0's name {}".format(input_0.name))
print ("get input_1's name {}".format(input_1.name))
pipeline.add_component(dataio_0, data=Data(data=input_0.data))
pipeline.add_component(dataio_1, data=Data(data=input_1.data), model=Model(dataio_0.output.model_output))
pipeline.add_component(intersect_0, data=Data(data=dataio_0.output.data))
pipeline.add_component(intersect_1, data=Data(data=dataio_1.output.data))
pipeline.add_component(union_0, data=Data(data=[intersect_0.output.data, intersect_1.output.data]))

# pipeline.set_deploy_end_component([dataio_0])
# pipeline.deploy_component([dataio_0])

pipeline.compile()

pipeline.fit(backend=Backend.EGGROLL, work_mode=WorkMode.STANDALONE,
             feed_dict={input_0:
                           {"guest":
                                {9999: guest_train_data},
                            "host": {
                                10000: host_train_data[0],
                                10001: host_train_data[1]
                                }
                            },
                        input_1:
                            {"guest":
                                {9999: guest_train_data},
                            "host": {
                                10000: host_train_data[0],
                                10001: host_train_data[1]
                                }
                            },

                       })

# print (pipeline.get_component("intersection_0").get_output_data())
# print (pipeline.get_component("dataio_0").get_model_param())
print(pipeline.get_component("union_0").summary())
# pipeline.get_component("intersection_0").summary("intersect_count", "intersect_rate")

with open("output.pkl", "wb") as fout:
    fout.write(pipeline.dump())
