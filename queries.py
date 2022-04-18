callsQuery = """
{
  ethereum(network: ethereum) {
    smartContractCalls(
      options: {limit: 100, offset: 10}
      caller: {is: "%s"}
    ) {


      smartContract {
        address {
          address
        }
      }

    }
  }
}

"""
txQuery = """
{
  ethereum(network: ethereum) {
    smartContractCalls(
      options: {asc: "callDepth"}
      txHash: {is: "%s"}
    ) {
      smartContract {
        address {
          address
          annotation
        }
        contractType
        protocolType
        currency {
          symbol
        }
      }
      smartContractMethod {
        name
        signatureHash
      }
      caller {
        address
        annotation
        smartContract {
          contractType
          currency {
            symbol
        }
      }
      }
      success
      amount
      gasValue
      callDepth
    }
  }
}
"""