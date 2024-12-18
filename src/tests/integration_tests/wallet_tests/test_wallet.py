# import pytest

# from repositories.wallet import WalletRepo
# from models.wallet import CurrencyEnum


# @pytest.mark.parametrize(
#     "currency, id, exists, status_code",
#     [
#         ("USD", 1, True, 200),
#         ("RUB", 2, True, 200),
#         ("EUR", 3, True, 200),
#         ("JPY", 1, True, 400),
#         ("RUB", 7, False, 400),
#     ],
# )
# async def test_real_user_can_create_wallet_with_correct_currency(
#     currency, id, exists, status_code, client
# ):
#     data = {
#         "currency": currency,
#     }
#     repo = WalletRepo()
#     wallet = await repo.add_by_user_id(id, data)
#     if exists:
#         if currency in CurrencyEnum:
#             assert wallet
#             assert wallet["status_code"] == status_code
#         else:
#             assert wallet["status_code"] == 400
#     else:
#         assert wallet is None
#         assert wallet["status_code"] == status_code
