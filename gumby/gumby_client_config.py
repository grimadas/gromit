from typing import Optional

from pydantic import BaseSettings

class DiscoveryConfig(BaseSettings):
    enabled: bool = False


class IPv8Config(BaseSettings):
    port: int = 8000
    statistics: bool = False
    bootstrap_override: Optional[str] = None
    discovery: DiscoveryConfig = DiscoveryConfig()


class TrustchainConfig(BaseSettings):
    ec_keypair_filename: str = "ec_multichain.pem"
    enabled: bool = False
    memory_db: bool = False


class DHTConfig(BaseSettings):
    enabled: bool = False


class MarketConfig(BaseSettings):
    enabled: bool = False
    memory_db: bool = False


class BasaltConfig(BaseSettings):
    enabled: bool = False


class GumbyConfig(BaseSettings):
    state_dir: str = ""
    ipv8: IPv8Config = IPv8Config()
    trustchain: TrustchainConfig = TrustchainConfig()
    dht: DHTConfig = DHTConfig()
    market: MarketConfig = MarketConfig()
    basalt: BasaltConfig = BasaltConfig()
