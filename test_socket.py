# from gpib_ctypes import make_default_gpib

# make_default_gpib()

import pyvisa  # for scpi
import time  # for sleep
from readTraces import gen_csv_zip
import logging
import csv
import configparser
import argparse
from plotGraph import plotGraph
DELAY = 0.1


def read_channel_config(channel_config):
    config_dict = {}
    for key, value in channel_config.items():
        config_dict[key] = value

    return config_dict


def read_sensors_config(raw_config):
    struct_data = {}

    for key, value in raw_config.items():
        struct_data[key] = {}
        sep_items = value.replace(",", ".").split()
        struct_data[key]["center"] = sep_items[0]
        struct_data[key]["min"] = sep_items[1]
        struct_data[key]["max"] = sep_items[2]
        struct_data[key]["fml"] = sep_items[3]

    return struct_data


def read_config_file(file):
    config = configparser.ConfigParser()
    config.read(file)

    channel_list = [item for item in config.sections() if "CH" in item]
    config_dict = {}
    config_dict["IP"] = config["ID"]["ip"]
    config_dict["RATE"] = config["ID"]["rate"]

    for each_channel in channel_list:
        config_dict[each_channel] = read_channel_config(config[each_channel])
        config_dict[each_channel]["sensors"] = read_sensors_config(
            config["SENSORS" + each_channel.replace("CH", "")]
        )
    return config_dict


def open_session(log_file):
    logging.basicConfig(
        filename=log_file,
        filemode="a",
        level=logging.DEBUG,
    )

    try:
        logging.info("Openning session")
        rm = pyvisa.ResourceManager("@py")
        # rm = pyvisa.ResourceManager()

    except Exception as e:
        print(e)
        logging.error("Exception occurred", exc_info=True)

        exit()

    return rm


def close_session(rm):
    try:
        rm.close()
        logging.info("Closing session")
        logging.getLogger().handlers[0].close()

    except Exception as e:
        print(e)
        logging.error("Exception occurred", exc_info=True)

        exit()

    # close_session(rm = visa_session, inst=inst_handler)


class meter:
    def __init__(self, visa_handler, id):
        self.inst_handler = visa_handler
        self.id = id

    def __enter__(
        self,
    ):
        try:
            self.inst_handler = visa_handler.open_resource('TCPIP::10.0.0.10::3500::SOCKET')
            self.inst_handler.timeout = 5000
            self.inst_handler.read_termination = '\r'
        except Exception as e:
            print(e)
            logging.error(
                "Exception occurred when openning meter {}".format(self.id),
                exc_info=True,
            )

            exit()

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            logging.info("Closing {}".format(self.id))
            self.inst_handler.close()

        except Exception as e:
            print(e)
            logging.error("Exception occurred", exc_info=True)

    def write(self, cmd):
        self.__enter__()
        logging.debug("Sending command {} to meter".format(cmd))

        try:
            self.inst_handler.query(cmd)
            time.sleep(DELAY)

        except Exception as e:
            logging.warning("Command {} cannot be written".format(cmd), exc_info=True)
            status = False

    def query(self, cmd):
        try:
            response = self.inst_handler.query(cmd)

        except Exception as e:
            print(e)
            logging.warning(
                "Exception occurred during querying command {}".format(cmd),
                exc_info=True,
            )

            response = None

        return response

    @staticmethod
    def conv_maxmin_ranges(sensors_lambdas):
        ranges = []
        for each_sensor in sensors_lambdas.keys():
            ranges.append(sensors_lambdas[each_sensor]["min"])
            ranges.append(sensors_lambdas[each_sensor]["max"])

        return str(len(sensors_lambdas)) + ":" + ", ".join(ranges)

    @staticmethod
    def conv_formula(sensors_lambdas):
        formulas = []
        for each_sensor in sensors_lambdas.keys():
            sensor_info = []
            sensor_info.append(sensors_lambdas[each_sensor]["center"])
            sensor_info.append(sensors_lambdas[each_sensor]["fml"])
            formulas.append("[{}]".format(";".join(sensor_info)))

        return str(len(sensors_lambdas)) + ":" + ",".join(formulas)

    def configure(self, config_dict):
        self.__enter__()

        logging.info("Configuring meter")

        cmd_sequence = [
            ":ACQU:STAR",
            ":ACQU:CONF:THRE:CHAN:0:{}".format(config_dict["CH0"]["threshold"]),
            ":ACQU:CONF:RATE:{}".format(config_dict["RATE"]),
            ":ACQU:CONF:RANG:ENAB",
            ":ACQU:CONF:RANG:WAVE:0:{}".format(
                self.conv_maxmin_ranges(config_dict["CH0"]["sensors"])
            ),
            ":ACQU:CONF:RANG:FOR:0:".format(
                self.conv_formula(config_dict["CH0"]["sensors"])
            ),
            ":ACQU:STAR",
            ":ACQU:STOP",
        ]

        # preparar la lista de configuracion
        for each_command in cmd_sequence:
            self.query(each_command)

    def check(self):
        self.__enter__()

        logging.info("Checking configuration ... ")
        cmd_sequence = [
            ":IDEN?",
            ":STAT?",
            ":ACQU:STAR",
            ":RECA",
            ":ACQU:CONF:THRE:CHAN:0?",
            ":ACQU:CONF:RANG:WAVE:0?",
            ":ACQU:CONF:RANG:FORM:0?",
            ":ACQU:CONF:RANG:STAT?",
            ":ACQU:STOP",
        ]

        for each_cmd in cmd_sequence:
            response = self.query(each_cmd)
            logging.debug("Command: {}".format(each_cmd))
            logging.debug("Response: {}".format(response))

        logging.info("... {}".format(self.query(":STAT?")))


