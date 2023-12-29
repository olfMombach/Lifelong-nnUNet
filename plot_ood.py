import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np
import pandas as pd
import os

def rename_tasks(task_name: str):
    if task_name == "Task097_DecathHip":
        return "DecathHip"
    elif task_name == "Task098_Dryad":
        return "Dryad"
    elif task_name == "Task099_HarP":
        return "HarP"
    elif task_name == "Task008_mHeartA":
        return "Siemens"
    elif task_name == "Task009_mHeartB":
        return "Philips"
    elif task_name == "Task011_Prostate-BIDMC":
        return "BIDMC"
    elif task_name == "Task012_Prostate-I2CVB":
        return "I2CVB"
    elif task_name == "Task013_Prostate-HK":
        return "HK"
    elif task_name == "Task015_Prostate-UCL":
        return "UCL"
    elif task_name == "Task016_Prostate-RUNMC":
        return "RUNMC"
    return "unknown task"

def task_color(task_name: str):
    if task_name == "Task097_DecathHip":
        return "red"
    elif task_name == "Task098_Dryad":
        return "green"
    elif task_name == "Task099_HarP":
        return "blue"
    elif task_name == "Task008_mHeartA":
        return "purple"
    elif task_name == "Task009_mHeartB":
        return "orange"
    elif task_name == "Task011_Prostate-BIDMC":
        return "brown"
    elif task_name == "Task012_Prostate-I2CVB":
        return "pink"
    elif task_name == "Task013_Prostate-HK":
        return "gray"
    elif task_name == "Task015_Prostate-UCL":
        return "olive"
    elif task_name == "Task016_Prostate-RUNMC":
        return "cyan"
    return "black"

def vae_mse():
    root_path = "/local/scratch/clmn1/master_thesis/tests/larger_conditional/evaluation/nnUNet_ext/2d/"
    all_tasks = "Task097_DecathHip_Task098_Dryad_Task099_HarP"
    trained_on = ["Task097_DecathHip"]
    trainer = "nnUNetTrainerVAERehearsalNoSkips"
    file = "ood_scores_vae_reconstruction.csv"

    threshold_on_95_train = 0.0055873438483104

    csv_path = os.path.join(root_path, all_tasks, '_'.join(trained_on),f"{trainer}__nnUNetPlansv2.1/Generic_UNet/SEQ/head_None/fold_0", file)
    return csv_path, trained_on, r"MSE of reconstruction and original > tau \implies OOD", threshold_on_95_train

def uncertainty():
    root_path = "/local/scratch/clmn1/master_thesis/tests/larger_conditional/evaluation/nnUNet_ext/2d/"
    all_tasks = "Task097_DecathHip_Task098_Dryad_Task099_HarP"
    trained_on = ["Task097_DecathHip"]
    trainer = "nnUNetTrainerVAERehearsalNoSkips"
    file = "ood_scores_uncertainty.csv"

    threshold_on_95_train = 0.0025233626365661

    csv_path = os.path.join(root_path, all_tasks, '_'.join(trained_on),f"{trainer}__nnUNetPlansv2.1/Generic_UNet/SEQ/head_None/fold_0", file)
    return csv_path, trained_on, r"Uncertainty > \tau \implies OOD", threshold_on_95_train


# [x] threshold = 0.0171928624132354 (estimated on train and val)
# [ ] threshold = 0.0055873438483104 (estimated on train only)
def uncertainty_mse_temperature():
    root_path = "/local/scratch/clmn1/master_thesis/tests/larger_conditional/evaluation/nnUNet_ext/2d/"
    all_tasks = "Task097_DecathHip_Task098_Dryad_Task099_HarP"
    trained_on = ["Task097_DecathHip"]
    trainer = "nnUNetTrainerVAERehearsalNoSkips"
    file = "ood_scores_uncertainty_mse_temperature.csv"

    threshold_on_95_train = 0.0021607652306556

    csv_path = os.path.join(root_path, all_tasks, '_'.join(trained_on),f"{trainer}__nnUNetPlansv2.1/Generic_UNet/SEQ/head_None/fold_0", file)
    return csv_path, trained_on, r"Scaled Uncertainty > \tau \implies OOD", threshold_on_95_train








csv_path, trained_on, title, threshold = uncertainty_mse_temperature()
df = pd.read_csv(csv_path, sep="\t")


tasks = list(set(df.loc[:,"Task"]))
tasks.sort()

min_ood_score = 0
max_ood_score = max(df['ood_score'])
for task in tasks:
    xs = np.linspace(min_ood_score, max_ood_score, 1000)


    split_data = task in trained_on
    if split_data:
        arr = [False, True]
    else:
        arr = [None]
    for val in arr:
        subset_df = df[df['Task'] == task]
        if split_data:
            subset_df = subset_df[subset_df['is_val'] == val] #only validation data

        y = []
        for x in xs:
            #count amount of values in subset_df where values at column 'ood_score' is less than x
            y.append(len([v for v in subset_df['ood_score'] if v > x]) / len(subset_df))
        assert len(y) == len(xs)
        if task in trained_on:
            sns.lineplot(x=xs, y=y, label=f"{rename_tasks(task)}, {'val' if val else 'train'}", linestyle='dashed' if val else 'solid', color=task_color(task))
        else:
            sns.lineplot(x=xs, y=y, label=rename_tasks(task), linestyle='dashed', color=task_color(task))
if threshold is not None:
    plt.axvline(x=threshold, color='black', linestyle='dashed', label="95% threshold")
plt.xlabel(r"Threshold \tau")
plt.ylabel("Percentage of samples classified as OOD")
plt.title(title)
plt.savefig("plot_ood.png", bbox_inches='tight')