from config.shared_mongo_client import SharedMongoClient
from config.db_fixer import DbFixer
from config.global_conf import Global

Global.configure_default_root_logging()
SharedMongoClient.initialize(should_use_localhost_db=False)
start_time = Global.convert_local_datetime_to_epoch("2018.06.29 09:00:00", timezone="kr")
end_time = Global.convert_local_datetime_to_epoch("2018.06.30 13:00:00", timezone="kr")

print(start_time)
print(end_time)
# DbFixer.add_missing_item_with_plain_copy_prev("coinone", "bch_orderbook", "gopax", "bch_orderbook",
#                                               start_time, end_time)
# DbFixer.fill_empty_orderbook_entry("coinone", "bch_orderbook", start_time, end_time)
