import numpy as np
import skfuzzy as fuzz
from MFIS_Read_Functions import *
from gui import *


def main():
    # Main Variables
    applications = readApplicationsFile()
    fuzzifierSetsDict = readFuzzySetsFile('Files/InputVarSets.txt')
    fuzzySystemSet = readFuzzySetsFile('Files/Risks.txt')
    fuzzySystem = readRulesFile(version=2)

    # Variables for graphing
    basicGraphs = []
    applicationData = {}
    applicationRulesGraphData = {}
    applicationRiskGraphData = {}
    applicationRiskBasicGraphData = []

    # File to write to
    results = open('Files/NewResults.txt', 'w')

    # Generating data for graphs
    for key in fuzzifierSetsDict:
        # getting the membership function and  universe variables.
        fuzzySet = fuzzifierSetsDict.get(key)
        basicGraphs.append({
            "var": fuzzySet.var,
            "x": fuzzySet.x,
            "y": fuzzySet.y,
            "label": fuzzySet.label
        })

    for key in fuzzySystemSet:
        r = fuzzySystemSet.get(key)
        applicationRiskBasicGraphData.append([r.x, r.y])
        basicGraphs.append({
            "var": r.var,
            "x": r.x,
            "y": r.y,
            "label": r.label
        })

    for application in applications:
        # Fuzzyifcation
        age = application.data[0][1]
        IncomeLevel = application.data[1][1]
        Assets = application.data[2][1]
        Amount = application.data[3][1]
        Job = application.data[4][1]
        History = application.data[5][1]

        appIDWithoutLeadingZeros = application.appId.lstrip('0')

        applicationData[appIDWithoutLeadingZeros] = {
            "age": age,
            "IncomeLevel": IncomeLevel,
            "Assets": Assets,
            "Amount": Amount,
            "Job": Job,
            "History": History
        }

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
            arrayMax = [0]
            currentOP = rule.operator
            for antecedent in rule.antecedent:
                if "OP=AND" in antecedent:
                    currentOP = "AND"
                    continue
                elif "OP=OR" in antecedent:
                    currentOP = "OR"
                    continue
                else:
                    if "AND" in currentOP:
                        arrayMin = np.fmin(
                            arrayMin,  interp_memberhips.get(antecedent))
                    else:
                        arrayMax =  np.fmax(
                            arrayMax,  interp_memberhips.get(antecedent))
            # Now apply this by clipping the top off the corresponding output
            # membership function with `np.fmin`
            mainAnd = np.fmin(arrayMin, arrayMax) if arrayMax[0] > 0 else arrayMin
            mainOr = np.fmax(arrayMax, arrayMin) if arrayMin[0] < 1 else arrayMax
            rules.append(np.fmin(mainAnd if "AND" in rule.operator else mainOr, 
                         fuzzySystemSet.get(rule.consequent).y))

        graphData = []
        for rule in rules:
            for key in fuzzySystemSet:
                risk = fuzzySystemSet.get(key)
                graphData.append(
                    [risk.x, risk.y, np.zeros_like(risk.x), rule])
        applicationRulesGraphData[appIDWithoutLeadingZeros] = graphData

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

        risk_plot = fuzz.interp_membership(x, aggregated, risk)

        applicationRiskGraphData[appIDWithoutLeadingZeros] = [
            x, np.zeros_like(x), aggregated, risk, risk_plot]

    results.close()
    runGui(rulesGraphData=applicationRulesGraphData,
           riskGraphData=applicationRiskGraphData,
           riskGraphBasicData=applicationRiskBasicGraphData,
           applicationData=applicationData,
           basicGraphs=basicGraphs)


if __name__ == "__main__":
    main()
