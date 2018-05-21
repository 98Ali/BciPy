# -*- coding: utf-8 -*-
import acquisition.datastream.generator as generator
import acquisition.protocols.registry as registry
from acquisition.client import Client, _Clock
from acquisition.datastream.server import start_socket_server, await_start
from acquisition.processor import FileWriter
from acquisition.datastream.lsl_server import LslDataServer

# Channels relevant for analysis, for each supported device.
analysis_channels_by_device = {
    'DSI': ["P3", "C3", "F3", "Fz", "F4", "C4", "P4", "Cz", "A1", "Fp1", "Fp2",
            "T3", "T5", "O1", "O2", "F7", "F8", "A2", "T6", "T4"],
    'g.USBamp-2': ["Ch1", "Ch2", "Ch3", "Ch4", "Ch5", "Ch6", "Ch7", "Ch8",
                   "Ch9", "Ch10", "Ch11", "Ch12", "Ch13", "Ch14", "Ch15",
                   "Ch16"]
}

def init_eeg_acquisition(parameters, save_folder,
                         clock=_Clock(), server=False):
    """
    Initializes a client that connects with the EEG data source and begins
    data collection.

    Parameters
    ----------
        parameters : dict
            configuration details regarding the device type and other relevant
            connection information.
             {
               "acq_device": str,
               "acq_host": str,
               "acq_port": int,
               "buffer_name": str,
               "raw_data_name": str
             }
        clock : Clock, optional
            optional clock used in the client; see client for details.
        server : bool, optional
            optionally start a server that streams random DSI data; defaults
            to true; if this is True, the client will also be a DSI client.
    Returns
    -------
        (client, server) tuple
    """

    # Initialize the needed DAQ Parameters
    host = parameters['acq_host']
    port = parameters['acq_port']

    parameters = {
        'buffer_name': save_folder + '/' + parameters['buffer_name'],
        'device': parameters['acq_device'],
        'filename': save_folder + '/' + parameters['raw_data_name'],
        'connection_params': {'host': host,
                              'port': port}}

    # Set configuration parameters (with default values if not provided).
    buffer_name = parameters.get('buffer_name', 'buffer.db')
    connection_params = parameters.get('connection_params', {})
    device_name = parameters.get('device', 'DSI')
    filename = parameters.get('filename', 'rawdata.csv')

    dataserver = False
    if server:
        if device_name == 'DSI':
            protocol = registry.default_protocol(device_name)
            dataserver, port = start_socket_server(protocol, host, port)
            connection_params['port'] = port
        elif device_name == 'LSL':
            channels = ['ch{}'.format(c + 1) for c in range(16)]
            dataserver = LslDataServer(params={'name': 'LSL',
                                               'channels': channels,
                                               'hz': 512},
                                       generator=generator.random_data(
                                           channel_count=16))
            await_start(dataserver)

    Device = registry.find_device(device_name)

    # Start a client. We assume that the channels and fs will be set on the
    # device; add a channel parameter to Device to override!
    client = Client(device=Device(connection_params=connection_params),
                    processor=FileWriter(filename=filename),
                    buffer_name=buffer_name,
                    clock=clock)

    client.start_acquisition()

    # If we're using a server or data generator, there is no reason to
    # calibrate data.
    if server:
        client.is_calibrated = True

    return (client, dataserver)
