import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# from kombu.serialization import register

# from hub20.apps.blockchain.celery import web3_deserializer, web3_serializer

# BLOCK_CREATION_INTERVAL = 12
# NODE_HEALTH_CHECK_INTERVAL = 15
# RAIDEN_PAYMENT_CHECK_INTERVAL = 3


# register(
#     "web3",
#     web3_serializer,
#     web3_deserializer,
#     content_type="application/json",
#     content_encoding="utf-8",
# )


class Hub20CeleryConfig:
    name = "Hub20"

    broker_url = "memory" if "HUB20_TEST" in os.environ else settings.CELERY_BROKER_URL
    broker_use_ssl = "HUB20_BROKER_USE_SSL" in os.environ
    beat_schedule = {
        "clear-expired-sessions": {
            "task": "hub20.apps.core.tasks.clear_expired_sessions",
            "schedule": crontab(minute="*/30"),
            "expires": 60,
        },
        # "execute-transfers": {
        #     "task": "hub20.apps.core.tasks.execute_pending_transfers",
        #     "schedule": crontab(),
        #     "expires": 60,
        # },
        # "check-providers-connected": {
        #     "task": "hub20.apps.blockchain.tasks.check_providers_are_connected",
        #     "schedule": timedelta(seconds=NODE_HEALTH_CHECK_INTERVAL),
        #     "expires": NODE_HEALTH_CHECK_INTERVAL,
        # },
        # "check-providers-synced": {
        #     "task": "hub20.apps.blockchain.tasks.check_providers_are_synced",
        #     "schedule": timedelta(seconds=NODE_HEALTH_CHECK_INTERVAL),
        #     "expires": NODE_HEALTH_CHECK_INTERVAL,
        # },
        # "check-chain-reorgs": {
        #     "task": "hub20.apps.blockchain.tasks.check_chains_were_reorganized",
        #     "schedule": timedelta(seconds=10),
        #     "expires": NODE_HEALTH_CHECK_INTERVAL,
        # },
        # "reset-inactive-providers": {
        #     "task": "hub20.apps.blockchain.tasks.reset_inactive_providers",
        #     "schedule": crontab(minute="*/5"),
        #     "expires": NODE_HEALTH_CHECK_INTERVAL,
        # },
        # "refresh-priority-fee-cache": {
        #     "task": "hub20.apps.blockchain.tasks.refresh_max_priority_fee",
        #     "schedule": timedelta(seconds=30),
        #     "expires": BLOCK_CREATION_INTERVAL,
        # },
        # "refresh-wallet-balances": {
        #     "task": "hub20.apps.wallet.tasks.update_all_wallet_balances",
        #     "schedule": crontab(minute=0),
        #     "expires": BLOCK_CREATION_INTERVAL,
        # },
        # "index-token-transfer-events": {
        #     "task": "hub20.apps.ethereum_money.tasks.index_token_transfer_events",
        #     "schedule": timedelta(seconds=5 * BLOCK_CREATION_INTERVAL),
        #     "expires": 5 * NODE_HEALTH_CHECK_INTERVAL,
        # },
        # "sync-raiden-channels": {
        #     "task": "hub20.apps.raiden.tasks.sync_channels",
        #     "schedule": crontab(minute="*/5"),
        #     "expires": 5 * 60,
        # },
        # "sync-raiden-payments": {
        #     "task": "hub20.apps.raiden.tasks.sync_payments",
        #     "schedule": timedelta(seconds=RAIDEN_PAYMENT_CHECK_INTERVAL),
        #     "expires": RAIDEN_PAYMENT_CHECK_INTERVAL,
        # },
        # "process-mined-blocks": {
        #     "task": "hub20.apps.blockchain.tasks.process_mined_blocks",
        #     "schedule": timedelta(seconds=BLOCK_CREATION_INTERVAL),
        #     "expires": BLOCK_CREATION_INTERVAL,
        # },
        # "check-payments-in-open-routes": {
        #     "task": "hub20.apps.core.tasks.check_payments_in_open_routes",
        #     "schedule": timedelta(seconds=BLOCK_CREATION_INTERVAL),
        #     "expires": BLOCK_CREATION_INTERVAL,
        # },
    }
    result_backend = "django-db"
    task_always_eager = "HUB20_TEST" in os.environ
    task_eager_propagates = "HUB20_TEST" in os.environ
    task_ignore_result = True
    task_serializer = "web3"
    accept_content = ["web3", "json"]


app = Celery()
app.config_from_object(Hub20CeleryConfig)
app.autodiscover_tasks()
