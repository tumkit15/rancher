from .common import random_str
from rancher import ApiError
import pytest


def test_dns_fqdn_unique(admin_mc):
    client = admin_mc.client
    provider_name = random_str()
    access = random_str()
    secret = random_str()
    globaldns_provider = \
        client.create_global_dns_provider(
                                         name=provider_name,
                                         route53ProviderConfig={
                                             'accessKey': access,
                                             'secretKey': secret,
                                             'rootDomain': "example.com"})

    fqdn = random_str() + ".example.com"
    globaldns_entry = \
        client.create_global_dns(fqdn=fqdn, providerId=provider_name)

    # Make sure creator can access both, provider and entry
    gdns_provider_id = "cattle-global-data:" + provider_name
    gdns_provider = client.by_id_global_dns_provider(gdns_provider_id)
    assert gdns_provider is not None

    gdns_entry_id = "cattle-global-data:" + globaldns_entry.name
    gdns = client.by_id_global_dns(gdns_entry_id)
    assert gdns is not None

    with pytest.raises(ApiError) as e:
        client.create_global_dns(fqdn=fqdn, providerId=provider_name)
        assert e.value.error.status == 422

    client.delete(globaldns_entry)
    client.delete(globaldns_provider)


def test_dns_provider_deletion(admin_mc):
    client = admin_mc.client
    provider_name = random_str()
    access = random_str()
    secret = random_str()
    globaldns_provider = \
        client.create_global_dns_provider(
                                         name=provider_name,
                                         route53ProviderConfig={
                                             'accessKey': access,
                                             'secretKey': secret,
                                             'rootDomain': "example.com"})

    fqdn = random_str() + ".example.com"
    provider_id = "cattle-global-data:"+provider_name
    globaldns_entry = \
        client.create_global_dns(fqdn=fqdn, providerId=provider_id)

    with pytest.raises(ApiError) as e:
        client.delete(globaldns_provider)
        assert e.value.error.status == 403

    client.delete(globaldns_entry)
    client.delete(globaldns_provider)
