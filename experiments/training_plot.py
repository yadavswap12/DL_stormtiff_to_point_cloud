"""
Script to plot training history (training error vs epoch) for given experiment.

Swapnil 11/21
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Get CSV file path.
expfolder = "analysis_path\\"
experiment_directory = expfolder + "experiments\\"
history_directory = experiment_directory + "saved_training_history\\"
history_file = history_directory + "experiment5_history.csv"

# Load data from CSV file to a DataFrame and print first few lines from the DataFrame.
tr_hist_df = pd.read_csv(history_file)
print(tr_hist_df.head())

# ax = sns.lineplot(x="epoch", y="loss",data=tr_hist_df,legend='auto')
# ax = sns.lineplot(x="epoch", y="loss", data=tr_hist_df, legend='brief')
ax = sns.lineplot(x=tr_hist_df.index, y="loss", data=tr_hist_df, legend='brief')
# plt.xlim((2000, 5000))
# plt.ylim((0, 0.01))
plt.xlabel("epochs")
plt.legend(labels=['training error'])
plt.title("experiment_1_training_history", y=1.08)                                 
plt.savefig(history_directory + "experiment_1_training_history.jpg")
# plt.title("experiment_4_from_3k_to_20k_training_history", y=1.08)                                 
# plt.savefig(history_directory + "experiment_4_from_3k_to_20k_training_history.jpg")
plt.show()