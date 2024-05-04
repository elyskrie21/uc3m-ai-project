import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from itertools import cycle
from MFIS_Read_Functions import *
from gui import *


def main():
    applications = readApplicationsFile()
    fuzzifierSetsDict = readFuzzySetsFile('Files/InputVarSets.txt')
    fuzzySystemSet = readFuzzySetsFile('Files/Risks.txt')
    fuzzySystem = readRulesFile()

    cycol = cycle('bgrcmk')

    # File to write to
    results = open('Files/Results.txt', 'w')

    # First plotting the fuzzifier set
    fig, axs = plt.subplots(nrows=7, figsize=(8, 24))

    for key in fuzzifierSetsDict:
        # getting the membership function and  universe variables.
        fuzzySet = fuzzifierSetsDict.get(key)

        # visuals
        match fuzzySet.var:
            case "Age":
                axs[0].plot(fuzzySet.x, fuzzySet.y, c=next(cycol),
                            linewidth=1.5, label=fuzzySet.label)
                axs[0].set_title("AGE")
                axs[0].legend()
            case "IncomeLevel":
                axs[1].plot(fuzzySet.x, fuzzySet.y, c=next(cycol),
                            linewidth=1.5, label=fuzzySet.label)
                axs[1].set_title("IncomeLevel")
                axs[1].legend()
            case "Assets":
                axs[2].plot(fuzzySet.x, fuzzySet.y, c=next(cycol),
                            linewidth=1.5, label=fuzzySet.label)
                axs[2].set_title("Assets")
                axs[2].legend()
            case "Amount":
                axs[3].plot(fuzzySet.x, fuzzySet.y, c=next(cycol),
                            linewidth=1.5, label=fuzzySet.label)
                axs[3].set_title("Amount")
                axs[3].legend()
            case "Job":
                axs[4].plot(fuzzySet.x, fuzzySet.y, c=next(cycol),
                            linewidth=1.5, label=fuzzySet.label)
                axs[4].set_title("Job")
                axs[4].legend()
            case "History":
                axs[5].plot(fuzzySet.x, fuzzySet.y, c=next(cycol),
                            linewidth=1.5, label=fuzzySet.label)
                axs[5].set_title("History")
                axs[5].legend()
            case _:
                print("Unable to find axs to plot from for: " + fuzzySet.var)

    for application in applications:
        # Fuzzyifcation
        age = application.data[0][1]
        IncomeLevel = application.data[1][1]
        Assets = application.data[2][1]
        Amount = application.data[3][1]
        Job = application.data[4][1]
        History = application.data[5][1]

        # generating interp_memberships
        interp_memberhips = {}
        for key in fuzzifierSetsDict:
            # getting the membership function and  universe variables.
            fuzzySet = fuzzifierSetsDict.get(key)

            match fuzzySet.var:
                case "Age":
                    interp_memberhips[key] = fuzz.interp_membership(
                        fuzzySet.x, fuzzySet.y, age)
                case "IncomeLevel":
                    interp_memberhips[key] = fuzz.interp_membership(
                        fuzzySet.x, fuzzySet.y, IncomeLevel)
                case "Assets":
                    interp_memberhips[key] = fuzz.interp_membership(
                        fuzzySet.x, fuzzySet.y, Assets)
                case "Amount":
                    interp_memberhips[key] = fuzz.interp_membership(
                        fuzzySet.x, fuzzySet.y, Amount)
                case "Job":
                    interp_memberhips[key] = fuzz.interp_membership(
                        fuzzySet.x, fuzzySet.y, Job)
                case "History":
                    interp_memberhips[key] = fuzz.interp_membership(
                        fuzzySet.x, fuzzySet.y, History)
                case _:
                    print("Unable to find membership function for: " + fuzzySet.var)

        # Have to now create rules
        rules = []
        for rule in fuzzySystem:
            arrayMin = [1]
            for antecedent in rule.antecedent:
                im = interp_memberhips.get(antecedent)
                arrayMin = np.fmin(arrayMin, im)

            # Now apply this by clipping the top off the corresponding output
            # membership function with `np.fmin`
            rules.append(
                np.fmin(arrayMin, fuzzySystemSet.get(rule.consequent).y))

        # for rule in rules:
        #     for key in fuzzySystemSet:
        #         risk = fuzzySystemSet.get(key)
        #         color = next(cycol)
        #         axs[6].fill_between(risk.x, np.zeros_like(risk.x), rule, facecolor= color, alpha=0.7)
        #         axs[6].plot(risk.x, risk.y, color, linewidth=0.5, linestyle='--', )

        # Defuzzification
        # Aggregate all output membership functions together
        aggregated = [0]
        for rule in rules:
            aggregated = np.fmax(aggregated, rule)

        # Need x domain of an arbitary risk funcion
        x = fuzzySystemSet.get("Risk=LowR").x
        risk = fuzz.defuzz(x, aggregated, 'centroid')
        s = "Application: " + application.appId + \
            " Has a risk of: " + str(round(risk, 2)) + "%\n"
        results.write(s)

        # risk_plot = fuzz.interp_membership(x, aggregated, risk)

        # for key in fuzzySystemSet:
        #     r = fuzzySystemSet.get(key)
        #     color = next(cycol)
        #     axs[6].plot(x, r.y, color, linewidth=0.5, linestyle='--', )
        # axs[6].fill_between(x, np.zeros_like(x), aggregated, facecolor='Orange', alpha=0.7)
        # axs[6].plot([risk, risk], [0, risk_plot], 'k', linewidth=1.5, alpha=0.9)
        # axs[6].set_title('Aggregated membership and result (line)')

    # Turn off top/right axes
    for ax in axs.flat:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()

    results.close()
    runGui(fig)


if __name__ == "__main__":
    main()
