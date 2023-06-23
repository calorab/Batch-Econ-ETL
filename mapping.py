field_mapping = {
    'AV_FOREX_URL': {
        'data_set': 'Time Series FX (Weekly)',
        'fields': 'candles',
        'meta_data': True,
        'db_table': 'US_EU_FOREX',
        'name': 'US v EU (Forex)'
    },
    'AV_OIL_WTI_URL': {
        'data_set': 'data',
        'fields': 'dateValue',
        'meta_data': False,
        'db_table': 'OIL_WTI',
        'name': 'WTI OIL'
    },
    'AV_COMMODITIES_INDEX_URL': {
        'data_set': 'data',
        'fields': 'dateValue',
        'meta_data': False,
        'db_table': 'COMMODITIES_INDEX',
        'name': 'Commodities Index'
    },
    'AV_GDP_URL': {
        'data_set': 'data',
        'fields': 'dateValue',
        'meta_data': False,
        'db_table': 'US_GDP_Quarterly',
        'name': 'US GDP (Quarterly)'
    },
    'AV_TYIELD_URL': {
        'data_set': 'data',
        'fields': 'dateValue',
        'meta_data': False,
        'db_table': 'US_TREASURY_YIELD',
        'name': 'US Treasury Yield'
    }, 
    'AV_FUNDS_RATE_URL': {
        'data_set': 'data',
        'fields': 'dateValue',
        'meta_data': False,
        'db_table': 'US_FEDERAL_FUNDS_RATE',
        'name': 'US Federal Funds Rate'
    },
    'AV_CPI_URL': {
        'data_set': 'data',
        'fields': 'dateValue',
        'meta_data': False,
        'db_table': 'US_CPI',
        'name': 'US CPI'
    },
    'AV_INFLATION_URL': {
        'data_set': 'data',
        'fields': 'dateValue',
        'meta_data': False,
        'db_table': 'US_INFLATION',
        'name': 'Inflation ($)'
    },
    'AV_UNEMPLOYMENT_URL': {
        'data_set': 'data',
        'fields': 'dateValue',
        'meta_data': False,
        'db_table': 'US_UNEMPLOYMENT_RATE',
        'name': 'US Unemployment Rate'
    },
    'MD_DJI_INDICES_URL': {
        'data_set': 's',
        'fields': 'candles',
        'meta_data': False,
        'db_table': 'DOW_JONES_INDUSTRIAL_AVERAGE',
        'name': 'Dow Jones Industrial Average'
    },
    'MD_COMP_INDICES_URL': {
        'data_set': 's',
        'fields': 'candles',
        'meta_data': False,
        'db_table': 'NASDAQ_COMPOSITE_INDEX',
        'name': 'Nasdaq Composite'
    },
    'MD_NYA_INDICES_URL': {
        'data_set': 's',
        'fields': 'candles',
        'meta_data': False,
        'db_table': 'NYSE_COMPOSITE_INDEX',
        'name': 'NYSE Composite'
    },
    'MD_SPX_INDICES_URL': {
        'data_set': 's',
        'fields': 'candles',
        'meta_data': False,
        'db_table': 'SP_500_INDEX',
        'name': 'S&P 500'
    },
    'MD_XAU_INDICES_URL': {
        'data_set': 's',
        'fields': 'candles',
        'meta_data': False,
        'db_table': 'GOLD_SILVER_INDEX',
        'name': 'Gold & Silver Index'
    }
}