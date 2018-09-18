import logging
from config.global_conf import Global
from config.shared_mongo_client import SharedMongoClient
from trader.trade_manager.trade_streamer_v2 import TradeStreamerV2
from trader.market_manager.market_manager import MarketManager
from trader.market_manager.okcoin_market_manager import OkcoinMarketManager
from trader.market_manager.bithumb_market_manager import BithumbMarketManager


def main(mm1: MarketManager, mm2: MarketManager, target_currency: str):
    Global.configure_default_root_logging(should_log_to_file=True, log_level=logging.WARNING)
    SharedMongoClient.initialize(should_use_localhost_db=True)
    # run TradeStreamer
    TradeStreamerV2(mm1=mm1, mm2=mm2, target_currency=target_currency).run(use_ocat=False)


if __name__ == '__main__':
    main(BithumbMarketManager(), OkcoinMarketManager(), "xrp")
