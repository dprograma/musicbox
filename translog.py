log={'status': True, 'message': 'Verification successful', 'data': {'id': 2234965863, 'domain': 'test', 'status': 'success', 'reference': '4qz9coajzk', 'amount': 15000, 'message': None, 'gateway_response': 'Successful', 'paid_at': '2022-10-29T23:21:08.000Z', 'created_at': '2022-10-29T23:20:56.000Z', 'channel': 'card', 'currency': 'NGN', 'ip_address': '105.112.31.21', 'metadata': '', 'log': {'start_time': 1667085664, 'time_spent': 6, 'attempts': 1, 'errors': 0, 'success': True, 'mobile': False, 'input': [], 'history': [{'type': 'action', 'message': 'Attempted to pay with card', 'time': 3}, {'type': 'success', 'message': 'Successfully paid with card', 'time': 6}]}, 'fees': 225, 'fees_split': None, 'authorization': {'authorization_code': 'AUTH_nmy3rnw142', 'bin': '408408', 'last4': '4081', 'exp_month': '12', 'exp_year': '2030', 'channel': 'card', 'card_type': 'visa ', 'bank': 'TEST BANK', 'country_code': 'NG', 'brand': 'visa', 'reusable': True, 'signature': 'SIG_Y81P6LYJWsYFpypLzKTz', 'account_name': None}, 'customer': {'id': 99827621, 'first_name': None, 'last_name': None, 'email': 'ketuojoken@gmail.com', 'customer_code': 'CUS_1yi58e8g3m70tzq', 'phone': None, 'metadata': None, 'risk_action': 'default', 'international_format_phone': None}, 'plan': None, 'split': {}, 'order_id': None, 'paidAt': '2022-10-29T23:21:08.000Z', 'createdAt': '2022-10-29T23:20:56.000Z', 'requested_amount': 15000, 'pos_transaction_data': None, 'source': None, 'fees_breakdown': None, 'transaction_date': '2022-10-29T23:20:56.000Z', 'plan_object': {}, 'subaccount': {}}}

for k, v in log.items():
    print(f"{k}: {v}")
            # if dkey == 'log':
            #     for lkey, lval in log[k][dkey].items():
            #         print(f"{lkey}: {lval}")
            # elif dkey == 'authorization':
            #     for akey, aval in log[k][dkey].items():
            #         print(f"{akey}: {aval}")
            # elif dkey == 'customer':
            #     for ckey, cval in log[k][dkey].items():
            #         print(f"{ckey}: {cval}")
            # else:
            #     print(f"{dkey}: {dval}")
            # print(f"{dkey}: {dval}")
    
    