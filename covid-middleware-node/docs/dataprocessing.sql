UPDATE bs_base SET nwc_level = 3, nwc_parent = 'Trade Working Capital' WHERE account_mapped_3 IN ('Trade Receivables','Inventories','Trade Payables')
UPDATE bs_base SET nwc_level = 3, nwc_parent = 'Other working Capital' WHERE account_mapped_3 IN ('Other Current Assets','Other Current Liabilities')


-- deviation
UPDATE public.deviations SET "row" = REPLACE(REPLACE(deviationtext, ' increased',''),' decreased','')


UPDATE bs_base p SET organization_id = ( SELECT id FROM organizations WHERE p.organization = organizations.name)
UPDATE pnl_base p SET organization_id = ( SELECT id FROM organizations WHERE p.company = organizations.name)


UPDATE pnl_base SET pnl_parent = 'Operating Income'
WHERE account_mapped IN ('Selling, General And Administration Expenses', 'Research & Development','Depreciation And Amortization','Other Operating Income/Expenses')

UPDATE pnl_base SET pnl_parent = 'Gross Profit'
WHERE account_mapped IN ('Selling, General And Administration Expenses', 'Research & Development','Depreciation And Amortization','Other Operating Income/Expenses')

UPDATE pnl_base SET pnl_parent = 'Gross Profit' WHERE is_gross_profit = 'WAHR';
