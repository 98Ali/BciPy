import numpy as np
from helpers.load import load_trigger_data


def trial_reshaper(trigger_location, filtered_eeg, fs, k):
    """

    :param trigger_location: location of the trigger.txt file to read triggers from
    :param filtered_eeg: channel wise band pass filtered and downsampled eeg data with format: [channel x signal_length]
    :param fs: sampling frequency
    :param k: downsampling rate applied to the filtered eeg signal.

    :return [reshaped_trials, labels]: Return type is a list.
    reshaped_trials =   3 dimensional np array first dimension is trials
                        second dimension is channels and third dimension is time samples.
    labels = np array for every trial's class.

     """
    # Load triggers.txt
    trigger_txt = load_trigger_data(trigger_location)

    # Every trial's trigger timing
    triggers = [eval(line[2]) for line in trigger_txt]

    # triggers in seconds are mapped to triggers in number of samples. -1 is for indexing
    triggers = map(lambda x: int(x*fs/k) - 1, triggers)

    # Number of samples in half a second that we are interested in:
    num_samples = int(1.*fs/2/k)

    # 3 dimensional np array first dimension is trials
    #  second dimension is channels and third dimension is time samples.
    reshaped_trials = np.zeros((len(triggers), len(filtered_eeg), num_samples))

    # Label for every trial
    labels = np.zeros(len(triggers))

    # For every trial
    for trial in range(len(triggers)):
        if trigger_txt[trial][1] == 'target':
            labels[trial] = 1

        # For every channel
        for channel in range(len(filtered_eeg)):
            reshaped_trials[trial][channel] = filtered_eeg[channel][triggers[trial]:triggers[trial]+num_samples]

    return [reshaped_trials, labels]
