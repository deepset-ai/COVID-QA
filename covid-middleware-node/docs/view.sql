DROP VIEW pnl_base;

CREATE VIEW pnl_base as
  (
SELECT SUM(value_signed), calender_year, organization_id, account_description, account_mapped, is_ebit, is_gross_profit, account_desc_sorting, account_mapped_sorting FROM pnl_w_sorting_v2

  GROUP BY calender_year, organization_id, account_description, account_mapped, is_ebit, is_gross_profit, account_desc_sorting, account_mapped_sorting
  )
;



UPDATE pnl_w_sorting_v2 p  SET organization_id = ( SELECT id FROM organizations WHERE p.company = organizations.name)
UPDATE pnl_deviations_v2 p SET organization_id = ( SELECT id FROM organizations WHERE p.company = organizations.name)


-- PNL
CREATE VIEW pnl_short as
  (
    SELECT SUM(value_signed) as value_signed, calender_year, organization_id, account_description, account_mapped, is_ebit, is_gross_profit, account_desc_sorting, account_mapped_sorting FROM pnl_base

  GROUP BY calender_year, organization_id, account_description, account_mapped, is_ebit, is_gross_profit, account_desc_sorting, account_mapped_sorting
  )
;


-- Balance Sheet
CREATE VIEW bs as(
SELECT financial_year, organization_id, account_description,
       account_mapped_1,
       account_mapped_2,
       account_mapped_3,
       account_mapped_1_sorting,
       account_mapped_2_sorting,
       account_mapped_3_sorting,

       SUM(value_signed) as value_signed FROM bs_base

  GROUP BY  1,2,3,4,5,6,7,8,9
    )
;

-- NWC
DROP view nwc_level_3
CREATE view nwc_level_3 as (
    SELECT bs.nwc_parent as parent,
    account_mapped_3,
       account_mapped_3_sorting as sorting,
       financial_year,
           organization_id,
       value_signed
    FROM bs
    WHERE nwc_level = 3
)


DROP view IF EXISTS  nwc_level_2;
CREATE VIEW nwc_level_2 as;
  SELECT
                 parent,
                  financial_year,
                    organization_id,
                  max(sorting) as sorting,
                  sum(value_signed) as value_signed
  ,COUNT(*)
             FROM nwc_level_3
         GROUP BY 1,2,3;

CREATE VIEW nwc_level_1 as
  SELECT
                  financial_year,
                    organization_id,
                  max(sorting) as sorting,
                  sum(value_signed) as value_signed
  ,COUNT(*)
             FROM nwc_level_3
         GROUP BY 1,2;



