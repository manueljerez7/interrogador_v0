# test configuration file

import configparser


def conv_maxmin_ranges(sensors_lambdas):
    ranges = []
    for each_sensor in sensors_lambdas.keys():
        ranges.append(sensors_lambdas[each_sensor]["min"])
        ranges.append(sensors_lambdas[each_sensor]["max"])

    return str(len(sensors_lambdas)) + ":" + ", ".join(ranges)


def conv_formula(sensors_lambdas):
    formulas = []
    for each_sensor in sensors_lambdas.keys():
        sensor_info = []
        sensor_info.append(sensors_lambdas[each_sensor]["center"])
        sensor_info.append(sensors_lambdas[each_sensor]["fml"])
        formulas.append("[{}]".format(";".join(sensor_info)))

    return str(len(sensors_lambdas)) + ":" + ",".join(formulas)


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


config = configparser.ConfigParser()
config.read("configuration_1.ini")

channel_list = [item for item in config.sections() if "CH" in item]
config_dict = {}
config_dict["IP"] = config["ID"]["ip"]

for each_channel in channel_list:
    config_dict[each_channel] = read_channel_config(config[each_channel])
    config_dict[each_channel]["sensors"] = read_sensors_config(
        config["SENSORS" + each_channel.replace("CH", "")]
    )

print(conv_maxmin_ranges(config_dict["CH0"]["sensors"]))

a = conv_formula(config_dict["CH0"]["sensors"])
print("kk")
