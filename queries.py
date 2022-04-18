senderQuery = """
{
 ethereum(network: ethereum) {
    transactions(txHash: {is: "%s"}) {
      sender {
        address
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