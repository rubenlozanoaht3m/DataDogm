from pipeline.backend.pipeline import PipeLine
from pipeline.component.dataio import DataIO
from pipeline.component.input import Input
from pipeline.component.evaluation import Evaluation
from pipeline.component.hetero_lr import HeteroLR
from pipeline.component.hetero_secureboost import HeteroSecureBoost
from pipeline.component.intersection import Intersection
from pipeline.component.sampler import FederatedSample
from pipeline.interface.data import Data
from pipeline.backend.config import Backend
from pipeline.backend.config import WorkMode


guest = 9999
host = 10000
arbiter = 10002

guest_train_data = {"name": "breast_b", "namespace": "hetero"}
host_train_data = {"name": "breast_a", "namespace": "hetero"}

input_0 = Input(name="train_data")
print ("get input_0's init name {}".format(input_0.name))

pipeline = PipeLine().set_initiator(role='guest', party_id=guest).set_roles(guest=guest, host=host, arbiter=arbiter)
dataio_0 = DataIO(name="dataio_0")

dataio_0.get_party_instance(role='guest', party_id=guest).algorithm_param(with_label=True, output_format="dense")
dataio_0.get_party_instance(role='host', party_id=host).algorithm_param(with_label=False)

intersect_0 = Intersection(name="intersection_0")
federated_sample_0 = FederatedSample(name="federated_sample_0", mode="stratified",
      method="upsample", fractions=[[0, 1.5], [1, 2.0]])
hetero_lr_0 = HeteroLR(name="hetero_lr_0", early_stop="weight_diff", max_iter=10)
hetero_secureboost_0 = HeteroSecureBoost(name="hetero_secureboost_0", num_trees=5,
                                          tree_param={"max_depth":3, "tol":1e-2})
evaluation_0 = Evaluation(name="evaluation_0")
evaluation_1 = Evaluation(name="evaluation_1")

print ("get input_0's name {}".format(input_0.name))
pipeline.add_component(dataio_0, data=Data(data=input_0.data))
pipeline.add_component(intersect_0, data=Data(data=dataio_0.output.data))
pipeline.add_component(federated_sample_0, data=Data(data=intersect_0.output.data))
pipeline.add_component(hetero_lr_0, data=Data(train_data=federated_sample_0.output.data))
pipeline.add_component(hetero_secureboost_0, data=Data(train_data=federated_sample_0.output.data))
pipeline.add_component(evaluation_0, data=Data(data=hetero_lr_0.output.data))
pipeline.add_component(evaluation_1, data=Data(data=hetero_secureboost_0.output.data))

# pipeline.set_deploy_end_component([dataio_0])
# pipeline.deploy_component([dataio_0])

pipeline.compile()

pipeline.fit(backend=Backend.EGGROLL, work_mode=WorkMode.STANDALONE,
             feed_dict={input_0:
                           {"guest": {9999: guest_train_data},
                            "host": {
                              10000: host_train_data
                             }
                            }

                       })

print (pipeline.get_component("intersection_0").get_output_data())
print (pipeline.get_component("dataio_0").get_model_param())
print (pipeline.get_component("hetero_lr_0").get_model_param())
print (pipeline.get_component("federated_sample_0").get_model_param())
print (pipeline.get_component("hetero_secureboost_0").get_model_param())
print (pipeline.get_component("evaluation_0").summary())

# pipeline.get_component("intersection_0").summary("intersect_count", "intersect_rate")


# predict

pipeline = PipeLine().predict(backend=Backend.EGGROLL, work_mode=WorkMode.STANDALONE,
                              feed_dict={input_0:
                                             {"guest":
                                                  {9999: guest_train_data},
                                              "host": {
                                                  10000: host_train_data
                                              }
                                              }
                                         })

with open("output.pkl", "wb") as fout:
    fout.write(pipeline.dump())
