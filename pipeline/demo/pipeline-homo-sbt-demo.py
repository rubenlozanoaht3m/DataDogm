from pipeline.backend.pipeline import PipeLine
from pipeline.component.dataio import DataIO
from pipeline.component.input import Input
from pipeline.component.homo_secureboost import HomoSecureBoost
from pipeline.interface.data import Data
from pipeline.backend.config import Backend
from pipeline.backend.config import WorkMode


guest = 9999
host = 10000
arbiter = 10002

guest_train_data = {"name": "homo_breast_guest", "namespace": "homo_breast_guest"}
host_train_data = {"name": "homo_breast_host", "namespace": "homo_breast_host"}

input_0 = Input(name="train_data")
print ("get input_0's init name {}".format(input_0.name))

pipeline = PipeLine().set_initiator(role='guest', party_id=guest).set_roles(guest=guest, host=host, arbiter=arbiter)
dataio_0 = DataIO(name="dataio_0")

dataio_0.get_party_instance(role='guest', party_id=guest).algorithm_param(with_label=True, output_format="dense")
dataio_0.get_party_instance(role='host', party_id=host).algorithm_param(with_label=True)

homo_secureboost_0 = HomoSecureBoost(name="homo_secureboost_0")

print ("get input_0's name {}".format(input_0.name))
pipeline.add_component(dataio_0, data=Data(data=input_0.data))
pipeline.add_component(homo_secureboost_0, data=Data(data=dataio_0.output.data))

pipeline.compile()

pipeline.fit(backend=Backend.EGGROLL, work_mode=WorkMode.STANDALONE,
             feed_dict={input_0:
                           {"guest": {9999: guest_train_data},
                            "host": {
                              10000: host_train_data
                             }
                            }

                       })

print (pipeline.get_component("dataio_0").get_model_param())
print (pipeline.get_component("homo_secureboost_0").summary())

with open("output.pkl", "wb") as fout:
    fout.write(pipeline.dump())
