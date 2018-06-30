from trader.market.market import Market
from trader.market_manager.virtual_market_manager import VirtualMarketManager
from trader.risk_free_arb_bot import BaseArbBot
from config.global_conf import Global
from config.shared_mongo_client import SharedMongoClient
from collector.oppty_time_collector import OpptyRequestTimeCollector
from optimizer.initial_setting_optimizer import InitialSettingOptimizer

Global.configure_default_root_logging(should_log_to_file=False)
SharedMongoClient.initialize(should_use_localhost_db=True)

start_time = Global.convert_local_datetime_to_epoch("2018.06.30 09:00:00", timezone="kr")
end_time = Global.convert_local_datetime_to_epoch("2018.06.30 13:00:00", timezone="kr")

target_currency = "bch"
mm1 = VirtualMarketManager(Market.VIRTUAL_CO, 0.001, 5000000, 0.5, target_currency)
mm2 = VirtualMarketManager(Market.VIRTUAL_GP, 0.00075, 500000, 5, target_currency)
mm1_col = SharedMongoClient.get_target_col(Market.VIRTUAL_CO, target_currency)
mm2_col = SharedMongoClient.get_target_col(Market.VIRTUAL_GP, target_currency)
mm1_data_cursor, mm2_data_cursor = BaseArbBot.get_data_from_db(mm1_col, mm2_col, start_time, end_time)

result_dict = OpptyRequestTimeCollector(mm1, mm2, target_currency).run(mm1_data_cursor, mm2_data_cursor)

print(result_dict)

# get total duration time for each trade
total_dur_dict = OpptyRequestTimeCollector.get_total_duration_time(result_dict)
for key in total_dur_dict.keys():
    print("Total [%s] duration (hour): %.2f" % (key.upper(), (total_dur_dict[key] / 60 / 60)))

# Run ISO with start, end time under oppty
for trade_type in result_dict.keys():
    for time in result_dict[trade_type]:
        # Settings for ISO
        factor_settings = {
            "max_trading_coin": {
                "start": 0,
                "end": 0.1,
                "step_limit": 0.0001
            },
            "min_trading_coin": {
                "start": 0,
                "end": 0,
                "step_limit": 0
            },
            "new": {
                "threshold": {
                    "start": 0,
                    "end": 1000,
                    "step_limit": 1

                },
                "factor": {
                    "start": 1,
                    "end": 3,
                    "step_limit": 0.01
                }
            },
            "rev": {
                "threshold": {
                    "start": 0,
                    "end": 1000,
                    "step_limit": 1
                },
                "factor": {
                    "start": 1,
                    "end": 3,
                    "step_limit": 0.01
                }
            }
        }
        settings = {
            "target_currency": "bch",
            "mm1": {
                "market_tag": Market.VIRTUAL_CO,
                "fee_rate": 0.001,
                "krw_balance": 5000000,
                "coin_balance": 0.5
            },
            "mm2": {
                "market_tag": Market.VIRTUAL_GP,
                "fee_rate": 0.00075,
                "krw_balance": 500000,
                "coin_balance": 5

            },
            "division": 5,
            "depth": 5,
            "start_time": time[0],
            "end_time": time[1]
        }
        opt = InitialSettingOptimizer().run(settings, factor_settings)
        print("RESULT ===> [%s] start_time: %d, end_time: %d" % (trade_type.upper(), time[0], time[1]))
        print(opt)