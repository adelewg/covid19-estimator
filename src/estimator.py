def estimator(data):

  periodtype = data['periodType']
  timeToElase = data['timeToElapse']
  reportedCases = data['reportedCases']
  totalHospitalBeds = data['totalHospitalBeds']
  avgDailyIncome = data['region']['avgDailyIncomeInUSD']
  avgDailyIncomePopulation = data['region']['avgDailyIncomePopulation']

  impactCases = reportedCases * 10
  severeCases = reportedCases * 50
  available_beds = totalHospitalBeds * 0.35

  def numberOfDays(periodType, timeToElapse):
    if periodType == 'days':
      days = timeToElapse
    elif periodType == 'weeks':
      days = timeToElapse * 7
    else:
      days = timeToElapse * 30
    return days

  def noOfCasesTimeToElapse(case):
    factor = numberOfDays(periodType,timeToElapse)//3
    return case * (2 ** factor)

  def severeCasesByRequestedTime(case):
    return 0.15 * noOfCasesTimeToElapse(case)

  def hospitalBedsNeeded(case):
    return int(available_beds - severeCasesByRequestedTime(case))

  def ICUCases(case):
    return int(noOfCasesTimeToElapse(case) * 0.05)

  def VentilatorCases(case):
    return int(noOfCasesTimeToElapse(case) * 0.02)

  def moneyLost(case):
    return int((noOfCasesTimeToElapse * avgDailyIncomePopulation * avgDailyIncome)/numberOfDays(periodType, timeToElapse))



  answer = {
    'data': data,
    'impact': {
      'currentlyInfected': impactCases
      'infectionsByRequestedTime': noOfCasesTimeToElapse(impactCases)
      'severeCasesByRequestedTime': severeCasesByRequestedTime(impactCases)
      'hospitalBedsByRequestedTime': hospitalBedsNeeded(impactCases)
      'casesForICUByRequestedTime': ICUCases(impactCases)
      'casesForVentilatorsByRequestedTime': VentilatorCases(impactCases)
      'dollarInFlight': moneyLost(impactCases)
    }
    'severeImpact': {
      'currentlyInfected': severeCases
      'infectionsByRequestedTime': noOfCasesTimeToElapse(severeCases)
      'severeCasesByRequestedTime': severeCasesByRequestedTime(severeCases)
      'hospitalBedsByRequestedTime': hospitalBedsNeeded(severeCases)
      'casesForICUByRequestedTime': ICUCases(severeCases)
      'casesForVentilatorsByRequestedTime': VentilatorCases(severeCases)
      'dollarInFlight': moneyLost(severeCases)
      
    }
  }
  

  
  
 
  


  return answer