def arg_proc():
    my_parser = argparse.ArgumentParser()
    # my_parser.version = "1.0"

    my_parser.add_argument(
        "-c",
        "--config_file",
        action="store",
        type=str,
        required=True,
        help="configuration file",
    )

    my_parser.add_argument(
        "-s",
        "--samples",
        action="store",
        type=int,
        required=True,
        help="number of samples",
    )
    my_parser.add_argument(
        "-t",
        "--temperature",
        action="store",
        type=float,
        required=True,
        help="reference temperature (and output filename) ",
    )
    my_parser.add_argument(
        "-l",
        "--log_file",
        action="store",
        type=str,
        required=True,
        default="default.log",
        help="log file",
    )

    return my_parser.parse_args()


# ------------ MAIN ------------


args = arg_proc()

visa_handler = open_session(log_file=args.log_file)

config_dict = read_config_file(file=args.config_file)

fs22 = meter(visa_handler=visa_handler,id=config_dict["IP"])

fs22.configure(config_dict=config_dict)
fs22.check()
traces_list = []
temp_list = []
peaks_loc_list = []
peak_val_list = []

# iniciar medida
fs22.write(":ACQU:STAR")
fs22.write(":ACQU:RECA")

for sample_index in range(args.samples):


    traces_list.append(fs22.query(":ACQU:OSAT:CHAN:0?").replace(":ACK:", ""))
    temp_list.append(fs22.query(":ACQU:ENGI:CHAN:0?").replace(":ACK:", ""))
    peak_val_list.append(fs22.query(":ACQU:POWE:CHAN:0?").replace(":ACK:", ""))
    peaks_loc_list.append(fs22.query(":ACQU:WAVE:CHAN:0?").replace(":ACK:", ""))
    print(sample_index)
    time.sleep(1)

fs22.write(":ACQU:STOP")

with open(str(args.temperature) + "_os", "w", newline="") as csvfile:
    # Create a CSV writer object
    csv_writer = csv.writer(csvfile)
    csv_writer.writerows(traces_list)

with open(str(args.temperature) + "_temp", "w", newline="") as csvfile:
    # Create a CSV writer object
    csv_writer = csv.writer(csvfile)
    csv_writer.writerows(temp_list)

with open(str(args.temperature) + "_loc", "w", newline="") as csvfile:
    # Create a CSV writer object
    csv_writer = csv.writer(csvfile)
    csv_writer.writerows(peaks_loc_list)

with open(str(args.temperature) + "_peaks", "w", newline="") as csvfile:
    # Create a CSV writer object
    csv_writer = csv.writer(csvfile)
    csv_writer.writerows(peak_val_list)


visa_handler.close()

gen_csv_zip(str(args.temperature),
    [str(args.temperature) + "_os",
     str(args.temperature) + "_temp",
     str(args.temperature) + "_loc",
     str(args.temperature) + "_peaks"])

plotGraph(str(args.temperature)+".zip",str(args.temperature) + "_temp.csv",1)