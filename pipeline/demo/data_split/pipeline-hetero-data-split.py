from pipeline.backend.config import Backend
from pipeline.backend.config import WorkMode
from pipeline.backend.pipeline import PipeLine
from pipeline.component.dataio import DataIO
from pipeline.component.hetero_data_split import HeteroDataSplit
from pipeline.component.hetero_linr import HeteroLinR
from pipeline.component.input import Input
from pipeline.component.intersection import Intersection
from pipeline.interface.data import Data

guest = 9999
host = 10000
arbiter = 10002
backend = Backend.EGGROLL
work_mode = WorkMode.STANDALONE

guest_train_data = {"name": "motor_hetero_guest", "namespace": "experiment"}
host_train_data = {"name": "motor_hetero_host", "namespace": "experiment"}

input_0 = Input(name="train_data")

pipeline = PipeLine().set_initiator(role='guest', party_id=guest).set_roles(guest=guest, host=host, arbiter=arbiter)
dataio_0 = DataIO(name="dataio_0")

dataio_0.get_party_instance(role='guest', party_id=guest).algorithm_param(with_label=True, label_name="motor_speed",
                                                                         label_type="float", output_format="dense")
dataio_0.get_party_instance(role='host', party_id=host).algorithm_param(with_label=False)

intersection_0 = Intersection(name="intersection_0")
hetero_data_split_0 = HeteroDataSplit(name="hetero_data_split_0", stratified=True,
                                      test_size=0.3, split_points=[0.0, 0.2])
hetero_linr_0 = HeteroLinR(name="hetero_linr_0", penalty="L2", optimizer="sgd", tol=0.001,
                           alpha=0.01, max_iter=10, early_stop="weight_diff", batch_size=-1,
                           learning_rate=0.15, decay=0.0, decay_sqrt=False,
                           init_param={"init_method": "zeros"},
                           encrypted_mode_calculator_param={"mode": "fast"})

pipeline.add_component(dataio_0, data=Data(data=input_0.data))
pipeline.add_component(intersection_0, data=Data(data=dataio_0.output.data))
pipeline.add_component(hetero_data_split_0, data=Data(data=intersection_0.output.data))
pipeline.add_component(hetero_linr_0, data=Data(train_data=hetero_data_split_0.output.data.train_data,
                                                validate_data=hetero_data_split_0.output.data.test_data))


pipeline.compile()

pipeline.fit(backend=backend, work_mode=work_mode,
             feed_dict={input_0:
                           {"guest": {
                               9999: guest_train_data
                           },
                            "host": {
                              10000: host_train_data
                             }
                            }

                       })


print ("linr output data table is: ")
print (pipeline.get_component("hetero_linr_0").get_output_data_table())
print ("\ndata_split output data table is: ")
print (pipeline.get_component("hetero_data_split_0").get_output_data_table())
print ("\ndata_split output data is: ")
print (pipeline.get_component("hetero_data_split_0").get_output_data(limits=10))
print ("\nlinr output data is: ")
print (pipeline.get_component("hetero_linr_0").get_output_data(limits=10))
print ("\n summary content is: ")
print (pipeline.get_component("hetero_data_split_0").get_summary())
