def estimator(data):

  periodType = data['periodType']
  timeToElapse = data['timeToElapse']
  reportedCases = data['reportedCases']
  totalHospitalBeds = data['totalHospitalBeds']
  avgDailyIncomeInUSD = data['region']['avgDailyIncomeInUSD']
  avgDailyIncomePopulation = data['region']['avgDailyIncomePopulation']

  impactCases = reportedCases * 10
  severeCases = reportedCases * 50
  availableBeds = 0.35 * totalHospitalBeds


  
  def numberOfDays(periodType, timeToElapse):
    if periodType == 'days':
      days = timeToElapse
    elif periodType == 'weeks':
      days = timeToElapse * 7
    else:
      days = timeToElapse * 30
    return days

  
  def noOfCasesTimeToElapse(case):
    factor = numberOfDays(periodType, timeToElapse) // 3
    return case * (2 ** factor)

  def severeCasesByRequestedTime(case):
    return 0.15 * noOfCasesTimeToElapse(case)

  def hospitalBedsNeeded(case):
    return int(availableBeds - severeCasesByRequestedTime(case))

  def ICUCases(case):
    return int(noOfCasesTimeToElapse(case) * 0.05)

  def ventilatorCases(case):
    return int(noOfCasesTimeToElapse(case) * 0.02)

  def moneyLost(case):
    return int((noOfCasesTimeToElapse(case) * avgDailyIncomePopulation * avgDailyIncomeInUSD)/numberOfDays(periodType, timeToElapse))

  answer = {
    "data":data,
    "impact": {
      "currentlyInfected": impactCases,
      "infectionsByRequestedTime": noOfCasesTimeToElapse(impactCases),
      "severeCasesByRequestedTime": int(severeCasesByRequestedTime(impactCases)),
      "hospitalBedsByRequestedTime": hospitalBedsNeeded(impactCases),
      "casesForICUByRequestedTime": ICUCases(impactCases),
      "casesForVentilatorsByRequestedTime":ventilatorCases(impactCases),
      "dollarsInFlight": moneyLost(impactCases)
    },
    "severeImpact": {
      "currentlyInfected": severeCases,
      "infectionsByRequestedTime": noOfCasesTimeToElapse(severeCases),
      "severeCasesByRequestedTime": int(severeCasesByRequestedTime(severeCases)),
      "hospitalBedsByRequestedTime": hospitalBedsNeeded(severeCases),
      "casesForICUByRequestedTime": ICUCases(severeCases),
      "casesForVentilatorsByRequestedTime": ventilatorCases(severeCases),
      "dollarsInFlight": moneyLost(severeCases)
    }
  }

  return answer
