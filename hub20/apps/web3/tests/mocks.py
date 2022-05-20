import datetime
import random
from unittest.mock import MagicMock

import factory
from web3 import Web3
from web3.datastructures import AttributeDict

from hub20.apps.blockchain.factories import TEST_CHAIN_ID
from hub20.apps.blockchain.factories.providers import EthereumProvider

factory.Faker.add_provider(EthereumProvider)


def _make_web3_mock():
    w3 = Web3()
    w3.net = MagicMock()
    w3.net.version = str(TEST_CHAIN_ID)
    w3.net.peer_count = random.randint(1, 5)
    w3.eth = MagicMock()
    w3.eth.chain_id = TEST_CHAIN_ID
    w3.provider = MagicMock()
    w3.provider.endpoint_uri = "ipc://dev/null"

    w3.isConnected = lambda: True
    return w3


class Web3Model(AttributeDict):
    def __init__(self, **kw):
        super().__init__(kw)


class Web3DataMock(factory.Factory):
    class Meta:
        model = Web3Model


class TransactionMock(Web3DataMock):
    hash = factory.Faker("hex64")
    blockHash = factory.Faker("hex64")
    blockNumber = factory.Sequence(lambda n: n)
    from_address = factory.Faker("ethereum_address")
    to = factory.Faker("ethereum_address")
    transactionIndex = 0
    gas = 21000
    gasPrice = factory.fuzzy.FuzzyInteger(1e9, 1e14)

    class Meta:
        rename = {"from_address": "from"}


class TransactionDataMock(TransactionMock):
    input = "0x0"
    nonce = factory.Sequence(lambda n: n)
    value = 0
    chainId = hex(TEST_CHAIN_ID)


class TransactionReceiptDataMock(TransactionMock):
    contractAddress = None
    logs = []
    status = 1

    class Meta:
        rename = {
            "from_address": "from",
            "hash": "transactionHash",
            "gas": "gasUsed",
            "gasPrice": "effectiveGasPrice",
        }


class BlockMock(Web3DataMock):
    difficulty = (int(1e14),)
    hash = factory.Faker("hex64")
    logsBloom = "0x0"
    nonce = factory.Sequence(lambda n: hex(n))
    number = factory.Sequence(lambda n: n)

    parentHash = factory.Faker("hex64")
    receiptRoot = factory.Faker("hex64")
    sha3Uncles = factory.Faker("hex64")
    timestamp = factory.LazyFunction(lambda: int(datetime.datetime.now().timestamp()))
    transactions = factory.LazyAttribute(
        lambda obj: [obj.tx_hash for _ in range(obj.total_transactions)]
    )
    uncles = []

    class Params:
        total_transactions = 1
        tx_hash = factory.Faker("hex64")


class BlockWithTransactionDetailsMock(BlockMock):
    transactions = factory.LazyAttribute(
        lambda obj: [
            TransactionDataMock(blockNumber=obj.number, blockHash=obj.hash, transactionIndex=idx)
            for idx in range(obj.total_transactions)
        ]
    )


Web3Mock = _make_web3_mock()

__all__ = [
    "BlockMock",
    "BlockWithTransactionDetailsMock",
    "TransactionMock",
    "TransactionDataMock",
    "TransactionReceiptDataMock",
    "Web3Mock",
]
