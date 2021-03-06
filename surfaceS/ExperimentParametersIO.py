################################################################################
# MIT License
#
# Copyright (c) 2019 surfaceS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
################################################################################

"""
 The ``ExperimentParametersIO`` module
 =====================================

 *Author:* [Jérémy Jayet](mailto:jeremy.jayet@epfl.ch)
 *Last modification:* 04.06.2019



 """

import json
import logging as log

def getDefaultParameters():
    """
     Prepare the default values for the experiment.

     """
    experimentParameters = {}
    experimentParameters['cnc_port'] = "COM5"
    experimentParameters['delay_before_measuring'] = 0.2
    experimentParameters['start_x'] = -270.0
    experimentParameters['start_y'] = -232.0
    experimentParameters['start_z'] = -2.003
    experimentParameters['nb_point_x'] = 2
    experimentParameters['nb_point_y'] = 2
    experimentParameters['step_x'] = 10.0
    experimentParameters['step_y'] = 10.0
    experimentParameters['sg_port'] = "COM6"
    experimentParameters['wave_type'] = "SINE"
    experimentParameters['frequency'] = 10000
    experimentParameters['channel_sg'] = 1
    experimentParameters['osc_ip'] = "128.178.201.9"
    experimentParameters['vibrometer_channel'] = 2
    experimentParameters['reference_channel'] = 1
    experimentParameters['unit_time_division'] = "MS"
    experimentParameters['unit_volt_division'] = "MV"
    experimentParameters['volt_division_vibrometer'] = 20
    experimentParameters['volt_division_reference'] = 500
    experimentParameters['time_division'] = 0.05
    experimentParameters['trigger_level'] = 100
    experimentParameters['trigger_mode'] = "SINGLE"
    experimentParameters['trigger_delay'] = 0
    experimentParameters['data_filename'] = "data.csv"

    return experimentParameters

def toJSONFromExpParams(experimentParameters):
    """
    Serialize the dictionnary into a JSON string.

    :param experimentParameters: The dictionnary containing the experiment parameters
    :type experimentParameters: dict

    :return: JSON representation of the experiment parameters
    :rtype: string

    """
    return json.dumps(experimentParameters, indent=4)

def toExpParamsFromJSON(jsonInput):
    """
    Parse a JSON input into the experiment parameters.

    :param jsonInput: JSON representation of the experiment parameters
    :type jsonInput: string

    :return: The dictionnary containing the experiment parameters
    :rtype: dict

    """
    try:
        experimentParameters = json.loads(jsonInput)
        return experimentParameters
    except Exception as e:
        log.error(str(e))
        return getDefaultParameters()

def readParametersFromFile(filename="experiment_parameters.json"):
    """
    Read the parameters from a JSON file.

    :param filename: The path to the file.
    :type filename: string

    :return: A dictionnary containing the experiment parameters.
    :rtype: dict

    """
    fhandle = open(filename)
    param = json.load(fhandle)
    fhandle.close()
    return param
def writeParametersToFile(filename, parameters):
    """
    Write the parameters to a JSON file.

    :param filename: The path to the file.
    :type filename: string
    :param parameters: The parameters to write.
    :type parameters: dict

    """
    try:
        fhandle = open(filename, "w")
        fhandle.write(toJSONFromExpParams(parameters))
        fhandle.close()
    except Exception as e :
        log.error(str(e))
        return getDefaultParameters()
