from typing import Optional

from django import forms
from django.contrib import admin
from django.db.models import Q
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from . import models
from .typing import EthereumAccount_T
from .validators import web3_url_validator


class ConnectedChainListFilter(admin.SimpleListFilter):
    title = _("connected chain")

    parameter_name = "connected"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Yes"),
            ("no", "No"),
        )

    def queryset(self, request, queryset):
        selection = self.value()

        if selection is None:
            return queryset

        connected_q = Q(providers__is_active=True)

        filter_type = queryset.filter if selection == "yes" else queryset.exclude
        return filter_type(connected_q)


class TestChainListFilter(admin.SimpleListFilter):
    title = _("testnets")

    parameter_name = "testnet"

    def lookups(self, request, model_admin):
        return (
            models.Chain.objects.filter(testnets__isnull=False)
            .distinct()
            .values_list("id", "name")
        )

    def queryset(self, request, queryset):
        selection = self.value()

        if selection is None:
            return queryset

        return models.Chain.objects.filter(info__testing_for=selection)


class RollupListFilter(admin.SimpleListFilter):
    title = _("rollups")

    parameter_name = "rollup"

    def lookups(self, request, model_admin):
        return (
            models.Chain.objects.filter(rollups__isnull=False).distinct().values_list("id", "name")
        )

    def queryset(self, request, queryset):
        selection = self.value()

        if selection is None:
            return queryset

        return models.Chain.objects.filter(info__rollup_for=selection)


class SidechainListFilter(admin.SimpleListFilter):
    title = _("sidechains")

    parameter_name = "sidechain"

    def lookups(self, request, model_admin):
        return (
            models.Chain.objects.filter(sidechains__isnull=False)
            .distinct()
            .values_list("id", "name")
        )

    def queryset(self, request, queryset):
        selection = self.value()

        if selection is None:
            return queryset

        return models.Chain.objects.filter(info__sidechain_for=selection)


class Web3URLField(forms.URLField):
    default_validators = [web3_url_validator]


Web3ProviderForm = forms.modelform_factory(
    model=models.Web3Provider,
    fields=["chain", "url", "max_block_scan_range", "is_active", "connected", "synced"],
    field_classes={"url": Web3URLField},
)


class ChainMetadataInline(admin.StackedInline):
    model = models.ChainMetadata
    autocomplete_fields = ("testing_for", "rollup_for", "sidechain_for")
    fields = ("short_name", "testing_for", "rollup_for", "sidechain_for")
    fk_name = "chain"


@admin.register(models.Chain)
class ChainAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "id", "provider")
    list_filter = (
        ConnectedChainListFilter,
        TestChainListFilter,
        RollupListFilter,
        SidechainListFilter,
    )
    readonly_fields = ("highest_block",)
    search_fields = ("name", "id")

    inlines = [ChainMetadataInline]


@admin.register(models.Web3Provider)
class Web3ProviderAdmin(admin.ModelAdmin):
    form = Web3ProviderForm

    list_display = (
        "hostname",
        "chain",
        "is_active",
        "connected",
        "synced",
    )
    list_filter = ("is_active", "connected", "synced")
    readonly_fields = ("connected", "synced")
    search_fields = ("url", "chain__name")


@admin.register(models.Explorer)
class BlockchainExplorerAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "standard")
    list_filter = ("standard",)
    search_fields = ("url", "chain__name")


@admin.register(models.BaseEthereumAccount)
class EthereumAccountAdmin(admin.ModelAdmin):
    list_display = ("address",)

    def has_add_permission(
        self, request: HttpRequest, obj: Optional[EthereumAccount_T] = None
    ) -> bool:
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: Optional[EthereumAccount_T] = None
    ) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: Optional[EthereumAccount_T] = None
    ) -> bool:
        return False
