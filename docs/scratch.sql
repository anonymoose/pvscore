


select * from cms_site;

delete from crm_campaign where company_id = 6;
delete from crm_company where enterprise_id = 4;
delete from crm_enterprise where enterprise_id = 4;


delete from cms_template where template_id = 43;


alter table crm_customer_order add column note text;
alter table crm_customer_order add column shipping_note varchar(50);

alter table crm_campaign add column comm_packing_slip_id integer;
alter table crm_campaign add foreign key (comm_packing_slip_id) references crm_communication;

drop table cms_page_content;

alter table cms_content drop column site_id;
alter table cms_content add column page_id integer;
alter table cms_content add foreign key (page_id) references cms_page;

alter table crm_customer_order add column handling_note varchar(50);
alter table crm_customer_order add column handling_total float default 0.0;
alter table crm_customer_order add column payment_applied float default 0.0;

alter table crm_customer_order drop column payment_applied;

alter table crm_customer add column current_balance float default 0.0;

alter table crm_customer drop column current_balance;



select * from cms_content;

select * from core_user;

delete from core_user where enterprise_id <> 5;
delete from crm_company where enterprise <> 5;
delete from crm_enterprise where enterprise_id <> 5;
delete from cms_template where enterprise_id <> 5;

select * from cms_site;
select * from crm_order_item;

select * from crm_company;
select * from crm_customer_order;

-- individual orders for a day.
select sum(oi.unit_cost*oi.quantity) as cost,
       sum(oi.unit_price*oi.quantity) as revenue,
       sum((oi.unit_price*oi.quantity)-(oi.unit_cost*oi.quantity)) as profit,
       sum(o.shipping_total) as shipping,
       sum(coalesce(p.handling_price, 0)) as handling
from
crm_customer_order o, crm_customer cust,
crm_order_item oi, crm_campaign cmp,
crm_company co, core_status cs, core_status_event cse, crm_product p
where
o.customer_id = cust.customer_id and
o.order_id = oi.order_id and
o.campaign_id = cmp.campaign_id and
oi.product_id = p.product_id and
cmp.company_id = co.company_id and
co.enterprise_id = 3 and
o.delete_dt is null and
oi.delete_dt is null and
o.status_id = cs.status_id and
cs.event_id = cse.event_id and
o.create_dt between '2011-02-10' and '2011-02-22';

select * from core_status_event;


-- Daily sales total by Campaign
select o.create_dt,
cmp.name As campaign,
sum(1) as orders,
sum(oi.unit_price*oi.quantity) as revenue,
sum(oi.unit_cost*oi.quantity) as cost,
sum((oi.unit_price*oi.quantity)-(oi.unit_cost*oi.quantity)) as profit
from
crm_customer_order o, crm_customer cust, crm_order_item oi, crm_campaign cmp, crm_product p, crm_company co
where
o.customer_id = cust.customer_id and
o.order_id = oi.order_id and
o.campaign_id = cmp.campaign_id and
cmp.company_id = co.company_id and
co.enterprise_id = 3 and
oi.product_id = p.product_id and
o.delete_dt is null and
oi.delete_dt is null
group by o.create_dt, cmp.name
order by o.create_dt desc, cmp.name;

-- product.get_orders_report
select o.order_id, o.create_dt, cust.email, cmp.name as campaign,
oi.quantity,
oi.unit_price*oi.quantity revenue,
oi.unit_cost*oi.quantity as cost,
(oi.unit_price*oi.quantity)-(oi.unit_cost*oi.quantity) as profit
from
crm_customer_order o, crm_customer cust, crm_order_item oi, crm_campaign cmp, crm_product p
where
o.customer_id = cust.customer_id and
o.order_id = oi.order_id and
o.campaign_id = cmp.campaign_id and
cmp.company_id = 5
and oi.product_id = p.product_id
and p.product_id= 1449
and o.delete_dt is null
and oi.delete_dt is null
order by o.create_dt desc;


-- P/L report


alter table crm_product add column status_id integer;
alter table crm_product add foreign key (status_id) references core_status;


select * from core_status_event;

alter table crm_customer_order add column shipping_total float default 0.0;
alter table crm_product add column status_id integer;
alter table crm_product add foreign key (status_id) references core_status;
alter table crm_report add column override varchar(200);

alter table crm_product add column web_visible boolean default true;

delete from wm_prediction;

select * from wm_exchange;

insert into wm_exchange (symbol, name, type)
values ('UNK', '', 'STOCK');


\d wm_prediction;


select * from crm_customer;

select * from crm_product where sku = 'SUP-1001';

update crm_product set name = 'Folapro #60' where product_id = 1519;



delete from crm_product_pricing where product_id in (1449,1453,1454,1455,1456,1475,1476,1480,1482,1485,1495,1497,1498,
1499,1507,1512,1513,1521,1528,1535,1537,1543,1552,1574,1575,1577,
1588,1660,1596,1597,1459,1601,1602,1589,1609,1613,1615,1617,1616,
1611,1629,1634,1640,1648,1661,1651,1654,1554,1582,1527,1529,1585,
1586);
delete from crm_order_item where product_id in (1449,1453,1454,1455,1456,1475,1476,1480,1482,1485,1495,1497,1498,
1499,1507,1512,1513,1521,1528,1535,1537,1543,1552,1574,1575,1577,
1588,1660,1596,1597,1459,1601,1602,1589,1609,1613,1615,1617,1616,
1611,1629,1634,1640,1648,1661,1651,1654,1554,1582,1527,1529,1585,
1586);
delete from crm_product_category_join where product_id in (1449,1453,1454,1455,1456,1475,1476,1480,1482,1485,1495,1497,1498,
1499,1507,1512,1513,1521,1528,1535,1537,1543,1552,1574,1575,1577,
1588,1660,1596,1597,1459,1601,1602,1589,1609,1613,1615,1617,1616,
1611,1629,1634,1640,1648,1661,1651,1654,1554,1582,1527,1529,1585,
1586);
delete from crm_product where product_id in (1449,1453,1454,1455,1456,1475,1476,1480,1482,1485,1495,1497,1498,
1499,1507,1512,1513,1521,1528,1535,1537,1543,1552,1574,1575,1577,
1588,1660,1596,1597,1459,1601,1602,1589,1609,1613,1615,1617,1616,
1611,1629,1634,1640,1648,1661,1651,1654,1554,1582,1527,1529,1585,
1586);

select web_visible from crm_product;

select * from crm_campaign;



select * from core_status_event where short_name in ('PAYMENT_APPLIED', 'CREATED') and event_type = 'CustomerOrder';

insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system, milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('CustomerOrder', 'PAYMENT_APPLIED', 'Payment Applied', false, false, true, false, false, false, false, true, false);

insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system, milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('Customer', 'NOTE', 'Note', false, false, true, false, true, false, false, false, false);

insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system, milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('Customer', 'DELETED', 'Deleted', false, false, true, false, false, false, false, false, false);

insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system, milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('OrderItem', 'PROVISIONED', 'Provisioned', false, false, true, false, false, false, false, false, false);

insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system, milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('CustomerOrder', 'DISCOUNT_APPLIED', 'Discount Applied', false, false, true, false, false, false, false, true, false);


select * from crm_journal;


delete from crm_product_return;
delete from crm_journal;
delete from core_status where event_id = 20;
delete from core_status where fk_type = 'OrderItem' and fk_id in (select order_item_id from crm_order_item where order_id in (select order_id from crm_customer_order where customer_id = 38));
delete from core_status where fk_type = 'Order' and fk_id in (select order_id from crm_customer_order where customer_id = 38);
delete from crm_order_item where order_id in (select order_id from crm_customer_order where customer_id = 38);
delete from crm_customer_order where customer_id = 38;


select * from crm_journal;

select name, inventory from crm_product where product_id in (1592, 1463, 1477);

alter table crm_billing drop column customer_id;

alter table crm_customer add column billing_id integer;
alter table crm_customer add foreign key (billing_id) references crm_billing;

alter table crm_campaign add column comm_forgot_password_id integer;


select max(order_id) from crm_customer_order;



select * from crm_company;

delete from wm_prediction;

select * from crm_company where name = 'Wealthmakers';

select * from wm_portfolio;

select * from wm_stock_symbol where symbol = 'SPLS';


select * from crm_campaign where campaign_id = 8;

select * from crm_communication where comm_id = 3;


select * from wm_exchange;



select distinct(ss.* )
from wm_portfolio wmp, wm_stock_symbol ss
where wmp.symbol_id = ss.symbol_id;




alter table wm_stock_symbol add column div_yield Float default 0.0;
alter table wm_stock_symbol add column ptb Float default 0.0;
alter table wm_stock_symbol add column dps Float default 0.0;
alter table wm_stock_symbol add column pts Float default 0.0;
alter table wm_stock_symbol add column eps Float default 0.0;
alter table wm_stock_symbol add column shares  Integer default 0.0;
alter table wm_stock_symbol add column yieldd Float default 0.0;
alter table wm_stock_symbol add column pe Float default 0.0;
alter table wm_stock_symbol add column nta Float default 0.0;
alter table wm_stock_symbol add column dividend Float default 0.0;
alter table wm_stock_symbol add column ebitda Integer default 0;
alter table wm_stock_symbol add column description varchar(100);


alter table wm_stock_symbol drop column shares;
alter table wm_stock_symbol add column shares int default 0;
alter table wm_stock_symbol alter column ebitda type float;
alter table wm_stock_symbol drop column market_cap;
alter table wm_stock_symbol add column market_cap int default 0;

alter table wm_stock_symbol alter column market_cap type int;

alter table wm_stock_symbol add column ma1 float default 0.0;
alter table wm_stock_symbol add column yearlow float default 0.0;
alter table wm_stock_symbol add column ma2 float default 0.0;
alter table wm_stock_symbol add column ma5 float default 0.0;
alter table wm_stock_symbol add column avgmonthvolume float default 0.0;
alter table wm_stock_symbol add column yearchange float default 0.0;
alter table wm_stock_symbol add column monthlow float default 0.0;
alter table wm_stock_symbol add column monthchange float default 0.0;
alter table wm_stock_symbol add column mtm14 float default 0.0;
alter table wm_stock_symbol add column weekhigh float default 0.0;
alter table wm_stock_symbol add column yearhigh float default 0.0;
alter table wm_stock_symbol add column weeklow float default 0.0;
alter table wm_stock_symbol add column ma100 float default 0.0;
alter table wm_stock_symbol add column ma200 float default 0.0;
alter table wm_stock_symbol add column threemonthchange float default 0.0;
alter table wm_stock_symbol add column avgmonthchange float default 0.0;

alter table wm_stock_symbol add column ptc float default 0.0;
alter table wm_stock_symbol add column volumechange float default 0.0;
alter table wm_stock_symbol add column avgyearvolumne float default 0.0;
alter table wm_stock_symbol add column ma20 float default 0.0;
alter table wm_stock_symbol add column sixmonthchange float default 0.0;
alter table wm_stock_symbol add column sar float default 0.0;
alter table wm_stock_symbol add column change float default 0.0;
alter table wm_stock_symbol add column volatility float default 0.0;
alter table wm_stock_symbol add column avgweekchange float default 0.0;
alter table wm_stock_symbol add column rsi14 float default 0.0;
alter table wm_stock_symbol add column wpr14 float default 0.0;
alter table wm_stock_symbol add column sto9 float default 0.0;
alter table wm_stock_symbol add column mareturn float default 0.0;
alter table wm_stock_symbol add column liquidity float default 0.0;
alter table wm_stock_symbol add column description float default 0.0;
alter table wm_stock_symbol add column ma50 float default 0.0;
alter table wm_stock_symbol add column avgyearchange float default 0.0;
alter table wm_stock_symbol add column weekchange float default 0.0;
alter table wm_stock_symbol add column avgweekvolume float default 0.0;
alter table wm_stock_symbol add column monthhigh float default 0.0;
alter table wm_stock_symbol add column mapercent float default 0.0;
alter table wm_stock_symbol add column roc14 float default 0.0;
alter table wm_stock_symbol add column previous float default 0.0;

select market_cap, shares from wm_stock_symbol where symbol = 'AA.P';

select * from wm_exchange;


alter table wm_stock_symbol add column today_high float default 0.0;
alter table wm_stock_symbol add column today_low float default 0.0;
alter table wm_stock_symbol add column today_last float default 0.0;

alter table wm_stock_symbol add column today_open float default 0.0;
alter table wm_stock_symbol add column today_change varchar(10);

alter table wm_stock_symbol drop column today_vol;
alter table wm_stock_symbol add column today_vol varchar(30);


alter table wm_prediction add column price float default 0.0;



select count(0), source from wm_prediction group by source;



create index wm_pred_symbol_id on wm_prediction (symbol_id);
create index wm_pred_source on wm_prediction (source);
create index wm_pred_create_dt on wm_prediction (create_dt);
create index wm_eodquote_exchange_id on wm_eod_quote (exchange_id);
create index wm_eodquote_symbol_id on wm_eod_quote (symbol_id);
create index wm_eodquote_create_dt on wm_eod_quote (create_dt);


select distinct(create_dt) from wm_prediction;

select * from crm_enterprise;


delete from crm_campaign where company_id in (select company_id from crm_company where enterprise_id = 2);
delete from crm_company where enterprise_id = 2;
delete from crm_customer

alter table wm_stock_symbol drop column wm_update_dt;
alter table wm_stock_symbol add column today_update_dt date;

select * from crm_product where product_id = 1008;


select * from crm_enterprise;

select * from core_user where enterprise_id = 1;



alter table crm_order_item drop column unit_discount;
alter table crm_order_item add column unit_discount_price float default 0.0;
alter table crm_order_item add column unit_retail_price float default 0.0;


        return DB::getLink('main')->loadList("select g.group_id, g.name, g.is_preferred, g.keywords
                                              from ly.group g, ly.symbol s
                                              where g.group_id = s.group_id
                                              and s.symbol_id = $symbol_id");



select sum(amount) from crm_journal where order_id = 91;






select cust.customer_id,
       --  o.create_dt, cust.email,
  o.order_id,
  sum(oi.unit_cost*oi.quantity) as "cost",

  (sum(oi.unit_price*oi.quantity)) as "item_revenue",

  (coalesce(o.shipping_total, 0)) as "shipping_revenue",

  (coalesce(o.handling_total, 0)) as "handling_revenue",

  (sum(oi.unit_price*oi.quantity)+coalesce(o.shipping_total,0)+coalesce(o.handling_total,0)) as "total_revenue",

  (sum((oi.unit_price-(oi.unit_price-oi.unit_discount_price))*oi.quantity)) as "discount",

  coalesce(  (select sum(coalesce(amount,0)) from crm_journal
     where order_id = o.order_id
    and type in ('CreditIncrease', 'Refund')), 0) as "refunds",

  coalesce(  (select sum(coalesce(amount,0)) from crm_journal
     where order_id = o.order_id
    and type in ('FullPayment', 'PartialPayment')), 0) as "payments",

  coalesce(  (sum(oi.unit_price*oi.quantity)+coalesce(o.shipping_total,0)+coalesce(o.handling_total,0))
    -coalesce((select sum(coalesce(amount,0)) from crm_journal
              where order_id = o.order_id
              and type in ('FullPayment', 'PartialPayment')), 0), 0) as "due",

  cse.display_name,
  CASE WHEN o.user_created is null THEN 'WEB'
            ELSE 'OFFICE'
       END as source
from
  crm_customer_order o, crm_customer cust,
  crm_order_item oi, crm_campaign cmp,
  crm_company co, core_status cs, core_status_event cse
where
o.customer_id = cust.customer_id and
o.order_id = oi.order_id and
o.campaign_id = cmp.campaign_id and
cmp.company_id = co.company_id and
co.enterprise_id = 3 and
o.delete_dt is null and
oi.delete_dt is null and
o.status_id = cs.status_id and
cs.event_id = cse.event_id
group by o.create_dt, cust.email,
  o.order_id, cse.display_name, cust.customer_id, o.user_created, o.shipping_total, o.handling_total
order by o.order_id desc
;


select * from crm_journal
     where order_id = 92
    and type in ('CreditIncrease', 'Refund');

alter table crm_journal add column method varchar(15) default 'Credit Card';


alter table crm_company add column default_campaign_id integer;
alter table crm_company add foreign key (default_campaign_id) references crm_campaign;

select * from crm_campaign;

update crm_company set default_campaign_id = 6 where company_id = 5;

select default_campaign_id, name from crm_company where company_id = 5;

alter table crm_order_item add column unit_discount_price float default 0.0;
alter table crm_order_item add column unit_retail_price float default 0.0;

select unit_discount_price, unit_retail_price, unit_price, create_dt from crm_order_item where order_id = 98;


select * from crm_product_category where category_id = 10;




alter table crm_report add column show_start_dt boolean default false;
alter table crm_report add column show_end_dt boolean default false;
alter table crm_report add column show_campaign_id boolean default false;
alter table crm_report add column show_company_id boolean default false;
alter table crm_report add column show_user_id boolean default false;
alter table crm_report add column show_product_id boolean default false;
alter table crm_report add column p0_name varchar(50);
alter table crm_report add column p1_name varchar(51);
alter table crm_report add column p2_name varchar(52);


select * from pvs_listing;


insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system,
milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('Listing', 'OPEN', 'OPEN', false, false, true,
true, false, false, false, true, false);

insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system,
milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('Listing', 'OPEN', 'OPEN', false, false, true,
true, false, false, false, true, false);


select * from wm_prediction where prediction_id = 1924;

alter table pvs_listing add column category varchar(50);


select * from crm_product where company_id = 6;

select * from crm_company;

select name, path, file from cms_template where name = 'ams';

select * from cms_page where site_id = 6 order by name;


\d wm_prediction;

select prediction_id, target from wm_prediction where create_dt = '2011-03-30' and target is not null;

select source, count(0) from wm_prediction group by source;


select count(0) from wm_stock_symbol where summary is not null;

select sso.* from wm_stock_symbol sso where sso.symbol_id in (
    select symbol_id from (
        select ss.symbol_id, count(eq.quote_id) cnt
        from wm_exchange ex inner join wm_stock_symbol ss on (ex.exchange_id = ss.exchange_id)
             left outer join wm_eod_quote eq on ss.symbol_id = eq.symbol_id
        where ex.symbol in ('NASDAQ', 'AMEX', 'NYSE', 'OTCBB')
        group by ex.symbol, ss.symbol_id, ss.name, ss.symbol
    ) i where i.cnt = 0)
limit 100;

select count(0) from wm_eod_quote where symbol_id = 44343;

create index wm_ss_ex_id on wm_stock_symbol (exchange_id);
create index wm_ex_symbol on wm_exchange (symbol);
create index wm_eq_symid on wm_eod_quote (symbol_id);


vacuum full verbose wm_stock_symbol;
vacuum full verbose wm_exchange;
vacuum full verbose wm_eod_quote;

select * from wm_eod_quote where symbol_id = 1074;




select i.symbol, count(0) from (
        select ex.symbol, ss.name, ss.symbol_id, count(eq.quote_id) cnt
        from wm_exchange ex inner join wm_stock_symbol ss on (ex.exchange_id = ss.exchange_id)
             left outer join wm_eod_quote eq on ss.symbol_id = eq.symbol_id
        where ex.symbol in ('NASDAQ', 'AMEX', 'NYSE', 'OTCBB')
        group by ex.symbol, ss.symbol_id, ss.name, ss.symbol
) i where i.cnt < 20
group by i.symbol;



select prediction_disposition, lookback, lookon, numerator, denominator, expectation, period from wm_prediction where prediction_id = 8479;

\d wm_prediction


alter table wm_prediction add column avg_volatility float default 0.0;
alter table wm_prediction add column maturity_dt date;

select distinct avgmonthvolume from wm_stock_symbol;


delete from wm_prediction;

select * from wm_prediction where maturity_dt is not null;


delete from wm_prediction_result;


select * from wm_prediction_result;

select * from crm_billing_history;

select cancel_dt from crm_customer_order where order_id = 59;

update crm_customer_order set cancel_dt = null where order_id = 59;


alter table crm_campaign add column comm_post_cancel_id integer;
alter table crm_campaign add foreign key (comm_post_cancel_id) references crm_communication;

alter table cms_site add column domain_alias0 varchar(50);
alter table cms_site add column domain_alias1 varchar(50);
alter table cms_site add column domain_alias2 varchar(50);


select * from wm_stock_symbol where symbol_id = 24124;

delete from wm_portfolio where symbol_id in (24124,19529);


select count(0) from wm_eod_quote where symbol_id = 22139;

select * from wm_stock_symbol where symbol = 'WWWW';

select * from crm_company where company_id = 5;


alter table core_user drop column allow_cms;
alter table core_user drop column allow_report_edit;
alter table core_user drop column allow_superadmin;
alter table core_user add column priv_id integer;
alter table core_user add foreign key (priv_id) references core_user_priv;


select priv_id from core_user where username = 'kenneth.bedwell@gmail.com';

select view_customer from core_user_priv;


alter table crm_product drop column inventory;

select * from crm_product_inventory_journal where product_id = 1452;


alter table crm_vendor add column delete_dt date;
alter table crm_vendor add column create_dt date default now();

delete from crm_purchase_order_item;

select * from crm_purchase_order_item;


insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system, milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('PurchaseOrder', 'CREATED', 'Created', false, false, true, false, false, false, false, true, false);

insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system, milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('PurchaseOrder', 'MODIFIED', 'Modified', false, false, true, false, false, false, false, true, false);

insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system, milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('PurchaseOrder', 'COMPLETED', 'Completed', false, true, true, false, false, false, false, true, false);


alter table crm_purchase_order_item drop column complete_dt;
alter table crm_purchase_order_item drop column cancel_dt;
alter table crm_purchase_order add column complete_dt date;
alter table crm_purchase_order add column cancel_dt date;

alter table crm_purchase_order_item add column complete_dt date;
alter table crm_purchase_order_item add column cancel_dt date;


alter table core_user_priv add column send_customer_emails boolean default true;
alter table core_user_priv add column modify_customer_order boolean default true;


select * from crm_journal where type = 'Discount';

delete from crm_journal where type = 'Discount';


select ss.symbol, p.source,
date_part('days', p.maturity_dt-now()) maturity_days,
ss.today_last,p.price, p.target,
round(cast (p.target-p.price as numeric), 2) price_diff,
round(cast (p.avg_volatility as numeric), 2) as avg_volatility,
round(cast ((p.target-p.price)/p.avg_volatility as numeric), 2) days_required_to_cover,
round(cast (date_part('days', p.maturity_dt-now())-((p.target-p.price)/p.avg_volatility) as numeric), 2) days_left_over_after_cover
from wm_prediction p, wm_stock_symbol ss
where p.target is not null
and p.symbol_id = ss.symbol_id
and p.maturity_dt is not null
and p.prediction_direction = 'UP'
and p.source not in ('SqueezeTrigger', 'Friction Factor')
and p.maturity_dt > now() + interval '5 days'
and p.maturity_dt < now() + interval '15 days'
and ss.today_last < p.target
and p.target > p.price
and p.target > ss.today_last
and (p.target-p.price)/p.avg_volatility <date_part('days', p.maturity_dt-now())
--order by p.maturity_dt - now()
order by date_part('days', p.maturity_dt-now())-(p.target-p.price)/p.avg_volatility desc
limit 30;


select ss.symbol, p.prediction_direction,
case when p.source = 'Earnings' then p.source || ' ' || p.prediction_disposition
else p.source
end,
p.maturity_dt,
date_part('days', p.maturity_dt-now()) maturity_days,
ss.today_last,p.price, p.target,
round(cast (@(p.target-p.price)/p.price as numeric),2) as gap,
round(cast (@(p.target-p.price) as numeric), 2) as price_diff,
round(cast (p.avg_volatility as numeric), 2) as avg_volatility,
round(cast (@(p.target-p.price)/p.avg_volatility as numeric), 2) days_required_to_cover,
round(cast (date_part('days', p.maturity_dt-now())-((@(p.target-p.price))/p.avg_volatility) as numeric), 2) days_left_over_after_cover
from wm_prediction p, wm_stock_symbol ss
where
p.symbol_id = ss.symbol_id and
p.target is not null and
p.maturity_dt is not null and
p.source not in ('SqueezeTrigger', 'Friction Factor') and
p.maturity_dt > now() and
((p.prediction_direction = 'UP' and ss.today_last < p.target and p.target > p.price)
                         or (p.prediction_direction = 'DOWN' and ss.today_last > p.target and p.target < p.price)) and
--(@(p.target-p.price))/p.avg_volatility <date_part('days', p.maturity_dt-now()) and
--source in ('Group Correlation') and
p.target > 0 and
p.avg_volatility > 0 and
1=1
--order by date_part('days', p.maturity_dt-now())-(p.target-p.price)/p.avg_volatility desc
order by @(p.target-p.price)/p.price desc
--order by source desc
limit 50;

select source, count(0) from wm_prediction where valuation is not null and valuation > 0 group by source;

select symbol_id, prediction_direction from wm_prediction where prediction_id = 13695;

select yearhigh, yearlow, today_update_dt from wm_stock_symbol where symbol_id = 26917;
\d wm_stock_symbol;

select max(high) from wm_eod_quote where symbol_id = 26917;

delete from wm_prediction where create_dt = '2011-05-05';

select title, maturity_dt from wm_prediction where title like 'MDTH%' and create_dt = '2011-05-05';

select source, count(0) from wm_prediction where create_dt = '2011-05-05' group by source;

select source, count(0) from wm_prediction where maturity_dt > now() group by source;


select source, maturity_dt, title from wm_prediction where source = 'PatternScan' and create_dt = '2011-05-05' limit 10;


select source, count(0) from wm_prediction group by source;


select source, count(0) from wm_prediction where maturity_dt > now() group by source;


\d wm_stock_symbol;


\d wm_exchange;

select symbol, name, exchange_id from wm_exchange;

select symbol from wm_exchange where active = true;

copy foo from '/Users/kbedwell/dev/pydev/wm/stock/processed/AMEX-2001-0.csv' using delimiters ',';



for i in `find . -name "*.csv"`; do
    echo $i;
    cat $i | cut -d, -f1-42 > l;
    cat $i | cut -d, -f43-132 > m;
    cat $i | cut -d, -f133-208 > r;
    lam l -s,  r -s, m  > $i.fix;
    cat $i.fix >> `echo $i | sed 's/-.*//'`.out
done


copy tmp_ext_quote_amex from '/Users/kbedwell/dev/pydev/wm/stock/processed/AMEX.out' using delimiters ',' null as 'None';

select * from wm_exchange where symbol = 'AMEX';
alter table tmp_ext_quote_amex add column exchange_id integer default 54;

select count(0) from wm_stock_symbol;

\d wm_eod_quote;

alter table wm_eod_quote alter column volume type bigint;

select count(0) from wm_eod_quote;



select * from wm_stock_symbol  where symbol = 'AAME';

select * from wm_exchange where exchange_id = 68;


\d wm_eod_quote;

drop table tmp_quote;
create table tmp_quote (
    quote_id integer,
    exchange_id integer,
    symbol_id integer,
    quote_dt date,
    open float,
    high float,
    low float,
    close float,
    open_int integer,
    volume bigint
);

select count(0) from tmp_quote;

select symbol, name, active from wm_exchange order by name;


python -c 'from picker.bin.work import fix_orig; fix_orig()' -I ../extensions/ext_picker/picker/dev.ini

select * from wm_exchange where symbol = 'NASDAQ';

select * from wm_stock_symbol where exchange_id = 68 and symbol = 'WWWW';

68,22139


alter table crm_purchase_order add column shipping_cost float default 0.0;
alter table crm_purchase_order add column tax_cost float default 0.0;

alter table crm_report add column show_vendor_id boolean default false;



select company_id, name, paypal_id from crm_company;


alter table pvs_listing add column company_id integer;
alter table pvs_listing add foreign key (company_id) references crm_company;

alter table pvs_listing add column latitude float default 0.0;
alter table pvs_listing add column longitude float default 0.0;

alter table pvs_listing add column city varchar(50);
alter table pvs_listing add column state varchar(50);
alter table pvs_listing add column zip varchar(50);
alter table pvs_listing add column country varchar(50);
alter table pvs_listing add column ip varchar(15);
alter table pvs_listing add column dma integer default 0;

select date_part('hour', create_dt) from pvs_listing;

alter table pvs_listing alter column create_dt type timestamp;


select title, latitude, longitude from pvs_listing;

update pvs_listing set latitude=null, longitude=null;


select count(0) from wm_prediction where create_dt = '2011-05-05' and maturity_dt is not null and source = 'Earnings';

\d wm_prediction;


select open, close from wm_eod_quote where
exchange_id = 68 and symbol_id = 22139
and quote_dt = '2006-12-27';


select exchange_id, name from wm_exchange where symbol = 'NYSE';



select quote_dt, count(0) from wm_eod_quote
where exchange_id = 72
and quote_dt > '2011-01-01'
group by quote_dt
order by quote_dt;

\d wm_eod_quote;

alter table wm_eod_quote alter column volume type bigint;


select exchange_id, symbol from wm_exchange order by symbol;

alter table wm_exchange add column web_active boolean default true;

update wm_exchange set web_active = false
where exchange_id in (select exchange_id where symbol not in ('OTCBB', 'NYSE', 'NASDAQ', 'AMEX'));


select * from wm_stock_symbol where symbol = 'WWWW';

select * from pvs_listing;


                select listing_id, create_dt, title, description, category,
                radians(latitude) as latitude, radians(longitude) as longitude
                from pvs_listing where
                company_id = 6 and delete_dt is null;


select symbol, name from wm_stock_symbol where symbol_id = 20887;

select * from crm_product where product_id = 1695;


alter table cms_site add column default_campaign_id integer;
alter table cms_site add foreign key (default_campaign_id) references crm_campaign;



\d wm_prediction

select count(0) from wm_prediction;

update wm_prediction set valuation = null, target=null;

select username from core_user;


select count(0), symbol from wm_prediction p, wm_stock_symbol ss
where p.symbol_id = ss.symbol_id
group by ss.symbol
order by count(0) desc
limit 50;

select site_id, domain from cms_site;

select * from cms_page where site_id = 9;


alter table cms_page add column mod_dt date default now();
alter table crm_product_category add column mod_dt date default now();
alter table crm_product add column mod_dt date default now();

alter table crm_customer add column mod_dt timestamp default now();


alter table cms_page alter column mod_dt type timestamp;
alter table crm_product_category alter column mod_dt type timestamp;
alter table crm_product alter column mod_dt type timestamp;



select count(0) from crm_product where special = true;

\d core_asset;

select company_id, name from crm_company;

update crm_product set web_visible = false where product_id in (
select product_id from crm_product p where company_id = 5 and  not exists (select id from core_asset where fk_type = 'Product' and fk_id = p.product_id));


\d core_status_event;

select event_type, short_name from core_status_event where event_type = 'Customer';



select email from crm_customer where customer_id = 46;

update crm_customer set email = null where customer_id = 46;

delete from pvs_listing;

select listing_id, create_dt, title, description, category, radians(latitude) as latitude, radians(longitude) as longitude
from pvs_listing where company_id = 6 and delete_dt is null;


alter table pvs_listing add column show_location boolean default false;




select * from crm_customer;

\d crm_customer;


delete from pvs_listing where listing_id = 9;

select * from pvs_listing;

alter table crm_customer add column default_latitude float default 0.0;
alter table crm_customer add column default_longitude float default 0.0;

alter table crm_customer_order add column external_cart_id varchar(100);


select * from crm_customer_order where order_id = 921;

update crm_customer_order set external_cart_id = 'fud' where order_id = 921;

select title from pvs_listing;

insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system,
milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('ListingMessage', 'SEND_OK', 'SEND_OK', false, false, true,
false, false, false, false, false, false);

insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system,
milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('ListingMessage', 'SEND_FAIL', 'SEND_FAIL', false, false, true,
false, false, false, false, false, false);


select * from pvs_listing_message;

update pvs_listing_message set sent_dt = null;


SELECT *
FROM pvs_listing_message
WHERE pvs_listing_message.delete_dt IS NULL AND pvs_listing_message.sent_dt IS null
AND pvs_listing_message.listing_id = 24
ORDER BY pvs_listing_message.listing_message_id ASC;


select customer_id, md5(coalesce(email, password, '')) from crm_customer;

create index idx_customer_key on crm_customer (md5(coalesce(email, password, '')));
create index idx_rkey on pvs_listing_message (md5(responder_email));

select customer_id, email from crm_customer where
'fdf774eb58feefd35fc2abab7db194e8' = ;

select md5(coalesce('kenneth.bedwell@gmail.com', 'pass', ''));

select * from pvs_listing_message where listing_message_id = 3;

delete from pvs_listing_message;

select * from pvs_listing_message;

update pvs_listing_message set sent_dt = null where listing_message_id = (select max(listing_message_id) from pvs_listing_message);

select count(0) from pvs_listing_message where listing_id = 24 and listing_message_id = 13 and md5(text(customer_id)) = '8d5e957f297893487bd98fa830fa6413';

select listing_id, title, category, customer_id from pvs_listing;

select count


select lf.* from
                                   pvs_listing_favorite lf, pvs_listing l
                                   where lf.customer_id = 147
                                   and lf.listing_id = l.listing_id
                                   and lf.delete_dt is null;

select latitude, longitude from pvs_listing where listing_id = 8;

-- 30.1023 |  -81.3532
update pvs_listing set delete_dt = null, latitude = 30.09, longitude = -81.35 where listing_id = 8;
update pvs_listing set delete_dt = null, latitude = 30.1123, longitude = -81.3432 where listing_id = 6;

select title from pvs_listing where listing_id in (8,6);

alter table cms_page add column track boolean default false;





--    # listings last week
select count(0) from pvs_listing where date_part('week', create_dt) = date_part('week', current_timestamp)-1;
--    # listings this week
select count(0) from pvs_listing where date_part('week', create_dt) = date_part('week', current_timestamp);
--    # listings yesterday
select count(0) from pvs_listing where date_part('day', create_dt) = date_part('day', current_timestamp)-1;


--    # signups last week
select count(0) from crm_customer c, crm_campaign cmp where date_part('week', c.create_dt) = date_part('week', current_timestamp)-1
       and c.campaign_id = cmp.campaign_id and cmp.company_id = 6;
--    # signups this week
select count(0) from crm_customer c, crm_campaign cmp where date_part('week', c.create_dt) = date_part('week', current_timestamp)
       and c.campaign_id = cmp.campaign_id and cmp.company_id = 6;
--    # signups yesterday
select count(0) from crm_customer c, crm_campaign cmp where date_part('day', c.create_dt) = date_part('day', current_timestamp)
       and c.campaign_id = cmp.campaign_id and cmp.company_id = 6;


--    # messages last week
select count(0) from pvs_listing_message where date_part('week', create_dt) = date_part('week', current_timestamp)-1;
--    # messages this week
select count(0) from pvs_listing_message where date_part('week', create_dt) = date_part('week', current_timestamp);
--    # messages yesterday
select count(0) from pvs_listing_message where date_part('day', create_dt) = date_part('day', current_timestamp)-1;



\d crm_customer;

#/Applications/XAMPP/xamppfiles/bin/mysql -u ly -ply ly

alter table core_user add column vendor_id integer;
alter table core_user add foreign key (vendor_id) references crm_vendor;

alter table crm_product add column vendor_id integer;
alter table crm_product add foreign key (vendor_id) references crm_vendor;


alter table core_user_priv add column edit_category boolean default false;
alter table core_user_priv add column barcode_order boolean default false;

alter table crm_report add column is_vendor boolean default false;


select * from crm_company;


SELECT crm_customer.*
FROM crm_customer JOIN crm_campaign ON crm_campaign.campaign_id = crm_customer.campaign_id
WHERE crm_customer.delete_dt IS NULL AND crm_campaign.company_id = 4 AND crm_customer.email ILIKE 'v@v.com';

select * from crm_customer where email like 'v@v%';

select * from crm_product_pricing where product_id = 1707;


SELECT crm_purchase_order_item.*
FROM crm_purchase_order_item
WHERE 69 = crm_purchase_order_item.purchase_order_id ORDER BY crm_purchase_order_item.order_item_id;

select purchase_order_id, create_dt from crm_purchase_order_item;


select count(0) from wm_eod_quote;

select max(create_dt) from wm_eod_quote;

select * from core_user;

insert into crm_product (name, vendor_id, third_party_id) values ();

select product_id from crm_product where name = 'KeyFobs - Assorted';

delete from crm_product_pricing where product_id >= 1724;
delete from crm_product_inventory_journal where product_id >= 1724;
delete from crm_product where product_id >= 1724;


select * from crm_company where name like 'Amy%';

select * from crm_enterprise;

\d crm_product_inventory_journal;




select inv_journal_id, product_id, quantity, create_dt, delete_dt, type from crm_product_inventory_journal where product_id = 1603
and create_dt = '2011-07-08'
order by inv_journal_id;
select product_id, order_id, create_dt, delete_dt, quantity from crm_order_item where product_id = 1603 and create_dt >= '2011-04-14'
and create_dt = '2011-07-08'
order by order_item_id;


select inv_journal_id, product_id, quantity, create_dt, delete_dt, type from crm_product_inventory_journal where product_id = 1720
order by inv_journal_id;
select product_id, order_id, create_dt, delete_dt, quantity from crm_order_item where product_id = 1720
order by order_item_id;
select sum(quantity) from crm_product_inventory_journal where product_id = 1720;


select * from crm_report;

alter table crm_report drop column company_id;

select count(0) from wm_exchange_period;

\d wm_exchange;


select exchange_id, count(0) from wm_exchange_period group by exchange_id;

select count(0) from wm_exchange_period where score0 > 4.01 and score0 < 5.01 and exchange_id = 68;

select count(0) from wm_exchange_period where score0 is null and exchange_id = 68;

select start_dt, end_dt from wm_exchange_period where exchange_id = 68 and score0 >4.01 and score0 <5.02;


http://api.buyins.net/37363245-3632-4439-2D36-3936452D3445

\d wm_prediction;

select prediction_id from
wm_prediction where link = 'http://api.buyins.net/index.php?user=wealthmakers&pass=vfh%21%2175gh456%24Wv&object=report&action=get&type=prediction-success&uid=E267269D-696E-4EC6-9F60-91270FEABC80&format=html';

select prediction_id, link from wm_prediction limit 10;


select exchange_id from wm_exchange where symbol = 'NYSE';

select symbol_id from wm_stock_symbol where symbol = 'GEO' and exchange_id = 72;

select title from wm_prediction where symbol_id = 24904;

select count(0) from wm_eod_quote where quote_dt = '2011-03-01';


select cust.customer_id,
       o.create_dt, cust.email, o.order_id,
  sum(oi.unit_cost*oi.quantity) as "cost",
  (sum(oi.unit_price*oi.quantity)) as "item_revenue",
  (coalesce(o.shipping_total, 0)) as "shipping_revenue",
  (coalesce(o.handling_total, 0)) as "handling_revenue",
  (sum(oi.unit_price*oi.quantity)+coalesce(o.shipping_total,0)+coalesce(o.handling_total,0)) as "total_revenue",
  (sum((oi.unit_price-(oi.unit_price-oi.unit_discount_price))*oi.quantity)) as "discount",
  coalesce(  (select sum(coalesce(amount,0)) from crm_journal
     where order_id = o.order_id
    and type in ('CreditIncrease', 'Refund')), 0) as "refunds",
  coalesce(  (select sum(coalesce(amount,0)) from crm_journal
     where order_id = o.order_id
    and type in ('FullPayment', 'PartialPayment')), 0) as "payments",
  coalesce(  (sum(oi.unit_price*oi.quantity)+coalesce(o.shipping_total,0)+coalesce(o.handling_total,0))
    -coalesce((select sum(coalesce(amount,0)) from crm_journal
              where order_id = o.order_id
              and type in ('FullPayment', 'PartialPayment')), 0), 0) as "due",
  csx.display_name,
  CASE WHEN o.user_created is null THEN 'WEB'
            ELSE 'OFFICE'
       END as source
from
  crm_customer_order o, crm_customer cust,
  crm_order_item oi, crm_campaign cmp,
  crm_company co, core_status cs, core_status_event csx
where
o.customer_id = cust.customer_id and
o.order_id = oi.order_id and
o.campaign_id = cmp.campaign_id and
cmp.company_id = co.company_id and
co.enterprise_id = 3 and
o.delete_dt is null and
oi.delete_dt is null and
o.status_id = cs.status_id and
cs.event_id = csx.event_id and
  ('2011-06-01' is null or o.create_dt > '2011-06-01') and
  ('2011-07-01' is null or o.create_dt < '2011-07-01')
group by o.create_dt, cust.email,
  o.order_id, csx.display_name, cust.customer_id, o.user_created, o.shipping_total, o.handling_total
order by o.order_id desc;


alter table core_user_priv add column edit_discount boolean default false;


delete from crm_discount;


select * from wm_stock_symbol where symbol = 'F';

select symbol, name from wm_stock_symbol where name like 'Ford%';

delete from wm_ireport_prediction_join;
delete from wm_ireport_order;
delete from wm_ireport;
delete from wm_prediction where price is null;


select name, symbol, symbol_id from wm_stock_symbol where symbol='WWWW';

select * from wm_ireport limit 10;


alter table wm_prediction add column release_dt date;

\d wm_prediction;

select prediction_id, link from wm_prediction where source = 'Friction Factor' limit 10;

delete from wm_prediction where source = 'Friction Factor';


copy (
select cust.fname, cust.lname, cust.customer_id,
       o.create_dt, cust.email, o.order_id
from
  crm_customer cust,
  crm_order_item oi, crm_campaign cmp,
  crm_company co, core_status cs, core_status_event csx,
  crm_customer_order o
where
o.customer_id = cust.customer_id and
o.order_id = oi.order_id and
o.campaign_id = cmp.campaign_id and
cmp.company_id = co.company_id and
co.enterprise_id = 5 and
o.delete_dt is null and
oi.delete_dt is null and
o.status_id = cs.status_id and
cs.event_id = csx.event_id
group by cust.fname, cust.lname, cust.customer_id, o.create_dt, cust.email, o.order_id,
  o.order_id, csx.display_name, cust.customer_id, o.user_created, o.shipping_total, o.handling_total
order by o.order_id asc
) to '/tmp/rpt.csv' with CSV;

select name, enterprise_id from crm_enterprise;


select * from core_status where status_id = 1918;

select * from core_status_event where event_id = 9;

select * from core_status where event_id = 9;


\d wm_prediction;

select prediction_id, title from wm_prediction where source = 'Valuation' order by create_dt limit 10;

\d wm_prediction;

\d wm_ireport;

select ss.name || ' (' || e.symbol || ':' || ss.symbol || ') {' || i.ireport_id || '}'
from wm_ireport i, wm_stock_symbol ss, wm_exchange e
where
i.symbol_id = ss.symbol_id
and ss.exchange_id = e.exchange_id
and lower(ss.name) like 'fo%';

select distinct(product_id) from wm_ireport;

select * from crm_billing where billing_id = 30;


SELECT * FROM core_user where 1=1
                and lower(lname) like 'bedwell%' ;




select cust.customer_id, cust.fname, cust.lname, cust.phone, cust.email,
sum(oi.unit_price*oi.quantity) as revenue,
sum(oi.unit_cost*oi.quantity) as cost,
sum((oi.unit_price*oi.quantity)-(oi.unit_cost*oi.quantity)) as profit
from
crm_customer_order o, crm_customer cust, crm_order_item oi, crm_campaign cmp, crm_product p
where
o.customer_id = cust.customer_id and
o.order_id = oi.order_id and
o.campaign_id = cmp.campaign_id and
cmp.company_id = 5
and oi.product_id = p.product_id
and o.delete_dt is null
and oi.delete_dt is null
group by cust.fname, cust.lname, cust.phone, cust.email
order by sum(oi.unit_price*oi.quantity) desc
limit 10;

select company_id, name from crm_company;


select coalesce(null, 2);


select p.product_id, v.name as "vendor", p.name, oi.create_dt,
sum(oi.quantity) as quantity,
sum(oi.unit_price*oi.quantity) as revenue,
  sum(coalesce(oi.unit_cost,0)*oi.quantity) as cost,
  sum((oi.unit_price*oi.quantity)-(coalesce(oi.unit_cost,0)*oi.quantity)) as profit
from
crm_customer_order o, crm_customer cust, crm_order_item oi, crm_campaign cmp, crm_product p, crm_vendor v
where
o.customer_id = cust.customer_id and
o.order_id = oi.order_id and
o.campaign_id = cmp.campaign_id and
cmp.company_id = 4 and
oi.product_id = p.product_id and
o.delete_dt is null and
oi.delete_dt is null and
v.vendor_id = p.vendor_id
group by p.product_id, v.name, p.name, oi.create_dt
order by v.name
;



and  ('{rpt_start_dt}' is null or o.create_dt > '{rpt_start_dt}') and
  ('{rpt_end_dt}' is null or o.create_dt < '{rpt_end_dt}')


select o.order_id, c.email
from wm_ireport_order iro, crm_customer_order o, crm_order_item oi, crm_product p, crm_customer c, crm_oi_terms_acceptance t
where iro.order_id = o.order_id
and o.customer_id = c.customer_id
and o.order_id = oi.order_id
and oi.product_id = p.product_id
and p.sku = 'WM-010'
and t.order_id = o.order_id
and t.order_item_id = oi.order_item_id
and t.delete_dt is null
and o.delete_dt is null
and o.cancel_dt is null
and t.signature is not null
and t.signature = c.email
and (select sum(_j.amount) from crm_journal _j
     where _j.order_id = o.order_id
     and _j.delete_dt is null) = (select sum(_oi.unit_price) from crm_order_item _oi
                                  where _oi.delete_dt is null
                                  and _oi.order_id = o.order_id)
and not exists (select 1 from
        core_status _s, core_status_event _se
        where _s.customer_id = c.customer_id
        and _s.event_id = _se.event_id
        and _s.fk_type = 'OrderItem'
        and _s.fk_id = oi.order_item_id
        and _se.short_name = 'WM_IREPORT_DELIVERED')
;

delete from core_status where event_id = (select event_id from core_status_event where short_name = 'WM_IREPORT_DELIVERED');

select order_id, customer_id, create_dt, delete_dt from crm_customer_order where order_id > 125;

select * from core_status_event;


select distinct(source) from wm_prediction;

select email, customer_id, create_dt from crm_customer;


SELECT  'SELECT SETVAL(' ||quote_literal(S.relname)|| ', MAX(' ||quote_ident(C.attname)|| ') ) FROM ' ||quote_ident(T.relname)|| ';'
FROM pg_class AS S, pg_depend AS D, pg_class AS T, pg_attribute AS C
WHERE S.relkind = 'S'
    AND S.oid = D.objid
    AND D.refobjid = T.oid
    AND D.refobjid = C.attrelid
    AND D.refobjsubid = C.attnum
ORDER BY S.relname;


SELECT  'SELECT SETVAL(' ||quote_literal(S.relname)|| ', MAX(' ||quote_ident(C.attname)|| ') ) FROM ' ||quote_ident(T.relname)|| ';'
FROM pg_class AS S, pg_depend AS D, pg_class AS T, pg_attribute AS C
WHERE S.relkind = 'S'
    AND S.oid = D.objid
    AND D.refobjid = T.oid
    AND D.refobjid = C.attrelid
    AND D.refobjsubid = C.attnum
ORDER BY S.relname;


select name, campaign_id from crm_campaign;


select v.name,v.vendor_id,
sum(oi.quantity) as quantity,
sum(oi.unit_price*oi.quantity) as revenue,
  sum(coalesce(oi.unit_cost,0)*oi.quantity) as cost,
  sum((oi.unit_price*oi.quantity)-(coalesce(oi.unit_cost,0)*oi.quantity)) as profit
from
crm_customer_order o, crm_customer cust, crm_order_item oi, crm_campaign cmp, crm_product p,
  crm_vendor v, crm_company co
where
o.customer_id = cust.customer_id and
o.order_id = oi.order_id and
o.campaign_id = cmp.campaign_id and
    (length('4') = 0 or cast(cmp.company_id as text) = '4') and
oi.product_id = p.product_id and
o.delete_dt is null and
oi.delete_dt is null and
cmp.company_id = co.company_id and
co.enterprise_id = 2 and
v.vendor_id = p.vendor_id and
    ('2011-08-01' is null or o.create_dt > '2011-08-01') and
    ('2011-08-31' is null or o.create_dt < '2011-08-31')
group by v.name, v.vendor_id
order by v.name;



select v.name,v.vendor_id,
o.order_id, oi.order_item_id,
oi.quantity, oi.create_dt,
oi.unit_price*oi.quantity as revenue,
coalesce(oi.unit_cost,0)*oi.quantity as cost,
(oi.unit_price*oi.quantity)-(coalesce(oi.unit_cost,0)*oi.quantity) as profit
from
crm_customer_order o, crm_customer cust, crm_order_item oi, crm_campaign cmp, crm_product p,
  crm_vendor v, crm_company co
where
o.customer_id = cust.customer_id and
o.order_id = oi.order_id and
o.campaign_id = cmp.campaign_id and
    (length('4') = 0 or cast(cmp.company_id as text) = '4') and
oi.product_id = p.product_id and
o.delete_dt is null and
oi.delete_dt is null and
cmp.company_id = co.company_id and
co.enterprise_id = 2 and
v.vendor_id = p.vendor_id and
    ('2011-08-01' is null or o.create_dt > '2011-08-01') and
    ('2011-08-31' is null or o.create_dt < '2011-08-31')
and v.vendor_id = 31
order by v.name;


select * from crm_product_inventory_journal where order_item_id = 4496;

delete from crm_product_inventory_journal where order_item_id = 4496;
delete from crm_order_item where order_item_id = 4496;
delete from crm_product_inventory_journal where order_item_id = 4488;
delete from crm_order_item where order_item_id = 4488;

select count(0), source from wm_prediction group by source;


delete from wm_friction_factor_raw;
delete from wm_squeeze_trigger_raw;
delete from wm_ireport_prediction_join;
delete from wm_ireport_order;
delete from wm_prediction where source = 'Prediction Success';
delete from wm_ireport;

alter table wm_prediction add column vv float;
alter table wm_prediction add column ve float;
alter table wm_prediction add column target_orig float;

alter table wm_ireport add column inactive_dt timestamp;

alter table wm_ireport add column status_id integer;
alter table wm_ireport add foreign key (status_id) references core_status;

\d wm_ireport;

\d wm_prediction;



select quote_id from base_quotes b
where b.close / (select b_.close from base_quotes b_ where b_.symbol_id = b.symbol_id and b_.dt < b.dt -


select o.order_id, iro.ir_order_id, oi.order_item_id
from wm_ireport_order iro, crm_customer_order o, crm_order_item oi, crm_product p, crm_customer c, crm_oi_terms_acceptance t
where iro.order_id = o.order_id
and o.customer_id = c.customer_id
and o.order_id = oi.order_id
and oi.product_id = p.product_id
and p.sku = 'WM-010'
and t.order_id = o.order_id
and t.order_item_id = oi.order_item_id
and t.delete_dt is null
and o.delete_dt is null
and o.cancel_dt is null
and t.signature is not null
and t.signature = c.email
and exists (select 1 from
            core_status _s, core_status_event _se
            where _s.customer_id = c.customer_id
            and _s.event_id = _se.event_id
            and _s.fk_type = 'OrderItem'
            and _s.fk_id = oi.order_item_id
            and _se.short_name = 'WM_IREPORT_DELIVERED');

select * from wm_ireport_order where delivery_dt is not Null;


select * from wm_stock_symbol where symbol = 'WWWW';

update wm_ireport set notes = ' ', target_hit_dt = null, inactive_dt = null;


select name, company_id from crm_company;

alter table crm_vendor add column send_month_end_report boolean default false;


select * from core_asset;

select count(0),  fk_type from core_asset group by fk_type;

select * from core_key_value;

delete from core_key_value;


select password from crm_customer where email = 'amers_j@yahoo.com';

select count(0) from wm_stock_symbol;

select name, symbol, avgmonthvolume from wm_stock_symbol where symbol_id = 19600;

select avg(avgmonthvolume) from wm_stock_symbol
where exchange_id = (select exchange_id from wm_exchange where symbol = 'NASDAQ');

select count(0) from wm_stock_symbol
where exchange_id = (select exchange_id from wm_exchange where symbol = 'NASDAQ');





select name, exchange_id from wm_exchange;

\d wm_stock_symbol;





select count(0) from wm_ireport where inactive_dt is null;



select count(0) from (select distinct i.ireport_id /*p.prediction_id, p.maturity_dt*/
from wm_ireport i, wm_prediction p, wm_ireport_prediction_join j
where i.ireport_id = j.ireport_id
and j.prediction_id = p.prediction_id
and i.inactive_dt is null
and p.maturity_dt <= current_date
order by i.ireport_id) x;




select product_id, name from crm_product where product_id not in (select distinct(product_id) from crm_product_category_join) and company_id = 4;


select p.product_id, p.name, pc.category_id
from crm_product p, crm_product_category pc
where p.product_id = pc.category_id


select * from wm_customer_holding where customer_id = 312;


select * from crm_appointment;

update crm_appointment set start_time = '12:00' where appointment_id = 17;

delete from crm_appointment where appointment_id= (select max(appointment_id) from crm_appointment);

alter table crm_appointment add column user_assigned varchar(50);


select * from crm_appointment where
(user_created = 'tomronk@gmail.com' or user_assigned = 'tomronk@gmail.com')
and date_part('month', start_dt) = 9
and date_part('year', start_dt) = 2011
and date_part('day', start_dt) = 11
order by start_time asc;


select date_part('month', start_dt), date_part('day', start_dt), date_part('year', start_dt) from crm_appointment where user_assigned = 'tomronk@gmail.com';


select symbol_id, count(0), sum(cast (value as numeric))/1000000 from wm_customer_holding group by symbol_id limit 10;

select count(0) from (
select quote_id, exchange_id, symbol_id, quote_dt, open, high, low, close, 0, volume
                 from wm_eod_quote where exchange_id = 68 and quote_dt >= '2011-06-27'
) x;


/* KB: [2011-10-18]: optout by day */
select count(0), s.create_dt, cmp.name from
core_status_event se ,
core_status s,
crm_customer c,
crm_campaign cmp
where se.short_name = 'EMAIL_OPT_OUT'
and se.event_id = s.event_id
and c.customer_id = s.customer_id
and cmp.campaign_id = c.campaign_id
group by s.create_dt, cmp.name
order by s.create_dt desc;


select count(0), s.create_dt, cmp.name from
core_status_event se ,
core_status s,
crm_customer c,
crm_campaign cmp
where se.short_name = 'CLICKBACK'
and se.event_id = s.event_id
and c.customer_id = s.customer_id
and cmp.campaign_id = c.campaign_id
group by s.create_dt, cmp.name
order by s.create_dt desc;


select c.cmail
from


crm_customer c,
crm_campaign cmp
where c.customer_id = s.customer_id
and cmp.campaign_id = c.campaign_id
group by s.create_dt, cmp.name
order by s.create_dt desc;

select count(0) from (
SELECT cu.*
                 FROM crm_product p, crm_company com, crm_campaign cam, crm_customer cu, crm_customer_order co, crm_order_item oi
                 where p.company_id = com.company_id
                 and cam.company_id = com.company_id
                 and cam.campaign_id = cu.campaign_id
                 and cu.customer_id = co.customer_id
                 and co.order_id = oi.order_id
                 and oi.product_id = p.product_id
                 and cam.delete_dt is null
                 and co.cancel_dt is null
                 and cu.delete_dt is null
                 and oi.delete_dt is null
                 and com.enterprise_id = 5
                 and p.company_id=7 ) x;


select * from crm_enterprise;

select * from wm_ireport_prediction_join where prediction_id = 46802;


update wm_ireport set inactive_dt = null where inactive_dt > current_date-1;



insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system, milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('IReport', 'CREATE', 'Create', false, false, false, true, false, false, false, true, false);

insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system, milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('IReport', 'UPDATE', 'UPDATE', false, false, false, true, false, false, false, true, false);

insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system, milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('IReport', 'INACTIVE', 'Inactive', false, false, false, true, false, false, false, true, false);

insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system, milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('IReport', 'ADD_PREDICTION', 'Add Prediction', false, false, false, true, false, false, false, true, false);



delete from wm_ireport_prediction_join;
delete from wm_ireport_order;
delete from wm_ireport;
delete from wm_prediction where price is null;

update core_status_event set enterprise_id = 5 where event_type = 'IReport';

select * from crm_enterprise;


alter table wm_friction_factor_raw alter column share_factor type float;

delete from wm_friction_factor_raw where position(',' in report_date) > 0;


create index wm_ff_raw_dt_sym on wm_friction_factor_raw (report_date, symbol_id);
create index wm_ss_raw_dt_sym on wm_squeeze_trigger_raw (report_date, symbol_id);
create index wm_pred_link on wm_prediction(link);
create index wm_pred_sym_crdt_src on wm_prediction(symbol_id, create_dt, source);
create index wm_pred_sym_type on wm_prediction(symbol_id, type);
create index wm_irpt_sym_id on wm_ireport(symbol_id);
create index wm_irpt_inactive on wm_ireport(inactive_dt);


alter table cms_site add column maintenance_mode boolean default false;

select * from crm_product_pricing where product_id = 2031;



select * from crm_customer_order where order_id > 2230;

select current_date;

select * from crm_campaign;

\d crm_campaign;

alter table crm_order_item drop column tax;
alter table crm_order_item add column tax float default 0.0;


     select distinct o.order_id, iro.ir_order_id, oi.order_item_id
     from wm_ireport_order iro, crm_customer_order o, crm_order_item oi,
        crm_product p, crm_customer c, crm_oi_terms_acceptance t
     where iro.order_id = o.order_id
     and o.customer_id = c.customer_id
     and o.order_id = oi.order_id
     and oi.product_id = p.product_id
     and p.sku = 'WM-010'
     and t.order_id = o.order_id
     and t.order_item_id = oi.order_item_id
     and t.delete_dt is null
     and o.delete_dt is null
     and o.cancel_dt is null
     and t.signature is not null
     and t.signature = c.email
     and (select sum(_j.amount) from crm_journal _j
          where _j.order_id = o.order_id
          and _j.delete_dt is null) = (select sum(_oi.unit_price) from crm_order_item _oi
                                       where _oi.delete_dt is null
                                       and _oi.order_id = o.order_id)
     and not exists (select 1 from
             core_status _s, core_status_event _se
             where _s.customer_id = c.customer_id
             and _s.event_id = _se.event_id
             and _s.fk_type = 'OrderItem'
             and _s.fk_id = oi.order_item_id
             and _se.short_name = 'WM_IREPORT_DELIVERED');


\d crm_appointment;

                        select ss.symbol, p.prediction_direction,
                        case when p.source = 'Earnings' then p.source || ' ' || p.prediction_disposition
                        else p.source
                        end,
                        date_part('days', p.maturity_dt-now()) maturity_days,
                        ss.today_last,p.price, p.target,
                        round(cast (@(p.target-p.price)/p.price as numeric),2) as gap,
                        round(cast (@(p.target-p.price) as numeric), 2) as price_diff,
                        round(cast (p.avg_volatility as numeric), 2) as avg_volatility,
                        round(cast (@(p.target-p.price)/p.avg_volatility as numeric), 2) days_required_to_cover,
                        round(cast (date_part('days', p.maturity_dt-now())-((@(p.target-p.price))/p.avg_volatility) as numeric), 2) days_left_over_after_cover,
                        p.link, p.prediction_id,

                       ss.name || ' (' || e.symbol || ':' || ss.symbol || ') [' || p.prediction_id || ']' as prediction_name
                        from wm_prediction p, wm_stock_symbol ss, wm_exchange e
                        where
                        p.price is not null and p.price > 0 and
                        p.symbol_id = ss.symbol_id and
                        p.target is not null and
                        --p.sector is not null and
                        p.maturity_dt is not null and
                        p.source not in ('SqueezeTrigger', 'Friction Factor', 'Prediction Success') and
                        p.release_dt is null and
                        p.maturity_dt > now() and
                        ((p.prediction_direction = 'UP' and ss.today_last < p.target and p.target > p.price)
                                                 or (p.prediction_direction = 'DOWN' and ss.today_last > p.target and p.target < p.price)) and
                        --(@(p.target-p.price))/p.avg_volatility <date_part('days', p.maturity_dt-now()) and
                        p.target > 0 and
                        p.avg_volatility > 0 and
                        ss.exchange_id = e.exchange_id and
                         lower(ss.name) like 'f%' and
                        1=1
                        --order by date_part('days', p.maturity_dt-now())-(p.target-p.price)/p.avg_volatility desc
                        order by @(p.target-p.price)/p.price desc
                        --order by source desc
                        limit 20;


select symbol, name from wm_exchange;

update wm_ireport set inactive_dt = null where inactive_dt > current_date-1;


copy wm_exchange to '/tmp/wm_exchange.copy';
copy wm_stock_symbol to '/tmp/wm_stock_symbol.copy';
copy wm_eod_quote to '/tmp/wm_stock_symbol.copy';

copy (select * from wm_eod_quote where quote_dt between '2011-01-01' and '2011-12-31') to '/tmp/wm_eod_quote.copy';

\d wm_exchange.copy;


psql -U postgres -d wm -c "copy binary wm_exchange to '/tmp/wm_exchange.copy'"
psql -U postgres -d wm -c "copy binary wm_eod_quote to '/tmp/wm_eod_quote.copy'"
psql -U postgres -d wm -c "copy binary wm_stock_symbol to '/tmp/wm_stock_symbol.copy'"

copy binary pick_exchange from '/tmp/wm_exchange.copy';
copy binary pick_stock_symbol from '/tmp/wm_stock_symbol.copy';
copy binary pick_eod_quote from '/tmp/wm_eod_quote.copy';

truncate table pick_eod_quote cascade;
truncate table pick_stock_symbol cascade;
truncate table pick_exchange cascade;



update wm_ireport set inactive_dt = null where inactive_dt > current_date-1;

select v.name, sum(oi.unit_cost*oi.quantity) as cost,
                           sum(oi.unit_price*oi.quantity) as revenue,
                           sum((oi.unit_price*oi.quantity)-(oi.unit_cost*oi.quantity)) as profit
                    from
                    crm_customer_order o, crm_customer cust,
                    crm_order_item oi, crm_campaign cmp,
                    crm_company co, core_status cs, core_status_event cse, crm_product p,
                    crm_vendor v
                    where
                    o.customer_id = cust.customer_id and
                    o.order_id = oi.order_id and
                    o.campaign_id = cmp.campaign_id and
                    oi.product_id = p.product_id and
                    cmp.company_id = co.company_id and
                    co.enterprise_id = 3 and
                    o.delete_dt is null and
                    oi.delete_dt is null and
                    o.status_id = cs.status_id and
                    cs.event_id = cse.event_id and
                    extract(month from o.create_dt) = extract(month from current_date) and
                    extract(year from o.create_dt) = extract(year from current_date) and
                    p.vendor_id = v.vendor_id
                    group by v.name
                    order by sum(oi.unit_price*oi.quantity) desc;


select count(0) from crm_customer;


select count(0) as cnt, cust.create_dt
                    from
                    crm_customer cust, crm_campaign cmp, crm_company co
                    where
                    cust.campaign_id = cmp.campaign_id and
                    cmp.company_id = co.company_id and
                    co.enterprise_id = 3 and
                    cust.delete_dt is null and
                    cust.create_dt between current_date - 7 and current_date
                    group by cust.create_dt
                    order by cust.create_dt desc;


select split_part(start_time, ':', 1) from crm_appointment where
(user_created = 'kenneth.bedwell@gmail.com' or user_assigned = 'kenneth.bedwell@gmail.com')
order by start_time asc;




alter table crm_company drop column email_type;
alter table crm_company rename column email_addr_system to email;
alter table crm_company add column smtp_username varchar(50);
alter table crm_company rename column email_password to smtp_password;
alter table crm_company rename column email_smtp_server to smtp_server;
alter table crm_company add column imap_username varchar(50);
alter table crm_company rename column email_imap_server to imap_server;
alter table crm_company add column imap_password varchar(50);
update crm_company set smtp_username = email, imap_username = email, imap_password = smtp_password;
alter table crm_campaign drop column email_type;
alter table crm_campaign rename column email_addr_system to email;
alter table crm_campaign add column smtp_username varchar(50);
alter table crm_campaign rename column email_password to smtp_password;
alter table crm_campaign rename column email_smtp_server to smtp_server;
alter table crm_campaign add column imap_username varchar(50);
alter table crm_campaign rename column email_imap_server to imap_server;
alter table crm_campaign add column imap_password varchar(50);
update crm_campaign set smtp_username = email, imap_username = email, imap_password = smtp_password;
alter table core_user drop column email_addr_system;
alter table core_user drop column email_type;
alter table core_user add column smtp_username varchar(50);
alter table core_user rename column email_password to smtp_password;
alter table core_user rename column email_smtp_server to smtp_server;
alter table core_user add column imap_username varchar(50);
alter table core_user rename column email_imap_server to imap_server;
alter table core_user add column imap_password varchar(50);
update core_user set smtp_username = email, imap_username = email, imap_password = smtp_password;



select * from crm_enterprise;

drop table wm_quote_print;

delete from wm_quote_print;

create unique index wm_qp_by_type on wm_quote_print (quote_id, lookback);

\d wm_eod_quote;

select count(0), max(q.quote_dt), min(q.quote_dt), e.symbol, e.name, e.exchange_id from
wm_eod_quote q, wm_exchange e
where q.exchange_id = e.exchange_id
group by e.symbol, e.name, e.exchange_id
order by count(0);

delete from wm_eod_quote q where q.exchange_id = 73 and q.quote_dt < '2007-01-01';

select exchange_id from wm_exchange where symbol = 'OTCBB';


select count(0), q.quote_dt
from wm_eod_quote q
where q.exchange_id = 74
and q.quote_dt > '2011-09-01'
group by q.quote_dt
order by q.quote_dt asc;


SELECT pg_size_pretty(pg_database_size('wm'));


drop table pick_exchange;

insert into pick_exchange select * from wm_exchange;
insert into pick_stock_symbol select * from wm_stock_symbol;
insert into pick_eod_quote select * from wm_eod_quote;

drop function merge_table(tbl_origin varchar, tbl_destination varchar, pk_column varchar);
CREATE or replace FUNCTION merge_table(tbl_source varchar, tbl_destination varchar, pk_column varchar) RETURNS VOID AS
$$
BEGIN
    /* clean out all the rows that are in pick* that are not in wm* (splits, renames, drops, etc) */
    execute 'delete from ' || tbl_destination || ' where ' || pk_column
            || ' in (select ' || pk_column || ' from ' || tbl_destination
            || '     except '
            || '     select ' || pk_column || ' from ' || tbl_source || ')';
    /* copy over everything from source to destination that is not in destination already. */
    execute 'insert into ' || tbl_destination || ' select * from ' || tbl_source || ' ts where ts.' || pk_column
            || '              not in (select ' || pk_column || ' from ' || tbl_destination || ')';
END;
$$
LANGUAGE plpgsql;


select merge_table('wm_exchange', 'pick_exchange', 'exchange_id');
select merge_table('wm_stock_symbol', 'pick_stock_symbol', 'symbol_id');


delete from pick_eod_quote where quote_id in
(select quote_id from pick_eod_quote
 except
 select quote_id from wm_eod_quote); /* not in this one */


truncate table pick_exchange cascade;

select * into tmp_ss from wm_stock_symbol;

----------------------

insert into pick_exchange (exchange_id,symbol,name,type,suffix,create_dt,delete_dt,active,web_active)
    select exchange_id,symbol,name,type,suffix,create_dt,delete_dt,active,web_active from wm_exchange x
    where x.exchange_id not in (select exchange_id from pick_exchange);

insert into pick_stock_symbol (symbol_id,symbol,exchange_id,name,ipo_year,sector,industry,summary,create_dt,delete_dt,external_id,div_yield,ptb,dps,pts,eps,yieldd,pe,nta,dividend,ebitda,ma1,yearlow,ma2,ma5,avgmonthvolume,yearchange,monthlow,monthchange,mtm14,weekhigh,yearhigh,weeklow,ma100,ma200,threemonthchange,avgmonthchange,volumechange,avgyearvolumne,ma20,sixmonthchange,sar,change,volatility,avgweekchange,rsi14,wpr14,sto9,mareturn,liquidity,ma50,ptc,avgyearchange,weekchange,avgweekvolume,monthhigh,mapercent,roc14,previous,shares,market_cap,description,today_high,today_low,today_last,today_open,today_change,today_vol,today_update_dt)
    select symbol_id,symbol,exchange_id,name,ipo_year,sector,industry,summary,create_dt,delete_dt,external_id,div_yield,ptb,dps,pts,eps,yieldd,pe,nta,dividend,ebitda,ma1,yearlow,ma2,ma5,avgmonthvolume,yearchange,monthlow,monthchange,mtm14,weekhigh,yearhigh,weeklow,ma100,ma200,threemonthchange,avgmonthchange,volumechange,avgyearvolumne,ma20,sixmonthchange,sar,change,volatility,avgweekchange,rsi14,wpr14,sto9,mareturn,liquidity,ma50,ptc,avgyearchange,weekchange,avgweekvolume,monthhigh,mapercent,roc14,previous,shares,market_cap,description,today_high,today_low,today_last,today_open,today_change,today_vol,today_update_dt
    from wm_stock_symbol x
    where x.symbol_id not in (select symbol_id from pick_stock_symbol);

insert into pick_eod_quote (quote_id,symbol_id,exchange_id,quote_dt,open,high,low,close,volume,create_dt)
    select quote_id,symbol_id,exchange_id,quote_dt,open,high,low,close,volume,create_dt
    from wm_eod_quote x
    where x.quote_id not in (select quote_id from pick_eod_quote);

delete from pick_eod_quote where quote_id in
       (select quote_id from pick_eod_quote
        except
        select quote_id from wm_eod_quote);

delete from pick_stock_symbol where symbol_id in
       (select symbol_id from pick_stock_symbol
        except
        select symbol_id from wm_stock_symbol);

delete from pick_exchange where exchange_id in
       (select exchange_id from pick_exchange
        except
        select exchange_id from wm_exchange);





select count(0) from wm_stock_symbol;
select count(0), industry from wm_stock_symbol where industry is not null group by industry order by count(0) ;


\d wm_eod_quote;


create index pick_ex_sym_qtdt on pick_eod_quote (exchange_id, symbol_id, quote_dt);


select count(0) from  wm_stock_symbol where exchange_id = 60;

select max(quote_dt), min(quote_dt) from wm_eod_quote where symbol_id = 9517;

select * from wm_stock_symbol where exchange_id= 60 and symbol = 'OFIN';




select s.symbol_id, s.name, s.symbol, count(0)  from wm_stock_symbol s, wm_eod_quote q
where s.exchange_id = 60
and q.symbol_id = s.symbol_id
and q.quote_dt < '2006-08-08'
group by s.symbol_id, s.name, s.symbol
order by count(0);


select * from pick_index_correlation;

select min(quote_dt), max(quote_dt) from wm_eod_quote where symbol_id = 22139;

select * from wm_exchange where symbol in ('NASDAQ', 'INDEX', 'AMEX');



select count(0), symbol_id, exchange_id, quote_dt
 from wm_eod_quote where quote_dt between '2003-01-01' and '2005-12-31'
group by symbol_id, exchange_id, quote_dt
having count(0) > 1;





select * from pick_exchange where symbol = 'UNK';

update pick_exchange set active = false where exchange_id = 34;



select avg(q.volume), s.symbol_id, s.symbol, s.name, e.name
from wm_eod_quote q, wm_stock_symbol s, wm_exchange e
where q.symbol_id = s.symbol_id
and q.exchange_id = e.exchange_id
and q.quote_dt between '2011-01-01' and current_date
and q.exchange_id = 68
group by s.symbol, s.name, e.name
order by avg(q.volume) desc
limit 100;


update pick_stock_symbol set update_eod_quote = false;


drop table pick_eod_quote;


select symbol, exchange_id from pick_exchange where symbol in
('OTCBB', 'NASDAQ', 'NYSE', 'AMEX', 'FOREX', 'INDEX');

select name,symbol from pick_exchange order by name;

 AMEX   |           1
 NASDAQ |          21
 NYSE   |          26
 OTCBB  |          28


select count(0), e.name
from pick_stock_symbol ss, pick_exchange e
where e.exchange_id = ss.exchange_id
and ss.update_eod_quote = true
group by e.name;

update pick_stock_symbol set update_eod_quote = true where exchange_id in
   (select exchange_id from pick_exchange where symbol in ('FOREX', 'NYMEX', 'INDEX', 'CME', 'CFE', 'CBOT', 'KCBT', 'NYBOT'));

truncate table pick_eod_quote;


\dt pick*


update pick_stock_symbol set targeted = true where symbol_id in (
select distinct q.symbol_id
from pick_eod_quote q, pick_exchange e
where
q.exchange_id = e.exchange_id
and e.symbol in ('AMEX', 'OTCBB', 'NASDAQ', 'NYSE')
);

select * from pick_exchange;

select symbol, symbol_id from pick_stock_symbol where targeted = true and exchange_id = 21;


select * from pick_index_correlation;

truncate table pick_index_correlation;
truncate table pick_angle_quote_print;

select count(0) from pick_index_correlation where quote_dt between '2007-09-01' and '2007-09-10'
                                        and lookback = 124 and "offset" = 0;



select c.rms, c.symbol_id, s.name, s.symbol, idx.name, idx.symbol from pick_index_correlation c, pick_stock_symbol idx, pick_stock_symbol s
where c.index_symbol_id = idx.symbol_id
and c.symbol_id = s.symbol_id
order by c.rms desc
limit 10;



select count(0), exchange_id from pick_eod_quote
group by exchange_id;

update pick_eod_quote set create_dt = current_date - 3 where create_dt = current_date;


create index pick_eod_symid on pick_eod_quote (symbol_id);


select * from wm_stock_symbol where symbol = 'TWI';

select * from wm_ireport where symbol_id = 26697;

drop table wm_ireport_active;


select symbol_id, '|'||coalesce(value, '0')||'|' from wm_customer_holding where symbol_id = 19567 and delete_dt is null and value is not null;


select 'x' where '' is not null;

select sum(cast (case when value = '' then '0' else value end as numeric)) from wm_customer_holding where symbol_id = 19567 and delete_dt is null

alter table wm_ireport_active drop column earnings;
alter table wm_ireport_active add column earnings varchar(20) default '';

alter table wm_ireport_active add column user_created varchar(50);




select count(0) from (
select quote_id, exchange_id, symbol_id, quote_dt, open, high, low, close, 0.0, volume
                                from pick_eod_quote where
                                exchange_id = 21 and symbol_id = 25343 and quote_dt between '2011-02-01' and '2011-03-01'
                                order by quote_dt) x;

select count(0) from pick_eod_quote where symbol_id = 25343;

select count(0), s.name, s.symbol
from pick_stock_symbol s, pick_eod_quote eq , pick_exchange e
where s.symbol_id = eq.symbol_id
and e.exchange_id = s.exchange_id
and eq.exchange_id = e.exchange_id
and e.symbol in ('NASDAQ', 'NYSE')
group by s.name, s.symbol
order by count(0);




select * from cms_site;


delete  from cms_content;
delete  from cms_page;
delete  from cms_template;

select * from cms_site;


/** PICK **/
-- quotes today by exchange
select count(0), e.name
from pick_eod_quote q, pick_exchange e
where
e.exchange_id = q.exchange_id
and q.quote_dt = (select max(quote_dt) from pick_eod_quote)
group by e.name
order by e.name;

-- quotes yesterday by exchange
select count(0), e.name
from pick_eod_quote q, pick_exchange e
where
e.exchange_id = q.exchange_id
and q.quote_dt = (select max(quote_dt)-1 from pick_eod_quote)
group by e.name
order by e.name;








select max(delete_dt) from wm_ireport_active;
select max(target_hit_dt) from wm_ireport;


update wm_ireport set inactive_dt = null, target_hit_dt = null where inactive_dt > '2011-11-22' or target_hit_dt > '2011-11-22';
update wm_ireport_active set delete_dt = null where delete_dt = '2011-11-22';

alter table crm_discount add column code varchar(50);









Select count(0) from pick_eod_quote;

drop table pick_angle_quote_print;
drop table pick_index_correlation;

select count(0) from (
select quote_id, exchange_id, symbol_id, quote_dt, open, high, low, close, 0.0, volume
                            from pick_eod_quote where
                             symbol_id = 70336
                            order by quote_dt) x;

select * from pick_stock_symbol where symbol_id = 70336;


\d cms_content;

alter table crm_enterprise add column crm_style text;

select * from crm_enterprise;

delete from core_user where username = 'kwbedwell@hotmail.com';

alter table wm_ireport_active add column symbol_id integer;
update wm_ireport_active ia
set symbol_id = (select ir.symbol_id from wm_ireport ir where ir.ireport_id = ia.ireport_id);


select enterprise_id, name from crm_enterprise;

select count(0), cast(create_dt as date) from crm_oi_terms_acceptance group by cast(create_dt as date);


delete from crm_oi_terms_acceptance where create_dt > '2011-12-14';



 select v.name, sum(oi.unit_cost*oi.quantity) as cost,
                           sum(oi.unit_price*oi.quantity) as revenue,
                           sum((oi.unit_price*oi.quantity)-(oi.unit_cost*oi.quantity)) as profit
                    from
                    crm_customer_order o, crm_customer cust,
                    crm_order_item oi, crm_campaign cmp,
                    crm_company co, core_status cs, core_status_event cse, crm_product p,
                    crm_vendor v
                    where
                    o.customer_id = cust.customer_id and
                    o.order_id = oi.order_id and
                    o.campaign_id = cmp.campaign_id and
                    oi.product_id = p.product_id and
                    cmp.company_id = co.company_id and
                    co.enterprise_id = 5 and
                    o.delete_dt is null and
                    oi.delete_dt is null and
                    o.status_id = cs.status_id and
                    cs.event_id = cse.event_id and
                    extract(month from o.create_dt) = extract(month from current_date) and
                    extract(year from o.create_dt) = extract(year from current_date) and
                    p.vendor_id = v.vendor_id
                    group by v.name
                    order by sum(oi.unit_price*oi.quantity) desc;


explain select o.create_dt, sum(oi.unit_cost*oi.quantity) as cost,
                           sum(oi.unit_price*oi.quantity) as revenue,
                           sum((oi.unit_price*oi.quantity)-(oi.unit_cost*oi.quantity)) as profit
                    from
                    crm_customer_order o, crm_customer cust,
                    crm_order_item oi, crm_campaign cmp,
                    crm_company co, core_status cs, core_status_event cse, crm_product p
                    where
                    o.customer_id = cust.customer_id and
                    o.order_id = oi.order_id and
                    o.campaign_id = cmp.campaign_id and
                    oi.product_id = p.product_id and
                    cmp.company_id = co.company_id and
                    co.enterprise_id = 5 and
                    o.delete_dt is null and
                    oi.delete_dt is null and
                    o.status_id = cs.status_id and
                    cs.event_id = cse.event_id and
                    o.create_dt between current_date - 7 and current_date
                    group by o.create_dt
                    order by o.create_dt asc;

create index on crm_order_item (order_id);
create index on crm_customer_order (delete_dt);
create index on crm_customer_order (customer_id);
create index on crm_customer_order (campaign_id);
create index on crm_customer_order (create_dt);
create index on crm_customer_order (extract(month from create_dt), extract(year from create_dt));
create index on crm_company (enterprise_id);
create index on crm_campaign (company_id);
create index on crm_order_item (delete_dt);
create index on crm_customer_order (status_id);


select * from wm_ireport_view_log;



select * from wm_stock_symbol where symbol = 'VIX';

select * from wm_eod_quote where symbol_id = 22139 order by quote_dt;

select eq.* from wm_eod_quote eq, wm_stock_symbol ss, wm_exchange e where eq.symbol_id = ss.symbol_id and ss.exchange_id = e.exchange_id and ss.symbol = ' WWWW ' and e.symbol = ' NASDAQ ';





--


select src, extract(year from maturity_dt)||'-'||extract(month from maturity_dt) as "month",
            sum(case when res  = 'RIGHT' then 1 else 0 end) as "rights",
            sum(case when res  = 'WRONG' then 1 else 0 end) as "wrongs",
            round(cast(cast(sum(case when res  = 'RIGHT' then 1 else 0 end) as float)/cast(sum(1) as float) as numeric), 3) as "batting_avg",
            sum(case when tres = 'RIGHT' then 1 else 0 end) as "t_rights",
            sum(case when tres = 'WRONG' then 1 else 0 end) as "t_wrongs",
            round(cast(cast(sum(case when tres = 'RIGHT' then 1 else 0 end) as float)/cast(sum(1) as float) as numeric), 3) as "tbatting_avg",
            round(cast(avg(off_by)*100 as numeric), 2) as avg_off_by
from
(
    select maturity_dt, src, target, dir, open_quote, high_quote, low_quote, close_quote, prediction_id, symbol, exchange,
    case when ((high_quote >= target and dir = 'UP') or (low_quote <= target and dir = 'DOWN')) then 'RIGHT' else 'WRONG' end res,
    case when ((high_quote > open_quote and dir = 'UP') or (low_quote < open_quote and dir = 'DOWN')) then 'RIGHT' else 'WRONG' end tres,
    cast(abs(case when dir = 'UP' then target - high_quote else target - low_quote end) as float)/cast(target as float) as off_by
     from (
        select case when p.source = 'Earnings' then
                    p.source ||' '|| p.prediction_disposition
               else p.source end as "src", p.prediction_id,
               p.target, p.prediction_direction as "dir",
          (select eq.close from wm_eod_quote eq where eq.exchange_id = e.exchange_id
                                           and eq.symbol_id = ss.symbol_id
                                           and eq.quote_dt = p.create_dt limit 1) open_quote,
          (select eq.close from wm_eod_quote eq where eq.exchange_id = e.exchange_id
                                           and eq.symbol_id = ss.symbol_id
                                           and eq.quote_dt = p.maturity_dt limit 1) close_quote,
          (select max(eq.high) from wm_eod_quote eq where eq.exchange_id = e.exchange_id
                                           and eq.symbol_id = ss.symbol_id
                                           and eq.quote_dt between p.create_dt and p.maturity_dt limit 1) high_quote,
          (select min(eq.low) from wm_eod_quote eq where eq.exchange_id = e.exchange_id
                                           and eq.symbol_id = ss.symbol_id
                                           and eq.quote_dt between p.create_dt and p.maturity_dt limit 1) low_quote,
          ss.symbol, e.symbol as "exchange", p.create_dt, p.maturity_dt, p.event_dt
        from wm_prediction p, wm_stock_symbol ss, wm_exchange e
        where p.symbol_id = ss.symbol_id
        and ss.exchange_id = e.exchange_id
        and p.target is not null
        and p.target > 0
        and p.maturity_dt is not null
        and p.maturity_dt > '2011-10-01'
    ) as a where high_quote is not null and low_quote is not null and open_quote is not null and close_quote is not null
) as b
group by src, extract(year from maturity_dt)||'-'||extract(month from maturity_dt)
order by extract(year from maturity_dt)||'-'||extract(month from maturity_dt), src;


select c.email, ss.symbol, a.create_dt
from crm_oi_terms_acceptance a, crm_customer_order o, crm_order_item oi, crm_customer c, wm_ireport_view_log vl, wm_stock_symbol ss
 where a.create_dt between current_date -1 and current_date
and a.order_item_id = oi.order_item_id
and oi.order_id = o.order_id
and o.customer_id = c.customer_id
and vl.customer_id = c.customer_id
and ss.symbol_id = vl.symbol_id;

select * from crm_customer where email = 'kwbedwell@yahoo.com';


select eq.quote_dt, eq.open as "Open", eq.high as "High", eq.low as "Low", eq.close as "Close", eq.volume as "Volume", eq.close as "Adjusted"from wm_eod_quote eq, wm_stock_symbol ss, wm_exchange e where eq.symbol_id = ss.symbol_id and ss.exchange_id = e.exchange_id and eq.quote_dt between '2011-01-01' and '2011-09-31' and ss.symbol = 'SIRI' and e.symbol = 'NASDAQ';






select max(quote_dt) from wm_eod_quote;

select name, symbol from wm_stock_symbol where exchange_id = 60 and name like 'S &%' order by name;

select customer_id, email from crm_customer


create index wm_cust_email_campaign on crm_customer (lower(email), campaign_id);

select * from crm_enterprise where customer_id = 271382;


SELECT crm_enterprise.enterprise_id AS crm_enterprise_enterprise_id, crm_enterprise.name AS crm_enterprise_name, crm_enterprise.crm_style AS crm_enterprise_crm_style, crm_enterprise.customer_id AS crm_enterprise_customer_id, crm_enterprise.order_item_id AS crm_enterprise_order_item_id, crm_enterprise.terms_link AS crm_enterprise_terms_link, crm_enterprise.create_dt AS crm_enterprise_create_dt, crm_enterprise.delete_dt AS crm_enterprise_delete_dt
FROM crm_enterprise
WHERE crm_enterprise.customer_id = 271382 AND crm_enterprise.delete_dt IS NOT NULL
 LIMIT 1 OFFSET 0;


select username from core_user limit 1 offset 0;

select username from core_user where enterprise_id = 265069
and username = ;


select attr_name from core_attribute where attr_name like 'C%';

alter table crm_enterprise add column copyright varchar(200);

explain SELECT core_attribute.attr_id AS core_attribute_attr_id, core_attribute.fk_type AS core_attribute_fk_type, core_attribute.attr_name AS core_attribute_attr_name, core_attribute.attr_type AS core_attribute_attr_type
FROM core_attribute
WHERE core_attribute.fk_type = 'Customer' AND core_attribute.attr_name = 'Crd Number'
 LIMIT 1 OFFSET 0;


explain SELECT core_attribute_value.attr_value_id AS core_attribute_value_attr_value_id, core_attribute_value.attr_id AS core_attribute_value_attr_id, core_attribute_value.attr_value AS core_attribute_value_attr_value, core_attribute_value.fk_type AS core_attribute_value_fk_type, core_attribute_value.fk_id AS core_attribute_value_fk_id
FROM core_attribute_value
WHERE core_attribute_value.fk_type = 'Customer'
AND core_attribute_value.fk_id = 271382
AND core_attribute_value.attr_id = 56
 LIMIT 1 OFFSET 0;


create index cav_main on core_attribute_value (fk_type, fk_id, attr_id);

alter table core_status alter column create_dt type timestamp;


select * from core_status where fk_id = 530334;
\d crm_customer;


select ss.symbol, avg(eq.volume) as "AvgVolume"
from wm_stock_symbol ss, wm_exchange e, wm_eod_quote eq
where ss.exchange_id = e.exchange_id and e.symborl = 'NASDAQ' and eq.symbol_id = ss.symbol_id
and eq.quote_dt between current_date-60 and current_date
and ss.symbol != 'FTR'
group by ss.symbol_id, ss.symbol, ss.exchange_id, ss.name
order by avg(eq.volume) desc
limit 17;


select ss.symbol, avg(eq.volume) as "AvgVolume"
from wm_stock_symbol ss, wm_exchange e, wm_eod_quote eq
where ss.exchange_id = e.exchange_id and e.symbol = 'NASDAQ'
and eq.symbol_id = ss.symbol_id
and eq.quote_dt between '2009-01-01' and '2012-01-01'
and exists (select 1 from wm_eod_quote eq2 where eq2.symbol_id = eq.symbol_id and eq2.quote_dt < '2009-01-01')
group by ss.symbol_id, ss.symbol, ss.exchange_id, ss.name
order by avg(eq.volume) desc limit 50;

\d wm_ireport;

select count(0) from wm_ireport i, wm_stock_symbol ss, wm_exchange e
where i.symbol_id = ss.symbol_id
and ss.exchange_id = e.exchange_id
and ss.symbol = 'WXS'
and e.symbol = 'NYSE'
and i.create_dt = '2011-10-20';


, wm_ireport_prediction_join ipj

select distinct e.symbol||'.'||ss.symbol
from wm_ireport i, wm_stock_symbol ss, wm_exchange e
where i.symbol_id = ss.symbol_id
and ss.exchange_id = e.exchange_id
and i.create_dt > '2011-09-09'
and 2 <= (select count(0) from wm_prediction p, wm_ireport_prediction_join ipj
         where i.ireport_id = ipj.ireport_id
         and ipj.prediction_id = p.prediction_id and p.prediction_direction = 'UP');



select count(0)
from wm_ireport i, wm_stock_symbol ss, wm_exchange e
where i.symbol_id = ss.symbol_id
and ss.exchange_id = e.exchange_id
and 5 <= (select count(0) from wm_prediction p, wm_ireport_prediction_join ipj
         where i.ireport_id = ipj.ireport_id
         and ipj.prediction_id = p.prediction_id and p.prediction_direction = 'UP');


select count(0)
from wm_ireport i, wm_stock_symbol ss, wm_exchange e, wm_ireport_prediction_join ipj, wm_prediction p
where i.symbol_id = ss.symbol_id
                 and ss.exchange_id = e.exchange_id
                 and p.prediction_direction = 'UP'
                 and ipj.ireport_id = i.ireport_id
                 and ipj.prediction_id = p.prediction_id
                 and p.source in ('GATS', 'Group Correlation', 'PatternScan')
                 and ss.symbol = 'PEBO'
                 and e.symbol = 'NASDAQ'
                 and cast(i.create_dt as date) = '2011-10-21';

select * from crm_customer where email = 'kwbedwell@hotmail.com';

select * from wm_ireport where create_dt > '2012-01-31';

select max(create_dt) from wm_ireport;


select min(target), min(maturity_dt) from (
select i.ireport_id, p.source, p.target, p.vv, p.ve, p.maturity_dt, p.prediction_dt, p.updated_dt, p.event_dt
from wm_ireport i, wm_stock_symbol ss, wm_exchange e, wm_prediction p, wm_ireport_prediction_join pj
where i.symbol_id = ss.symbol_id
and ss.exchange_id = e.exchange_id
and ss.symbol = 'GDI'
and e.symbol = 'NYSE'
and pj.ireport_id = i.ireport_id
and pj.prediction_id = p.prediction_id
) x;

select e.symbol||'.'||ss.symbol as symbol, i.ireport_id, p.source, p.target, p.vv, p.ve, p.maturity_dt, p.event_dt
from wm_ireport i, wm_stock_symbol ss, wm_exchange e, wm_prediction p, wm_ireport_prediction_join pj
where i.symbol_id = ss.symbol_id
and ss.exchange_id = e.exchange_id
and i.create_dt > '2011-09-09'
and pj.ireport_id = i.ireport_id
and pj.prediction_id = p.prediction_id
and 5 = (select count(distinct p.source)
    from wm_prediction p, wm_ireport_prediction_join ipj
    where i.ireport_id = ipj.ireport_id
    and ipj.prediction_id = p.prediction_id
    and p.prediction_direction = 'UP') limit 2000
;


explain select e.symbol||'.'||ss.symbol as symbol, i.create_dt, i.ireport_id, p.source, p.target, p.vv, p.ve, p.maturity_dt, p.event_dt
    from wm_ireport i, wm_stock_symbol ss, wm_exchange e, wm_prediction p, wm_ireport_prediction_join pj
    where i.symbol_id = ss.symbol_id
    and ss.exchange_id = e.exchange_id
    and pj.ireport_id = i.ireport_id
    and pj.prediction_id = p.prediction_id
    and p.maturity_dt > '2011-09-09'
    and i.create_dt > '2011-09-09'
    and p.create_dt > '2011-09-09'
    and 5 = (select count(distinct px.source)
             from wm_prediction px, wm_ireport_prediction_join ipj
             where i.ireport_id = ipj.ireport_id
             and ipj.prediction_id = p.prediction_id
             and px.prediction_direction = 'UP')
    limit 2000;


select count(distinct p.source)
             from wm_prediction px, wm_ireport_prediction_join ipj
             where i.ireport_id = ipj.ireport_id
             and ipj.prediction_id = p.prediction_id
             and px.create_dt > '2011-09-09'
             and px.prediction_direction = 'UP';



select customer_id, email from crm_customer where campaign_id = 14;

select * from core_status_event where short_name = 'NOTE';

truncate table pvs_listing cascade;


insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system,
milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('Asset', 'ASSET_PROCESSED', 'ASSET_PROCESSED', false, false, true,
true, false, false, false, true, false);

insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system,
milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('Asset', 'ASSET_MOVED_NDN', 'ASSET_MOVED_NDN', false, false, true,
true, false, false, false, true, false);

insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system,
milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('Listing', 'CLOSED', 'CLOSED', false, false, true,
true, false, false, false, true, false);

insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system,
milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('ListingMessage', 'SEND_OK', 'SEND_OK', false, false, true,
false, false, false, false, false, false);

insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system,
milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('ListingMessage', 'SEND_FAIL', 'SEND_FAIL', false, false, true,
false, false, false, false, false, false);



select * from core_status where fk_type = 'Listing' and event_id = 29;

select * from core_asset where name = 'ab0b1cddf3f9d8a758fa6da76058291b.mp4';

select * from core_asset a, core_status s
where a.fk_type = 'Listing'
and a.status_id is null;

select * from core_status_event where short_name = 'ASSET_PROCESSED';

delete from core_status where event_id = 30;
select status_id from core_asset where id = 561;

select * from pvs_listing;


select a.name,a.id, a.create_dt from core_asset a order by a.create_dt;

select * from core_asset where id= 552;




select e.symbol||'.'||ss.symbol as symbol, p.prediction_id, i.create_dt, i.ireport_id, p.source, p.target, p.vv, p.ve, p.maturity_dt, p.event_dt
from wm_ireport i, wm_stock_symbol ss, wm_exchange e, wm_prediction p, wm_ireport_prediction_join pj
where i.symbol_id = ss.symbol_id
and ss.exchange_id = e.exchange_id
and i.create_dt > '2011-09-09'
and pj.ireport_id = i.ireport_id
and pj.prediction_id = p.prediction_id
and p.event_dt > '2011-09-09'
and ss.symbol = 'ANSS'
and 5 = (select count(distinct p.source)
    from wm_prediction p, wm_ireport_prediction_join ipj
    where i.ireport_id = ipj.ireport_id
    and ipj.prediction_id = p.prediction_id
    and p.prediction_direction = 'UP');


select p.prediction_id, p.event_dt, p.maturity_dt from
wm_prediction p, wm_ireport_prediction_join ipj
where ipj.ireport_id = 5991
and p.prediction_id = ipj.prediction_id;



select e.symbol||'.'||ss.symbol as symbol, p.prediction_id, i.create_dt, i.ireport_id, p.source, p.target, p.vv, p.ve, p.maturity_dt, p.event_dt
                                 from wm_ireport i, wm_stock_symbol ss, wm_exchange e, wm_prediction p, wm_ireport_prediction_join pj
                                 where i.symbol_id = ss.symbol_id
                                 and ss.exchange_id = e.exchange_id
                                 and i.create_dt > '2011-09-01'
                                 and pj.ireport_id = i.ireport_id
                                 and pj.prediction_id = p.prediction_id
                                 and (p.event_dt >= '2012-02-19' or p.maturity_dt >= '2012-02-19')
                                 and 5 <= (select count(distinct p.source)
                                           from wm_prediction p, wm_ireport_prediction_join ipj
                                           where i.ireport_id = ipj.ireport_id
                                           and ipj.prediction_id = p.prediction_id
                                           and p.prediction_direction = 'UP')
                                 order by p.event_dt asc;


select e.symbol||'.'||ss.symbol as symbol, p.event_dt, p.maturity_dt, p.prediction_id, i.create_dt, i.ireport_id, p.source, p.target, p.vv, p.ve
                                 from wm_ireport i, wm_stock_symbol ss, wm_exchange e, wm_prediction p, wm_ireport_prediction_join pj
                                 where i.symbol_id = ss.symbol_id
                                 and ss.exchange_id = e.exchange_id
                                 and i.create_dt > '2011-09-01'
                                 and pj.ireport_id = i.ireport_id
                                 and pj.prediction_id = p.prediction_id
                                 and (p.event_dt >= '2012-02-01' or p.maturity_dt >= '2012-02-01')
                                 and 4 <= (select count(distinct p.source)
                                           from wm_prediction p, wm_ireport_prediction_join ipj
                                           where i.ireport_id = ipj.ireport_id
                                           and ipj.prediction_id = p.prediction_id
                                           and p.prediction_direction = 'UP')
                                 order by p.event_dt asc;


select max(customer_id) from crm_customer;



select e.symbol||'.'||ss.symbol as symbol, p.prediction_direction, p.event_dt, p.maturity_dt, p.prediction_id, i.create_dt, i.ireport_id, p.source, p.target, p.vv, p.ve
from wm_ireport i, wm_stock_symbol ss, wm_exchange e, wm_prediction p, wm_ireport_prediction_join pj
where i.symbol_id = ss.symbol_id
and ss.exchange_id = e.exchange_id
and i.create_dt > '2011-09-09'
and pj.ireport_id = i.ireport_id
and pj.prediction_id = p.prediction_id
and p.event_dt > '2011-09-09'
and 4 = (select count(distinct px.source)
         from wm_prediction px, wm_ireport_prediction_join ipjx
         where i.ireport_id = ipjx.ireport_id
         and ipjx.prediction_id = px.prediction_id
         )
order by e.symbol||ss.symbol, p.event_dt, p.maturity_dt;




select symbol, ireport_id, max(target) as target, max(event_dt) as event_dt, max(maturity_dt) as maturity_dt
from (
select e.symbol||'.'||ss.symbol as symbol, i.create_dt, i.ireport_id, p.source, p.target, p.vv, p.ve, p.maturity_dt, p.event_dt
from wm_ireport i, wm_stock_symbol ss, wm_exchange e, wm_prediction p, wm_ireport_prediction_join pj
where i.symbol_id = ss.symbol_id
and ss.exchange_id = e.exchange_id
and i.create_dt > '2011-09-01'
and pj.ireport_id = i.ireport_id
and pj.prediction_id = p.prediction_id
and p.event_dt > '2011-09-01'
and 4 <= (select count(distinct p.source)
    from wm_prediction p, wm_ireport_prediction_join ipj
    where i.ireport_id = ipj.ireport_id
    and ipj.prediction_id = p.prediction_id
    )
) x group by symbol, ireport_id;





    select pix.symbol, pix.direction, pix.event_dt, pix.maturity_dt,
           pix.cumulative_st, pix.cl_before_event as pre_event_close, pix.cl_last as last_close,
           pix.avg_target, pix.min_target, pix.max_target,
           pix.symbol_id, pix.ireport_id,
           (select count(distinct pr.source) from wm_prediction pr, wm_ireport_prediction_join pj
                   where pr.prediction_id = pj.prediction_id
                   and pj.ireport_id = pix.ireport_id) as preds
    from (
        select o.symbol,
               case when o.direction = 'UP'   and o.cumulative_st < o.cl_last and o.cl_last < o.avg_target then 'YES'
                    when o.direction = 'DOWN' and o.cumulative_st > o.cl_last and o.cl_last > o.avg_target then 'YES'
                    else 'NO'
                    end as doit,
               o.symbol_id, o.ireport_id, o.direction, o.event_dt, o.maturity_dt,
               o.avg_target, o.min_target, o.max_target, o.cumulative_st, o.cl_before_event, o.cl_last
        from (
            select x.symbol, x.symbol_id, x.ireport_id, x.direction, x.event_dt, x.maturity_dt,
                   x.avg_target, x.min_target, x.max_target, x.cumulative_st,
                   (select eq_.close from wm_eod_quote eq_
                           where eq_.symbol_id = x.symbol_id
                           and eq_.quote_id = (select max(eq__.quote_id) from wm_eod_quote eq__ where eq__.quote_dt < x.event_dt and eq__.symbol_id = x.symbol_id)) cl_before_event,
                   (select eq_.close from wm_eod_quote eq_
                           where eq_.symbol_id = x.symbol_id
                           and eq_.quote_id = (select max(eq__.quote_id) from wm_eod_quote eq__ where eq__.symbol_id = x.symbol_id)) cl_last
            from (
                select e.symbol||'.'||ss.symbol as symbol, ss.symbol_id, i.ireport_id, max(p.prediction_direction) as direction,
                       min(p.event_dt) as event_dt, max(p.maturity_dt) as maturity_dt,
                       avg(p.target) as avg_target, min(target) as min_target, max(target) as max_target, avg(p.vv), avg(p.ve)
                    , max(str.cumulative_squeezetrigger) as cumulative_st
                from wm_ireport i, wm_stock_symbol ss, wm_exchange e, wm_prediction p, wm_ireport_prediction_join pj
                    , wm_squeeze_trigger_raw str
                where i.symbol_id = ss.symbol_id
                and ss.exchange_id = e.exchange_id
                and i.create_dt > '2011-09-01'
and i.ireport_id = 10511
                and pj.ireport_id = i.ireport_id
                and pj.prediction_id = p.prediction_id
                and p.event_dt between '2011-09-01' and '2012-04-01'
                and p.prediction_direction is not null
                and str.symbol_id = ss.symbol_id
                and '2011-01-01' > (select min(quote_dt) from wm_eod_quote eqx where eqx.symbol_id = ss.symbol_id)
                and 2 <= (select count(distinct p.source)
                    from wm_prediction p, wm_ireport_prediction_join ipj
                    where i.ireport_id = ipj.ireport_id
                    and ipj.prediction_id = p.prediction_id
                    )
                group by e.symbol||'.'||ss.symbol, ss.symbol_id, i.ireport_id
                order by e.symbol||'.'||ss.symbol
            ) x
        ) o
    ) pix
    where pix.doit = 'YES' and pix.event_dt > '2011-09-01';






    select pix.symbol, pix.direction, pix.event_dt, pix.maturity_dt,
           pix.cumulative_st, pix.cl_before_event as pre_event_close, pix.cl_last as last_close,
           pix.avg_target, pix.min_target, pix.max_target,
           pix.symbol_id, pix.ireport_id,
           (select count(distinct pr.source) from wm_prediction pr, wm_ireport_prediction_join pj
                   where pr.prediction_id = pj.prediction_id
                   and pj.ireport_id = pix.ireport_id) as preds
    from (
        select o.symbol,
               case when o.direction = 'UP'   and o.cumulative_st < o.cl_last and o.cl_last < o.avg_target then 'YES'
                    when o.direction = 'DOWN' and o.cumulative_st > o.cl_last and o.cl_last > o.avg_target then 'YES'
                    else 'NO'
                    end as doit,
               o.symbol_id, o.ireport_id, o.direction, o.event_dt, o.maturity_dt,
               o.avg_target, o.min_target, o.max_target, o.cumulative_st, o.cl_before_event, o.cl_last
        from (
            select x.symbol, x.symbol_id, x.ireport_id, x.direction, x.event_dt, x.maturity_dt,
                   x.avg_target, x.min_target, x.max_target, x.cumulative_st,
                   (select eq_.close from wm_eod_quote eq_
                           where eq_.symbol_id = x.symbol_id
                           and eq_.quote_id = (select max(eq__.quote_id) from wm_eod_quote eq__ where eq__.quote_dt < x.event_dt and eq__.symbol_id = x.symbol_id)) cl_before_event,
                   (select eq_.close from wm_eod_quote eq_
                           where eq_.symbol_id = x.symbol_id
                           and eq_.quote_id = (select max(eq__.quote_id) from wm_eod_quote eq__ where eq__.symbol_id = x.symbol_id)) cl_last
            from (
                select e.symbol||'.'||ss.symbol as symbol, ss.symbol_id, i.ireport_id, max(p.prediction_direction) as direction,
                       min(p.event_dt) as event_dt, max(p.maturity_dt) as maturity_dt,
                       avg(p.target) as avg_target, min(target) as min_target, max(target) as max_target, avg(p.vv), avg(p.ve)
                    , max(str.cumulative_squeezetrigger) as cumulative_st
                from wm_ireport i, wm_stock_symbol ss, wm_exchange e, wm_prediction p, wm_ireport_prediction_join pj
                    , wm_squeeze_trigger_raw str
                where i.symbol_id = ss.symbol_id
                and ss.exchange_id = e.exchange_id
                and i.create_dt > '2011-09-01'
                and pj.ireport_id = i.ireport_id
                and pj.prediction_id = p.prediction_id
                and p.event_dt > '2011-09-01' --and '2012-04-01'
                and p.prediction_direction is not null
                and str.symbol_id = ss.symbol_id
                and '2011-01-01' > (select min(quote_dt) from wm_eod_quote eqx where eqx.symbol_id = ss.symbol_id)
                and 1 <= (select count(distinct p.source)
                    from wm_prediction p, wm_ireport_prediction_join ipj
                    where i.ireport_id = ipj.ireport_id
                    and ipj.prediction_id = p.prediction_id
                    )
                group by e.symbol||'.'||ss.symbol, ss.symbol_id, i.ireport_id
                order by e.symbol||'.'||ss.symbol
            ) x
        ) o
    ) pix where pix.event_dt > '2012-04-01';


    --    select count(0), xx.event_dt from (
    select * FROM (
    select pix.symbol, pix.direction, pix.event_dt, pix.maturity_dt,
           pix.cumulative_st, pix.cl_before_event as pre_event_close, pix.cl_last as last_close,
           pix.avg_target, pix.min_target, pix.max_target,
           pix.symbol_id, pix.ireport_id,
           (select count(distinct pr.source) from wm_prediction pr, wm_ireport_prediction_join pj
                   where pr.prediction_id = pj.prediction_id
                   and pj.ireport_id = pix.ireport_id) as preds
    from (
        select o.symbol,
               case when o.direction = 'UP'
                         and o.cumulative_st < o.cl_last
                         and o.cl_before_event < o.avg_target
                         --                         and o.cl_before_event < o.avg_vv
                         --                         and o.cl_before_event < o.avg_ve
                         then 'YES'
                    when o.direction = 'DOWN'
                         and o.cumulative_st > o.cl_last
                         and o.cl_before_event > o.avg_target
                         --                         and o.cl_before_event > o.avg_vv
                         --                         and o.cl_before_event > o.avg_ve
                         then 'YES'
                    else 'NO'
                    end as doit,
               o.symbol_id, o.ireport_id, o.direction, o.event_dt, o.maturity_dt,
               o.avg_target, o.min_target, o.max_target, o.cumulative_st, o.cl_before_event, o.cl_last
        from (
            select x.symbol, x.symbol_id, x.ireport_id, x.direction, x.event_dt, x.maturity_dt,
                   x.avg_target, x.min_target, x.max_target, x.cumulative_st, x.avg_vv, x.avg_ve,
                   (select eq_.close from wm_eod_quote eq_
                           where eq_.symbol_id = x.symbol_id
                           and eq_.quote_id = (select max(eq__.quote_id) from wm_eod_quote eq__ where eq__.quote_dt < x.event_dt and eq__.symbol_id = x.symbol_id)) cl_before_event,
                   (select eq_.close from wm_eod_quote eq_
                           where eq_.symbol_id = x.symbol_id
                           and eq_.quote_id = (select max(eq__.quote_id) from wm_eod_quote eq__ where eq__.symbol_id = x.symbol_id)) cl_last
            from (
                select e.symbol||'.'||ss.symbol as symbol, ss.symbol_id, i.ireport_id, max(p.prediction_direction) as direction,
                       min(p.event_dt) as event_dt, max(p.maturity_dt) as maturity_dt,
                       avg(p.target) as avg_target, min(target) as min_target, max(target) as max_target,
                       avg(p.vv) as avg_vv, avg(p.ve) as avg_ve
                    , max(str.cumulative_squeezetrigger) as cumulative_st
                from wm_ireport i, wm_stock_symbol ss, wm_exchange e, wm_prediction p, wm_ireport_prediction_join pj
                    , wm_squeeze_trigger_raw str
                where i.symbol_id = ss.symbol_id
                and ss.exchange_id = e.exchange_id
--                and ss.symbol = 'KO'
                and i.create_dt > '2011-09-01'
                and pj.ireport_id = i.ireport_id
                and pj.prediction_id = p.prediction_id
                and p.event_dt between '2011-09-01' and '2012-04-17'
                and p.prediction_direction is not null
                and str.symbol_id = ss.symbol_id
                and '2011-01-01' > (select min(quote_dt) from wm_eod_quote eqx where eqx.symbol_id = ss.symbol_id)
                and 1 <= (select count(distinct p.source)
                    from wm_prediction p, wm_ireport_prediction_join ipj
                    where i.ireport_id = ipj.ireport_id
                    and ipj.prediction_id = p.prediction_id
                    )
                group by e.symbol||'.'||ss.symbol, ss.symbol_id, i.ireport_id
                order by e.symbol||'.'||ss.symbol
            ) x
        ) o
    ) pix
    where pix.doit = 'YES' and pix.event_dt > '2011-09-01' and pix.event_dt = '2012-04-04'
    ) xx
;
--    group by xx.event_dt
--    order by xx.event_dt;











select * from crm_enterprise;




alter table crm_communication add column enterprise_id integer;
alter table crm_communication add foreign key (enterprise_id) references crm_enterprise;
alter table crm_campaign add column default_url varchar(50);

alter table crm_communication drop column company_id;




SELECT crm_product.product_id AS crm_product_product_id
, crm_product.name AS crm_product_name
, crm_product.detail_description AS crm_product_detail_description
, crm_product.description AS crm_product_description
, crm_product.company_id AS crm_product_company_id
, crm_product.create_dt AS crm_product_create_dt
, crm_product.delete_dt AS crm_product_delete_dt
, crm_product.mod_dt AS crm_product_mod_dt
, crm_product.type AS crm_product_type
, crm_product.manufacturer AS crm_product_manufacturer
, crm_product.unit_cost AS crm_product_unit_cost
, crm_product.sku AS crm_product_sku
, crm_product.third_party_id AS crm_product_third_party_id
, crm_product.handling_price AS crm_product_handling_price
, crm_product.weight AS crm_product_weight
, crm_product.enabled AS crm_product_enabled
, crm_product.singleton AS crm_product_singleton
, crm_product.featured AS crm_product_featured
, crm_product.special AS crm_product_special
, crm_product.web_visible AS crm_product_web_visible
, crm_product.inventory_par AS crm_product_inventory_par
, crm_product.show_negative_inventory AS crm_product_show_negative_inventory
, crm_product.seo_title AS crm_product_seo_title
, crm_product.seo_keywords AS crm_product_seo_keywords
, crm_product.seo_description AS crm_product_seo_description
, crm_product.status_id AS crm_product_status_id
, crm_product.vendor_id AS crm_product_vendor_id
, crm_product.subscription AS crm_product_subscription
, crm_company_1.company_id AS crm_company_1_company_id
, crm_company_1.enterprise_id AS crm_company_1_enterprise_id
, crm_company_1.name AS crm_company_1_name
, crm_company_1.status_id AS crm_company_1_status_id
, crm_company_1.paypal_id AS crm_company_1_paypal_id
, crm_company_1.create_dt AS crm_company_1_create_dt
, crm_company_1.delete_dt AS crm_company_1_delete_dt
, crm_company_1.anon_customer_email AS crm_company_1_anon_customer_email
, crm_company_1.addr1 AS crm_company_1_addr1
, crm_company_1.addr2 AS crm_company_1_addr2
, crm_company_1.city AS crm_company_1_city
, crm_company_1.state AS crm_company_1_state
, crm_company_1.zip AS crm_company_1_zip
, crm_company_1.country AS crm_company_1_country
, crm_company_1.phone AS crm_company_1_phone
, crm_company_1.alt_phone AS crm_company_1_alt_phone
, crm_company_1.fax AS crm_company_1_fax
, crm_company_1.email AS crm_company_1_email
, crm_company_1.smtp_server AS crm_company_1_smtp_server
, crm_company_1.smtp_username AS crm_company_1_smtp_username
, crm_company_1.smtp_password AS crm_company_1_smtp_password
, crm_company_1.imap_server AS crm_company_1_imap_server
, crm_company_1.imap_username AS crm_company_1_imap_username
, crm_company_1.imap_password AS crm_company_1_imap_password
, crm_company_1.default_campaign_id AS crm_company_1_default_campaign_id
FROM crm_product JOIN crm_product_pricing ON crm_product_pricing.product_id = crm_product.product_id JOIN crm_company ON crm_product.company_id = crm_company.company_id LEFT OUTER JOIN crm_company AS crm_company_1 ON crm_company_1.company_id = crm_product.company_id
WHERE crm_product.delete_dt
 IS NULL AND crm_product.enabled = True AND crm_product.sku = 'FC-VID-001' AND crm_company.company_id = 11 AND crm_company.enterprise_id = 7 AND (crm_product.web_visible = True OR crm_product.web_visible = True) AND crm_product_pricing.delete_dt IS NULL
;


select * from crm_product where sku = 'FC-VID-001'
and enabled = True and company_id = 11 and web_visible = True
and delete_dt is null;

select * FROM CRM_CUSTOMER where email = 'info@faithchannelmedia.com';

select password from crm_customer where password is not null;


SELECT crm_customer.customer_id AS crm_customer_customer_id
, crm_customer.fname AS crm_customer_fname
, crm_customer.lname AS crm_customer_lname
, crm_customer.title AS crm_customer_title
, crm_customer.company_name AS crm_customer_company_name
, crm_customer.password AS crm_customer_password
, crm_customer.campaign_id AS crm_customer_campaign_id
, crm_customer.billing_id AS crm_customer_billing_id
, crm_customer.orig_campaign_id AS crm_customer_orig_campaign_id
, crm_customer.status_id AS crm_customer_status_id
, crm_customer.email AS crm_customer_email
, crm_customer.create_dt AS crm_customer_create_dt
, crm_customer.delete_dt AS crm_customer_delete_dt
, crm_customer.email_optout_dt AS crm_customer_email_optout_dt
, crm_customer.mod_dt AS crm_customer_mod_dt
, crm_customer.user_created AS crm_customer_user_created
, crm_customer.user_assigned AS crm_customer_user_assigned
, crm_customer.addr1 AS crm_customer_addr1
, crm_customer.addr2 AS crm_customer_addr2
, crm_customer.city AS crm_customer_city
, crm_customer.state AS crm_customer_state
, crm_customer.zip AS crm_customer_zip
, crm_customer.country AS crm_customer_country
, crm_customer.phone AS crm_customer_phone
, crm_customer.alt_phone AS crm_customer_alt_phone
, crm_customer.fax AS crm_customer_fax
, crm_customer.notes AS crm_customer_notes
, crm_customer.third_party_agent AS crm_customer_third_party_agent
, crm_customer.third_party_id AS crm_customer_third_party_id
, crm_customer.default_latitude AS crm_customer_default_latitude
, crm_customer.default_longitude AS crm_customer_default_longitude
, crm_customer.cid_0 AS crm_customer_cid_0
, crm_customer.cid_1 AS crm_customer_cid_1
, crm_customer.cid_2 AS crm_customer_cid_2
, crm_customer.cid_3 AS crm_customer_cid_3
, crm_customer.cid_4 AS crm_customer_cid_4
, crm_customer.cid_5 AS crm_customer_cid_5
, crm_customer.cid_6 AS crm_customer_cid_6
, crm_customer.cid_7 AS crm_customer_cid_7
, crm_customer.cid_8 AS crm_customer_cid_8
, crm_customer.cid_9 AS crm_customer_cid_9
, crm_customer.ref_0 AS crm_customer_ref_0
, crm_customer.ref_1 AS crm_customer_ref_1
, crm_customer.ref_2 AS crm_customer_ref_2
FROM crm_customer JOIN crm_campaign ON crm_campaign.campaign_id = crm_customer.campaign_id
WHERE crm_customer.delete_dt IS NULL AND crm_campaign.company_id = 12 AND crm_customer.email ILIKE 'info@faithchannelmedia.com' AND crm_customer.password = 'password'
 LIMIT 1;

select company_id, name from crm_campaign where campaign_id = 17;

select * from crm_company where company_id = 9;

alter table wm_ireport add column td_entry date;
alter table wm_ireport add column td_exit date;



alter table wm_ireport_alignment add column direction varchar(10);


select count(0) from wm_ireport_alignment;



select count(0) from crm_communication;


create index wm_ir_ali_find on wm_ireport_alignment (ireport_id, symbol_id, preds, delete_dt);


select count(0) from wm_prediction;

delete from wm_ireport_prediction_join where ireport_id in
(select i.ireport_id from wm_ireport_prediction_join ipj, wm_ireport i, wm_prediction p
where ipj.ireport_id = i.ireport_id
and ipj.prediction_id = p.prediction_id
and i.create_dt > date('2012-05-29'));


select count(0) from wm_ireport_prediction_join where ireport_id = 13235;



delete from wm_ireport_prediction_join where ireport_id = 13235;



truncate table wm_symbol_event;

select * from wm_exchange where symbol = 'NASDAQ';

select * from wm_stock_symbol where symbol = 'WWWW';


select se.name, se.event_dt, eq.quote_dt, eq.open, eq.high, eq.low, eq.close, eq.volume
from wm_symbol_event se, wm_eod_quote eq
where
se.symbol_id = 22139
and eq.exchange_id = 68
and eq.symbol_id = 22139
and eq.quote_dt between se.event_dt and se.event_dt + 5;


select source, event_dt, create_dt from wm_prediction where symbol_id = 22139 order by create_dt desc;


select e.symbol, s.symbol, min(q.close), max(q.close)
from wm_exchange e, wm_stock_symbol s, wm_eod_quote q
where
q.exchange_id in (68,72)
and s.exchange_id in (68,72)
and e.exchange_id = s.exchange_id
and q.exchange_id = e.exchange_id
and q.symbol_id = s.symbol_id
and q.quote_dt between '2007-01-01' and '2007-02-01'
and q.close between 3.5 and 7.5
and position('.' in s.symbol) = 0
group by e.symbol, s.symbol
limit 30;

select eq.quote_dt
, eq.open as "Open"
, eq.high as "High"
, eq.low as "Low"
, eq.close as "Close"
, eq.volume as "Volume"
, eq.close as "Adjusted"
from wm_eod_quote eq
, wm_stock_symbol ss
, wm_exchange e
where eq.symbol_id = ss.symbol_id
and ss.exchange_id = e.exchange_id
and eq.quote_dt between '2007-01-01'
and '2012-06-22'
and ss.symbol = 'HYI'
and e.symbol = 'NYSE';




select s.name, s.symbol from
wm_stock_symbol s, wm_exchange e
where e.symbol = 'INDEX'
and e.exchange_id = s.exchange_id
and s.name like 'S&P 500%'
order by s.symbol;



select e.quote_dt, e.quote_id, e.symbol_id, e.close
from wm_eod_quote e
where e.symbol_id = 35096
order by quote_dt desc
limit 30;


select count(0) from wm_ireport where notes like '%hit target%'
limit 10;

select count(0) from wm_ireport where notes like '%hit target%' and notes not like '%target = -1%';
select count(0) from wm_ireport where notes like '%target = -1%';
select count(0) from wm_ireport where notes like '%valuation conflict%' and notes not like '%target = -1%';
select count(0) from wm_ireport where notes like '%maturity date%';

select count(0) from wm_ireport;

select * from wm_ireport where notes like '%hit target%' and inactive_dt > current_date and notes not like '%target = -1%';



select p.target, p.target_orig
from wm_ireport i, wm_ireport_prediction_join ipj, wm_prediction p
where i.ireport_id = 13694
and ipj.ireport_id = i.ireport_id
and ipj.prediction_id = p.prediction_id;


select eq.*
                                                from wm_eod_quote eq, wm_stock_symbol ss
                                                where eq.symbol_id = ss.symbol_id
                                                and ss.symbol_id = 24111
                                                and eq.quote_dt between date '2011-07-19' and date '2012-08-03'
                                                order by eq.quote_dt asc;



select * from wm_ireport_alignment where ireport_id = 13837;


select * from wm_ireport_active where avg_vol is not null;


select description from pvs_listing where trim(both from description) = '"Our most saddening and sobering finding is the total disregard for the safety and welfare of Sandusky''s child victims.  The most powerful men at Penn State failed to take any steps for 14 years to protect the children who Sandusky victimized."  This accusation headlines the Penn State sexual abuse investigation that was made public yesterday.'
and keywords = 'Sandusky, Paterno, Penn State, Freeh, child, children, abuse, victims, scandal, Tyson, Teresa Guidice, New Jersey, culture, God, Jesus, Christ, Houston, Dallas, Chicago, Charlotte, Boston, New York, Seattle, commentary, Jim Denison, Denison Forum'
and title = 'Penn State: the death of truth';

select length(trim(both from title)) from pvs_listing where trim(both from title) like '%Hillary%';



select * from pvs_listing where trim(both from description) = trim(both from 'When Saul of Tarsus became a follower of Jesus, history changed forever.  When Martin Luther had his "tower experience" conversion, the Protestant Reformation resulted.  When C. S. Lewis left atheism for Christianity, our faith gained its most popular advocate of the 20th century.  Whose conversion would change history today?  This week I''d like to suggest five candidates and ask you to join me in praying every day for them to come to faith in Christ as their Lord.'
       and trim(both from keywords) = trim(both from 'Mohamed Morsi, Morsey, Egypt, Muslim Brotherhood, Muslim, Islam, Christian, Israel, Jewish, culture, God, Jesus, Christ, Houston, Dallas, Chicago, Charlotte, Boston, New York, Seattle, commentary, Jim Denison, Denison Forum')
                    and trim(both from title) = trim(both from '5 Conversions that would change history')
                    and company_id = 9 and delete_dt is null;


select length(trim(both from title)) from pvs_listing where
trim(both from title) = 'Tom Cruise and Katie Holmes divorce';


select * from crm_company where name = 'FaithChannel';

select email, password from crm_customer where campaign_id = 14;

update crm_customer set campaign_id = 17 where campaign_id = 14;


select * from crm_campaign where campaign_id = 17;

select max(campaign_id) from crm_campaign;

select * from crm_campaign where company_id = 9;

select l.listing_id, c.email, l.company_id, c.campaign_id
from pvs_listing l, core_asset a, crm_customer c
where a.fk_type = 'Listing'
and a.fk_id = l.listing_id
and l.customer_id = c.customer_id;


select * from pvs_listing where listing_id = 91;

select * from core_asset where fk_id = 91 and fk_type = 'Listing';


SELECT current_database() AS datname, nspname AS sname, relname AS tname,
  CASE WHEN v IS NULL THEN -1 ELSE round(extract(epoch FROM now()-v)) END AS ltime,
  CASE WHEN v IS NULL THEN '?' ELSE TO_CHAR(v, '$SHOWTIME') END AS ptime
FROM () AS foo;

SELECT nspname, relname, pg_stat_get_last_analyze_time(c.oid), pg_stat_get_last_autoanalyze_time(c.oid)
      FROM pg_class c, pg_namespace n
      WHERE relkind = 'r'
      AND n.oid = c.relnamespace
      AND n.nspname <> 'information_schema'
      and relname = 'pg_attribute'
      ORDER BY 3;



alter table cms_site add column;



select max(quote_id) from wm_eod_quote;

select quote_dt from wm_eod_quote where quote_id =  46283155;



select * from wm_ireport where ireport_id = 15260;


select * from wm_ireport where ireport_id = 15061;

select i.ireport_id, i.create_dt, p.create_dt, p.event_dt, p.type, p.source from wm_ireport_prediction_join ipj, wm_ireport i, wm_prediction p
where i.ireport_id in (15061,15332,15271,13826,15386)
and i.ireport_id = ipj.ireport_id
and ipj.prediction_id = p.prediction_id
order by i.ireport_id;






        select pix.create_dt, pix.symbol, pix.direction, pix.event_dt, pix.maturity_dt,
               pix.cumulative_st, pix.cl_before_event as pre_event_close, pix.cl_last as last_close,
               pix.avg_target, pix.min_target, pix.max_target,
               pix.symbol_id, pix.ireport_id,
               (select count(distinct pr.source) from wm_prediction pr, wm_ireport_prediction_join pj
                       where pr.prediction_id = pj.prediction_id
                       and pj.ireport_id = pix.ireport_id) as preds
        from (
            select o.symbol,
                   case when o.direction = 'UP'   and o.cumulative_st < o.cl_last and o.cl_last < o.avg_target then 'YES'
                        when o.direction = 'DOWN' and o.cumulative_st > o.cl_last and o.cl_last > o.avg_target then 'YES'
                        else 'NO'
                        end as doit,
                   o.symbol_id, o.ireport_id, o.direction, o.event_dt, o.maturity_dt,
                   o.avg_target, o.min_target, o.max_target, o.cumulative_st, o.cl_before_event, o.cl_last, o.create_dt
            from (
                select x.symbol, x.symbol_id, x.ireport_id, x.direction, x.event_dt, x.maturity_dt,
                       x.avg_target, x.min_target, x.max_target, x.cumulative_st,
                       (select eq_.close from wm_eod_quote eq_
                               where eq_.symbol_id = x.symbol_id
                               and eq_.quote_id = (select max(eq__.quote_id) from wm_eod_quote eq__ where eq__.quote_dt < x.event_dt and eq__.symbol_id = x.symbol_id)) cl_before_event,
                       (select eq_.close from wm_eod_quote eq_
                               where eq_.symbol_id = x.symbol_id
                               and eq_.quote_id = (select max(eq__.quote_id) from wm_eod_quote eq__ where eq__.symbol_id = x.symbol_id)) cl_last
                               ,x.create_dt
                from (
                    select e.symbol||'.'||ss.symbol as symbol, ss.symbol_id, i.ireport_id, max(p.prediction_direction) as direction,
                           max(p.event_dt) as event_dt, max(p.maturity_dt) as maturity_dt,
                           avg(p.target) as avg_target, min(target) as min_target, max(target) as max_target, avg(p.vv), avg(p.ve)
                        , max(str.cumulative_squeezetrigger) as cumulative_st, max(p.create_dt) as create_dt
                    from wm_ireport i, wm_stock_symbol ss, wm_exchange e, wm_prediction p, wm_ireport_prediction_join pj
                        , wm_squeeze_trigger_raw str
                    where i.symbol_id = ss.symbol_id
                    and ss.exchange_id = e.exchange_id
                    and i.create_dt > '2011-09-01'
                    and pj.ireport_id = i.ireport_id
                    and pj.prediction_id = p.prediction_id
                    and p.event_dt between '2011-09-01' and '2012-07-27'
                    and p.prediction_direction is not null
                    and str.symbol_id = ss.symbol_id
                    and '2011-01-01' > (select min(quote_dt) from wm_eod_quote eqx where eqx.symbol_id = ss.symbol_id)
                    and 1 <= (select count(distinct p.source)
                        from wm_prediction p, wm_ireport_prediction_join ipj
                        where i.ireport_id = ipj.ireport_id
                        and ipj.prediction_id = p.prediction_id
                        )
                    group by e.symbol||'.'||ss.symbol, ss.symbol_id, i.ireport_id
                    order by e.symbol||'.'||ss.symbol
                ) x
            ) o
        ) pix
        where pix.doit = 'YES' and pix.event_dt = '2012-07-27';



\d crm_product;


copy (
select p.product_id, p.name, p.manufacturer,
(select v.attr_value
    from core_attribute a, core_attribute_value v
    where a.attr_id = v.attr_id
    and a.fk_type = 'Product'
    and v.fk_type = 'Product'
    and a.attr_name = 'dose'
    and v.fk_id = p.product_id) as dose,
'<thumbnail-filename>' as thumbnail_filename,
'<front-large-filename>' as front_large_filename,
'<back-large-filename>' as back_large_filename
from crm_product p, crm_company c
where
p.company_id = c.company_id and
c.enterprise_id = 3
order by p.name
) to '/tmp/rpt.csv' with CSV;

\d crm_product;


\d core_attribute;
\d core_attribute_value;



select * from crm_enterprise;

select * from crm_campaign;

select name, company_id, enterprise_id from crm_company;

select * from core_user where username like 'xx%';
select * from crm_enterprise where name like 'Test%';



 select
     pg_stat_activity.datname,pg_class.relname,pg_locks.mode,substr(pg_stat_activity.current_query,1,50),
     age(now(),pg_stat_activity.query_start) as "age", pg_stat_activity.procpid
   from pg_stat_activity,pg_locks left
     outer join pg_class on (pg_locks.relation = pg_class.oid)
   where pg_locks.pid=pg_stat_activity.procpid order by query_start;


select sum(quantity) from crm_product_inventory_journal where product_id = 1451;

create index crm_prod_inv_jour_prod_id on crm_product_inventory_journal (product_id);

alter table crm_product add column inventory_cached integer default 0;

alter table crm_product drop column inventory_cached;


update crm_product set inventory = (select sum(quantity) from crm_product_inventory_journal ij where ij.product_id = product_id);

select p.product_id, p.inventory, (select sum(quantity) from crm_product_inventory_journal ij where ij.product_id = p.product_id)
from crm_product p
where p.delete_dt is null;



\copy (
select c.fname, c.lname, c.email, c.phone, cm.name, o.user_created, 'http://www.wealthmakers.com/crm/customer/edit/' || c.customer_id as "link"
from crm_product p, crm_order_item oi, crm_customer_order o, crm_customer c, crm_campaign cm
where p.sku = 'WM-PT2-001' and
p.product_id = oi.product_id and
oi.order_id = o.order_id and
o.customer_id = c.customer_id and
c.campaign_id = cm.campaign_id
 ) to '/tmp/rpt.csv' with csv header;

\d crm_customer_order;




select * from crm_customer where customer_id = 1077;


select cust.customer_id, cust.lname from
                                                 crm_customer cust, crm_campaign cam, crm_company com, crm_enterprise ent
                                                 where (lower(cust.lname) like '%b%' or cust.email = 'b')
                                                 and cust.delete_dt is null
                                                 and cust.campaign_id = cam.campaign_id
                                                 and cam.company_id = com.company_id
                                                 and com.enterprise_id = 3
                                                 order by cust.lname limit 10;



select TYPE, count(0) from crm_journal  group by type;



select p.product_id, p.name,
                p.unit_cost, pp.retail_price, pp.wholesale_price, pp.discount_price,
                cmp.campaign_id, pp.product_pricing_id
                from
                crm_product p, crm_company com, crm_enterprise ent, crm_campaign cmp, crm_product_pricing pp
                where lower(p.name) like '%%phar%%'
                and p.delete_dt is null
                and p.company_id = com.company_id
                and cmp.campaign_id = com.default_campaign_id
                and pp.campaign_id = cmp.campaign_id
                and pp.product_id = p.product_id
                and com.enterprise_id = 3
                order by p.name limit 15;

select * from crm_product_pricing where product_id = 1451;


SELECT core_status_event_1.display_name, core_status.create_dt
FROM core_status LEFT OUTER JOIN core_status_event AS core_status_event_1 ON core_status_event_1.event_id = core_status.event_id
WHERE core_status.customer_id = 220 ORDER BY core_status.status_id DESC;



insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system, milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('OrderItem', 'RETURN', 'Item Returned', false, false, true, false, false, false, false, true, false);


select cust.customer_id,
       o.create_dt, cust.email, o.order_id,
  sum(oi.unit_cost*oi.quantity) as "cost",
  (sum(oi.unit_price*oi.quantity)) as "item_revenue",
  (coalesce(o.shipping_total, 0)) as "shipping_revenue",
  (coalesce(o.handling_total, 0)) as "handling_revenue",
  (sum(oi.unit_price*oi.quantity)+coalesce(o.shipping_total,0)+coalesce(o.handling_total,0)) as "total_revenue",
  (sum((oi.unit_price-(oi.unit_price-oi.unit_discount_price))*oi.quantity)) as "discount",
  coalesce(  (select sum(coalesce(amount,0)) from crm_journal
     where order_id = o.order_id
    and type in ('CreditIncrease', 'Refund')), 0) as "refunds",
  coalesce(  (select sum(coalesce(amount,0)) from crm_journal
     where order_id = o.order_id
    and type in ('FullPayment', 'PartialPayment')), 0) as "payments",

  coalesce(  (sum(oi.unit_price*oi.quantity)+coalesce(o.shipping_total,0)+coalesce(o.handling_total,0))
    -coalesce((select sum(coalesce(amount,0)) from crm_journal
              where order_id = o.order_id
              and type in ('FullPayment', 'PartialPayment')), 0), 0) as "due",
  csx.display_name,
  CASE WHEN o.user_created is null THEN 'WEB'
            ELSE 'OFFICE'
       END as source
from
  crm_customer_order o, crm_customer cust,
  crm_order_item oi, crm_campaign cmp,
  crm_company co, core_status cs, core_status_event csx
where
o.customer_id = cust.customer_id and
o.order_id = oi.order_id and
o.campaign_id = cmp.campaign_id and
cmp.company_id = co.company_id and
co.enterprise_id = 3 and
o.delete_dt is null and
oi.delete_dt is null and
o.status_id = cs.status_id and
cs.event_id = csx.event_id and
  ('2012-01-08' is null or o.create_dt >= '2012-01-08') and
  ('2012-09-07' is null or o.create_dt <= '2012-09-07')
group by o.create_dt, cust.email,
  o.order_id, csx.display_name, cust.customer_id, o.user_created, o.shipping_total, o.handling_total;


select domain, domain_alias0, domain_alias1, domain_alias2
 from cms_site;



alter table crm_enterprise add column

alter table crm_enterprise add column     smtp_server varchar(50);
alter table crm_enterprise add column     smtp_username varchar(50);
alter table crm_enterprise add column     smtp_password varchar(50);
alter table crm_enterprise add column     imap_server varchar(50);
alter table crm_enterprise add column     imap_username varchar(50);
alter table crm_enterprise add column     imap_password varchar(50);
alter table crm_enterprise add column email varchar(50);


select * from crm_customer where email = 'amers_j@yahoo.com';

# index cache rate
SELECT
  sum(idx_blks_read) as idx_read,
  sum(idx_blks_hit)  as idx_hit,
  (sum(idx_blks_hit) - sum(idx_blks_read)) / sum(idx_blks_hit) as ratio
FROM
  pg_statio_user_indexes;

# index usage
SELECT
  relname,
  100 * idx_scan / (seq_scan + idx_scan) percent_of_times_index_used,
  n_live_tup rows_in_table
FROM
  pg_stat_user_tables
ORDER BY
  n_live_tup DESC;


# cache hit rate
SELECT
  sum(heap_blks_read) as heap_read,
  sum(heap_blks_hit)  as heap_hit,
  (sum(heap_blks_hit) - sum(heap_blks_read)) / sum(heap_blks_hit) as ratio
FROM
  pg_statio_user_tables;



insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system,
milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('Listing', 'APPROVED', 'APPROVED', false, false, true,
true, false, false, false, true, false);

insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system,
milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('Listing', 'DECLINED', 'DECLINED', false, false, true,
true, true, false, false, true, false);


insert into core_status_event
(event_type, short_name, display_name, claim, finalize, is_system,
milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values
('Listing', 'ASSET_PROCESSED', 'ASSET_PROCESSED', false, false, true,
false, false, false, false, true, false);


update core_status_event set event_type = 'Listing' where event_type = 'ASSET_PROCESSED';



select a.name, e.short_name, l.listing_id, l.title, l.status_id
from pvs_listing l, core_status s, core_status_event e, crm_company c, crm_enterprise ent, core_asset a
where l.status_id = s.status_id
and a.fk_type = 'Listing'
and a.fk_id = l.listing_id
and s.event_id = e.event_id
and l.company_id = c.company_id
and c.enterprise_id = ent.enterprise_id;


select * from core_status_event where short_name = 'ASSET_PROCESSED';



select e.short_name from
core_status_event e, core_status s, pvs_listing l
where l.status_id = s.status_id
and s.event_id = e.event_id
and l.listing_id = 96;

delete from core_status where status_id = (select max(status_id) from core_status);

select * from crm_enterprise;



select * from cms_site;

select * from crm_customer where email = 'unittest@test.com';


-- as postgres
alter table unittest owner to unittest;

create schema eyefoundit;

alter table cms_content                   set schema eyefoundit;
alter table cms_content_type              set schema eyefoundit;
alter table cms_page                      set schema eyefoundit;
alter table cms_site                      set schema eyefoundit;
alter table cms_template                  set schema eyefoundit;
alter table core_asset                    set schema eyefoundit;
alter table core_association              set schema eyefoundit;
alter table core_attribute                set schema eyefoundit;
alter table core_attribute_value          set schema eyefoundit;
alter table core_key_value                set schema eyefoundit;
alter table core_status                   set schema eyefoundit;
alter table core_status_event             set schema eyefoundit;
alter table core_status_event_reason      set schema eyefoundit;
alter table core_user                     set schema eyefoundit;
alter table core_user_priv                set schema eyefoundit;
alter table crm_appointment               set schema eyefoundit;
alter table crm_billing                   set schema eyefoundit;
alter table crm_billing_history           set schema eyefoundit;
alter table crm_campaign                  set schema eyefoundit;
alter table crm_communication             set schema eyefoundit;
alter table crm_company                   set schema eyefoundit;
alter table crm_customer                  set schema eyefoundit;
alter table crm_customer_order            set schema eyefoundit;
alter table crm_discount                  set schema eyefoundit;
alter table crm_enterprise                set schema eyefoundit;
alter table crm_journal                   set schema eyefoundit;
alter table crm_oi_terms_acceptance       set schema eyefoundit;
alter table crm_order_item                set schema eyefoundit;
alter table crm_product                   set schema eyefoundit;
alter table crm_product_category          set schema eyefoundit;
alter table crm_product_category_join     set schema eyefoundit;
alter table crm_product_child             set schema eyefoundit;
alter table crm_product_inventory_journal set schema eyefoundit;
alter table crm_product_pricing           set schema eyefoundit;
alter table crm_product_return            set schema eyefoundit;
alter table crm_purchase_order            set schema eyefoundit;
alter table crm_purchase_order_item       set schema eyefoundit;
alter table crm_report                    set schema eyefoundit;
alter table crm_report_company_join       set schema eyefoundit;
alter table crm_vendor                    set schema eyefoundit;
alter table pvs_listing                   set schema eyefoundit;
alter table pvs_listing_favorite          set schema eyefoundit;
alter table pvs_listing_message           set schema eyefoundit;


create table pvs_schema_map (
   schema_id serial not null,
   domain_name varchar(50) not null,
   schema_name varchar(50) not null,
   create_dt date DEFAULT now(),
   CONSTRAINT pvs_schema_map_pkey PRIMARY KEY (schema_id)
);

insert into pvs_schema_map (domain_name, schema_name) values ('eyefound.it', 'eyefoundit');

select is_generated from information_schema.columns where table_name = 'crm_customer' and column_name = 'customer_id';

        SELECT
            tc.constraint_name, tc.table_name, kcu.column_name,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name
        FROM
            information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name
        WHERE constraint_type = 'FOREIGN KEY' and ccu.table_name = 'crm_customer';



SELECT * FROM information_schema.tables WHERE table_schema = 'public';

select substring(fs_path from 54) from core_asset where fk_type = 'Listing';



select fs_path from core_asset where id = 626;

 update core_asset set fs_path = substring(fs_path from 25) where id in (628 ,629 ,630 );


alter table pvs_listing add column site_id integer;
alter table pvs_listing add foreign key (site_id) references cms_site;


select customer_id, company_id, site_id from pvs_listing;
select email from crm_customer where customer_id = 1010;



update pvs_listing set site_id = 13 where customer_id = 1078;

select * from cms_site;

select s.domain, c.name, substring(c.data from 0 for 100)
from cms_content c, cms_page p, cms_site s
where c.page_id = p.page_id
and p.site_id = s.site_id
and s.domain = 'wealthmakers.com';


select count(0) from crm_enterprise;

select * from crm_enterprise where enterprise_id < 50;



/****** porting fcm to eyefound.it **/
-- upload db from pvs02
-- zip up files under sites/6512bd43d9caa6e02c990b0a82652dca and copy tarball to sites/c51ce410c124a10e0db5e4b97fc2af39/
update crm_customer set campaign_id = 17 where campaign_id = 14;
update pvs_listing set site_id = 13 where customer_id = 1010;
-------- dont do this ------ update core_asset set fs_path = substring(fs_path from 54) where fk_type = 'Listing';
-- cd sites/c51ce410c124a10e0db5e4b97fc2af39/
-- find . -name "*.jpg" -exec rm -f {} \;
-- find . -name "*.png" -exec rm -f {} \;
update core_asset set status_id = null where fk_type = 'Listing';
-- python ../pvscore/pvscore/bin/uuidkey.py retail retail /Users/kbedwell/dev/pydev/pvs/storage
-- python -c 'from pvs.bin.eye_process import process_upload; process_upload()' -I development.ini
/****** end ********/




select
            t.relname as table_name,
            i.relname as index_name,
            array_to_string(array_agg(a.attname), ', ') as column_names
        from
            pg_class t,
            pg_class i,
            pg_index ix,
            pg_attribute a
        where
            t.oid = ix.indrelid
            and i.oid = ix.indexrelid
            and a.attrelid = t.oid
            and a.attnum = ANY(ix.indkey)
            and t.relkind = 'r'
            and t.relname = 'crm_customer_order'
            and i.relname not like '%_pkey'
        group by
            t.relname,
            i.relname
        order by
            t.relname,
            i.relname;


select count(0) from
            pg_class t,
            pg_class i,
            pg_index ix,
            pg_attribute a
        where
            t.oid = ix.indrelid
            and i.oid = ix.indexrelid
            and a.attrelid = t.oid
            and a.attnum = ANY(ix.indkey)
            and t.relkind = 'r'
            and t.relname = 'crm_customer_order'
            and i.relname = '%_pkey'
        group by
            t.relname,
            i.relname
        order by
            t.relname,
            i.relname;

-- round 1
alter table crm_customer add foreign key (status_id) references core_status;
alter table core_attribute_value add foreign key (attr_id) references core_attribute;
alter table crm_appointment add foreign key (user_assigned) references core_user;
alter table crm_campaign add foreign key (comm_forgot_password_id) references crm_communication;
alter table crm_customer_order add foreign key (status_id) references core_status;
alter table crm_order_item add foreign key (status_id) references core_status;
alter table crm_journal add foreign key (order_id) references crm_customer_order;

-- round 2
delete from core_status where status_id in (select status_id from core_status where customer_id is not null and customer_id not in (select customer_id from crm_customer));
alter table core_status add foreign key (customer_id) references crm_customer;





select * from crm_campaign;


select * from core_asset;

select distinct fk_type from core_asset;

select fk_type, fk_id, name, web_path
from core_asset where fk_type = 'Product'
limit 10;


select l.listing_id, l.company_id, c.enterprise_id
from pvs_listing l, crm_company c
where l.company_id = c.company_id;


/*alter table core_asset add column extension varchar(10);
#alter table core_asset add column enterprise_id uuid;
#alter table core_asset add foreign key (enterprise_id) references crm_enterprise;
*/

select customer_id, email, password from crm_customer where email like '%denison%';

select * from pvs_listing where listing_id = 'fdb2f3f5-2f9f-4d07-81ec-035d7c2bf971';
select * from core_asset where fk_id = 'fdb2f3f5-2f9f-4d07-81ec-035d7c2bf971';


\d crm_customer;

select table_name, column_name, data_type from information_schema.columns where data_type = 'date';

alter table core_asset add column extension varchar(10);
alter table core_asset add column enterprise_id uuid;
alter table core_asset add foreign key (enterprise_id) references crm_enterprise;


select count(0) from wm_eod_quote;

delete from wm_eod_quote where quote_dt < '2012-06-01';



select count(0) from crm_customer;

\d core_user;

\d cms_content;


alter table cms_site add column config_json text;


update crm_company set default_campaign_id = null where company_id = '9';
delete from crm_campaign where company_id = '9';




select cust.customer_id,
                                            cust.lname || ', ' || cust.fname as "name"
                                                 from crm_customer cust, crm_campaign cam, crm_company com, crm_enterprise ent
                                                 where (lower(cust.lname) like '%%{l}%%' or cust.email = '{l}')
                                                 and cust.delete_dt is null
                                                 and cust.campaign_id = cam.campaign_id
                                                 and cam.company_id = com.company_id

                                                 and com.enterprise_id = '{ent_id}'
                                                 order by cust.lname, cust.fname limit {lim}



select cust.customer_id,
                                            cust.lname || ', ' || cust.fname as "name", cam.campaign_id
                                                 from crm_customer cust, crm_campaign cam, crm_company com, crm_enterprise ent
                                                 where (lower(cust.lname) like '%%cob%%' or cust.email = 'cob')
                                                 and cust.delete_dt is null
                                                 and cust.campaign_id = cam.campaign_id
                                                 and cam.company_id = com.company_id
                                                 and com.enterprise_id = '8b012e41-ee87-4109-b0d5-d392be9f515a'
                                                 order by cust.lname, cust.fname limit 10;




--
-- create a smaller version of wm
--
delete from wm_eod_quote where quote_dt < '2012-06-01';
create index idx_customer_status on core_status (customer_id);
create index idx_holding_customer on wm_customer_holding (customer_id);
-- python pvscore/bin/delete_customers.py wm wm "where customer_id > 5000"


explain delete from core_status where customer_id = '40';
select count(0) from core_status;



delete from core_asset where status_id in (select status_id from core_status where customer_id > 1000) ;
delete from crm_billing_history where customer_id > 1000;
delete from crm_product_inventory_journal where return_id in (select return_id from crm_product_return where journal_id in (select journal_id from crm_journal where customer_id > 1000)) ;
delete from crm_product_return where journal_id in (select journal_id from crm_journal where customer_id > 1000) ;
delete from crm_journal where customer_id > 1000 ;
delete from crm_product_inventory_journal where order_item_id in (select order_item_id from crm_order_item where order_id in (select order_id from crm_customer_order where customer_id > 1000 ));
delete from crm_oi_terms_acceptance where order_id in (select order_id from crm_customer_order where customer_id > 1000);
delete from wm_ireport_order where order_id in (select order_id from crm_customer_order where customer_id > 1000) ;
--delete from pvs_listing where customer_id > 1000 ;
update crm_customer set status_id = null where customer_id > 1000 ;
delete from crm_billing_history where customer_id > 1000 ;
delete from wm_portfolio where customer_id > 1000 ;
delete from wm_ireport_view_log where customer_id > 1000 ;
delete from wm_customer_holding where customer_id > 1000 ;
delete from crm_order_item where order_id in (select order_id from crm_customer_order where customer_id > 1000) ;
delete from crm_customer_order where customer_id > 1000 ;
delete from core_status where customer_id > 1000 ;
delete from crm_billing where billing_id in (select billing_id from crm_customer where customer_id > 1000);




#    billing_ids = get_ids(cur, "select billing_id from crm_customer where customer_id = '%s'" % customer_id)
#    doit(conn, cur, "delete from crm_customer where customer_id = '%s'" % customer_id)
#    for bill_id in billing_ids:
#        if bill_id:
#            doit(conn, cur, "delete from crm_billing where billing_id = '%s'" % bill_id)


delete from crm_order_item where order_id in (select order_id from crm_customer_order where customer_id > 1000) ;

\d crm_customer_order;


select product_id, name, delete_dt from crm_product order by product_id desc;

select count(0) from crm_order_item where product_id = 1668;



delete from crm_order_item where product_id = 1668;








select count(0), p.name, p.product_id
from crm_customer c, crm_customer_order co, crm_order_item oi, crm_product p
where
c.customer_id = co.customer_id
and co.order_id = oi.order_id
and oi.product_id = p.product_id
group by p.name, p.product_id
;

------------------------

-- create a table of customers we care about based on product_id
drop table if exists tmp_keepers;
create table tmp_keepers as
select c.customer_id, c.email, c.billing_id, oi.order_id, oi.order_item_id, oi.product_id
from crm_customer c, crm_customer_order co, crm_order_item oi, crm_product p
where
c.customer_id = co.customer_id
and co.order_id = oi.order_id
and oi.product_id = p.product_id
and p.product_id in (1670);

drop table if exists tmp_status_keepers;
create table tmp_status_keepers
as select s.status_id
from core_status s, tmp_keepers tk
where s.customer_id = tk.customer_id;

insert into tmp_status_keepers select x.status_id
from crm_billing  x, tmp_keepers tk
where x.status_id is not null
and tk.billing_id = x.billing_id;

insert into tmp_status_keepers select x.status_id
from crm_company  x
where x.status_id is not null;

insert into tmp_status_keepers select x.status_id
from crm_customer_order  x, tmp_keepers tk
where x.status_id is not null
and tk.customer_id = x.customer_id;

insert into tmp_status_keepers select x.status_id
from crm_customer  x, tmp_keepers tk
where x.status_id is not null
and tk.customer_id = x.customer_id;

insert into tmp_status_keepers select x.status_id
from crm_order_item  x, tmp_keepers tk
where x.status_id is not null
and x.order_item_id = tk.order_item_id;

insert into tmp_status_keepers select x.status_id
from crm_product  x
where x.status_id is not null
and x.product_id in (select distinct(product_id) from tmp_keepers);

insert into tmp_status_keepers select x.status_id
from crm_purchase_order_item  x
where x.status_id is not null;

insert into tmp_status_keepers select x.status_id
from crm_purchase_order  x
where x.status_id is not null;

insert into tmp_status_keepers select x.status_id
from wm_ireport  x
where x.status_id is not null;

update crm_customer set billing_id = null;

copy (select c.* from crm_customer c
where c.customer_id in (select distinct customer_id from tmp_keepers)) to '/tmp/crm_customer.copy';

copy (select co.* from crm_customer_order co
where co.order_id in (select distinct order_id from tmp_keepers)) to '/tmp/crm_customer_order.copy';

copy (select oi.* from crm_order_item oi
where oi.order_item_id in (select distinct order_item_id from tmp_keepers)) to '/tmp/crm_order_item.copy';

copy (select j.* from crm_journal j
where j.order_id in (select distinct order_id from tmp_keepers)) to '/tmp/crm_journal.copy';

copy (select av.* from core_attribute_value av
where av.fk_type != 'Customer' or (av.fk_type = 'Customer' and av.fk_id in (select customer_id from tmp_keepers))) to '/tmp/core_attribute_value.copy';

copy (select distinct s.* from core_status s
where s.status_id in (select distinct status_id from tmp_status_keepers)) to '/tmp/core_status.copy';

copy (select p.* from wm_portfolio p
where p.customer_id in (select distinct customer_id from tmp_keepers)) to '/tmp/wm_portfolio.copy';


copy crm_company to '/tmp/crm_company.copy';
copy crm_campaign to '/tmp/crm_campaign.copy';
copy crm_communication to '/tmp/crm_communication.copy';
copy crm_product to '/tmp/crm_product.copy';
copy crm_product_category to '/tmp/crm_product_category.copy';
copy crm_product_category_join to '/tmp/crm_product_category_join.copy';
copy crm_product_child to '/tmp/crm_product_child.copy';
copy crm_product_pricing to '/tmp/crm_product_pricing.copy';
copy crm_report to '/tmp/crm_report.copy';


truncate table core_attribute_value cascade;
truncate table crm_customer cascade;  --
truncate table crm_customer_order cascade;
truncate table crm_order_item cascade;
truncate table crm_journal cascade;
truncate table core_status cascade;
truncate table crm_appointment;
truncate table core_asset;
truncate table wm_ireport_order;
truncate table wm_customer_holding;
truncate table wm_ireport_view_log;
truncate table crm_product_inventory_journal;
truncate table crm_oi_terms_acceptance;
delete from core_user_priv where priv_id not in (select distinct priv_id from core_user where priv_id is not null);


alter table crm_company drop constraint crm_company_default_campaign_id_fkey;
copy crm_company from '/tmp/crm_company.copy';
copy crm_communication from '/tmp/crm_communication.copy';
copy crm_campaign from '/tmp/crm_campaign.copy';
copy crm_customer from '/tmp/crm_customer.copy';
alter table crm_company add constraint crm_company_default_campaign_id_fkey FOREIGN KEY (default_campaign_id) REFERENCES crm_campaign(campaign_id);
copy crm_product from '/tmp/crm_product.copy';
copy crm_product_category from '/tmp/crm_product_category.copy';
copy crm_product_category_join from '/tmp/crm_product_category_join.copy';
copy crm_product_child from '/tmp/crm_product_child.copy';
copy crm_product_pricing from '/tmp/crm_product_pricing.copy';
copy crm_report from '/tmp/crm_report.copy';
copy core_status from '/tmp/core_status.copy';
copy crm_customer_order from '/tmp/crm_customer_order.copy';
copy crm_order_item from '/tmp/crm_order_item.copy';
copy crm_journal from '/tmp/crm_journal.copy';
copy core_attribute_value from '/tmp/core_attribute_value.copy';
copy wm_portfolio from '/tmp/wm_portfolio.copy';

-- select constraint_name, table_name from information_schema.table_constraints where constraint_name like '%fkey1';
alter table crm_customer drop constraint crm_customer_status_id_fkey1;
alter table crm_journal drop constraint crm_journal_order_id_fkey1;

drop table tmp_keepers;
drop table tmp_status_keepers;


-------------------------------------------------------------------



-- highest revenue categories
explain select x.* from
(select pc.name, pc.category_id
,sum(oi.quantity) as quantity
,sum(oi.unit_price*oi.quantity) as revenue
,sum(oi.unit_cost*oi.quantity) as cost
,sum((oi.unit_price*oi.quantity)-(oi.unit_cost*oi.quantity)) as profit
from
crm_customer_order o, crm_customer cust, crm_order_item oi, crm_campaign cmp, crm_product p,
crm_product_category pc, crm_product_category_join pcj
where
o.customer_id = cust.customer_id and
o.order_id = oi.order_id and
o.campaign_id = cmp.campaign_id and
cmp.campaign_id = '1fe1dc5d-1f9e-4f90-b711-db59c09009b1' and
oi.product_id = p.product_id and
p.product_id = pcj.product_id and
pcj.category_id = pc.category_id and
o.delete_dt is null and
oi.delete_dt is null
group by pc.name, pc.category_id
order by sum(oi.unit_price*oi.quantity) desc
) x order by revenue;


-- specials

select campaign_id, customer_id, email from crm_customer where email = 'kenneth.bedwell@gmail.com' and password = 'pass2';
select * from crm_campaign where campaign_id = 'c7b7ec79-3974-4927-bceb-83443f0add68';
select * from crm_company where company_id = '42d5ce7b-f5be-43fe-80b9-56a013b9314a';





SELECT anon_1.crm_customer_customer_id AS anon_1_crm_customer_customer_id
, anon_1.crm_customer_campaign_id AS anon_1_crm_customer_campaign_id
, anon_1.crm_customer_billing_id AS anon_1_crm_customer_billing_id
, anon_1.crm_customer_status_id AS anon_1_crm_customer_status_id
, anon_1.crm_customer_user_created AS anon_1_crm_customer_user_created
, anon_1.crm_customer_user_assigned AS anon_1_crm_customer_user_assigned
, anon_1.crm_customer_fname AS anon_1_crm_customer_fname
, anon_1.crm_customer_lname AS anon_1_crm_customer_lname
, anon_1.crm_customer_title AS anon_1_crm_customer_title
, anon_1.crm_customer_company_name AS anon_1_crm_customer_company_name
, anon_1.crm_customer_password AS anon_1_crm_customer_password
, anon_1.crm_customer_orig_campaign_id AS anon_1_crm_customer_orig_campaign_id
, anon_1.crm_customer_email AS anon_1_crm_customer_email
, anon_1.crm_customer_delete_dt AS anon_1_crm_customer_delete_dt
, anon_1.crm_customer_email_optout_dt AS anon_1_crm_customer_email_optout_dt
, anon_1.crm_customer_create_dt AS anon_1_crm_customer_create_dt
, anon_1.crm_customer_mod_dt AS anon_1_crm_customer_mod_dt
, anon_1.crm_customer_addr1 AS anon_1_crm_customer_addr1
, anon_1.crm_customer_addr2 AS anon_1_crm_customer_addr2
, anon_1.crm_customer_city AS anon_1_crm_customer_city
, anon_1.crm_customer_state AS anon_1_crm_customer_state
, anon_1.crm_customer_zip AS anon_1_crm_customer_zip
, anon_1.crm_customer_country AS anon_1_crm_customer_country
, anon_1.crm_customer_phone AS anon_1_crm_customer_phone
, anon_1.crm_customer_alt_phone AS anon_1_crm_customer_alt_phone
, anon_1.crm_customer_fax AS anon_1_crm_customer_fax
, anon_1.crm_customer_notes AS anon_1_crm_customer_notes
, anon_1.crm_customer_third_party_agent AS anon_1_crm_customer_third_party_agent
, anon_1.crm_customer_third_party_id AS anon_1_crm_customer_third_party_id
, anon_1.crm_customer_default_latitude AS anon_1_crm_customer_default_latitude
, anon_1.crm_customer_default_longitude AS anon_1_crm_customer_default_longitude
, anon_1.crm_customer_cid_0 AS anon_1_crm_customer_cid_0
, anon_1.crm_customer_cid_1 AS anon_1_crm_customer_cid_1
, anon_1.crm_customer_cid_2 AS anon_1_crm_customer_cid_2
, anon_1.crm_customer_cid_3 AS anon_1_crm_customer_cid_3
, anon_1.crm_customer_cid_4 AS anon_1_crm_customer_cid_4
, anon_1.crm_customer_cid_5 AS anon_1_crm_customer_cid_5
, anon_1.crm_customer_cid_6 AS anon_1_crm_customer_cid_6
, anon_1.crm_customer_cid_7 AS anon_1_crm_customer_cid_7
, anon_1.crm_customer_cid_8 AS anon_1_crm_customer_cid_8
, anon_1.crm_customer_cid_9 AS anon_1_crm_customer_cid_9
, anon_1.crm_customer_ref_0 AS anon_1_crm_customer_ref_0
, anon_1.crm_customer_ref_1 AS anon_1_crm_customer_ref_1
, anon_1.crm_customer_ref_2 AS anon_1_crm_customer_ref_2
, core_status_event_1.event_id AS core_status_event_1_event_id
, core_status_event_1.enterprise_id AS core_status_event_1_enterprise_id
, core_status_event_1.event_type AS core_status_event_1_event_type
, core_status_event_1.short_name AS core_status_event_1_short_name
, core_status_event_1.display_name AS core_status_event_1_display_name
, core_status_event_1.phase AS core_status_event_1_phase
, core_status_event_1.create_dt AS core_status_event_1_create_dt
, core_status_event_1.end_dt AS core_status_event_1_end_dt
, core_status_event_1.claim AS core_status_event_1_claim
, core_status_event_1.finalize AS core_status_event_1_finalize
, core_status_event_1.is_system AS core_status_event_1_is_system
, core_status_event_1.milestone_complete AS core_status_event_1_milestone_complete
, core_status_event_1.note_req AS core_status_event_1_note_req
, core_status_event_1.dashboard AS core_status_event_1_dashboard
, core_status_event_1.reason_req AS core_status_event_1_reason_req
, core_status_event_1.change_status AS core_status_event_1_change_status
, core_status_event_1.touch AS core_status_event_1_touch
, core_status_event_1.position AS core_status_event_1_position
, core_status_event_1.color AS core_status_event_1_color
, core_status_1.status_id AS core_status_1_status_id
, core_status_1.event_id AS core_status_1_event_id
, core_status_1.username AS core_status_1_username
, core_status_1.customer_id AS core_status_1_customer_id
, core_status_1.fk_type AS core_status_1_fk_type
, core_status_1.fk_id AS core_status_1_fk_id
, core_status_1.note AS core_status_1_note
, core_status_1.create_dt AS core_status_1_create_dt
, crm_enterprise_1.enterprise_id AS crm_enterprise_1_enterprise_id
, crm_enterprise_1.name AS crm_enterprise_1_name
, crm_enterprise_1.crm_style AS crm_enterprise_1_crm_style
, crm_enterprise_1.customer_id AS crm_enterprise_1_customer_id
, crm_enterprise_1.order_item_id AS crm_enterprise_1_order_item_id
, crm_enterprise_1.terms_link AS crm_enterprise_1_terms_link
, crm_enterprise_1.copyright AS crm_enterprise_1_copyright
, crm_enterprise_1.logo_path AS crm_enterprise_1_logo_path
, crm_enterprise_1.logo_path_pdf AS crm_enterprise_1_logo_path_pdf
, crm_enterprise_1.support_email AS crm_enterprise_1_support_email
, crm_enterprise_1.support_phone AS crm_enterprise_1_support_phone
, crm_enterprise_1.create_dt AS crm_enterprise_1_create_dt
, crm_enterprise_1.delete_dt AS crm_enterprise_1_delete_dt
, crm_enterprise_1.billing_method AS crm_enterprise_1_billing_method
, crm_enterprise_1.email AS crm_enterprise_1_email
, crm_enterprise_1.smtp_server AS crm_enterprise_1_smtp_server
, crm_enterprise_1.smtp_username AS crm_enterprise_1_smtp_username
, crm_enterprise_1.smtp_password AS crm_enterprise_1_smtp_password
, crm_enterprise_1.imap_server AS crm_enterprise_1_imap_server
, crm_enterprise_1.imap_username AS crm_enterprise_1_imap_username
, crm_enterprise_1.imap_password AS crm_enterprise_1_imap_password
, crm_company_1.company_id AS crm_company_1_company_id
, crm_company_1.enterprise_id AS crm_company_1_enterprise_id
, crm_company_1.status_id AS crm_company_1_status_id
, crm_company_1.default_campaign_id AS crm_company_1_default_campaign_id
, crm_company_1.name AS crm_company_1_name
, crm_company_1.paypal_id AS crm_company_1_paypal_id
, crm_company_1.create_dt AS crm_company_1_create_dt
, crm_company_1.delete_dt AS crm_company_1_delete_dt
, crm_company_1.anon_customer_email AS crm_company_1_anon_customer_email
, crm_company_1.addr1 AS crm_company_1_addr1
, crm_company_1.addr2 AS crm_company_1_addr2
, crm_company_1.city AS crm_company_1_city
, crm_company_1.state AS crm_company_1_state
, crm_company_1.zip AS crm_company_1_zip
, crm_company_1.country AS crm_company_1_country
, crm_company_1.phone AS crm_company_1_phone
, crm_company_1.alt_phone AS crm_company_1_alt_phone
, crm_company_1.fax AS crm_company_1_fax
, crm_company_1.email AS crm_company_1_email
, crm_company_1.smtp_server AS crm_company_1_smtp_server
, crm_company_1.smtp_username AS crm_company_1_smtp_username
, crm_company_1.smtp_password AS crm_company_1_smtp_password
, crm_company_1.imap_server AS crm_company_1_imap_server
, crm_company_1.imap_username AS crm_company_1_imap_username
, crm_company_1.imap_password AS crm_company_1_imap_password
, crm_product_pricing_1.product_pricing_id AS crm_product_pricing_1_product_pricing_id
, crm_product_pricing_1.campaign_id AS crm_product_pricing_1_campaign_id
, crm_product_pricing_1.product_id AS crm_product_pricing_1_product_id
, crm_product_pricing_1.wholesale_price AS crm_product_pricing_1_wholesale_price
, crm_product_pricing_1.retail_price AS crm_product_pricing_1_retail_price
, crm_product_pricing_1.discount_price AS crm_product_pricing_1_discount_price
, crm_product_pricing_1.bill_method_type AS crm_product_pricing_1_bill_method_type
, crm_product_pricing_1.bill_freq_type AS crm_product_pricing_1_bill_freq_type
, crm_product_pricing_1.create_dt AS crm_product_pricing_1_create_dt
, crm_product_pricing_1.delete_dt AS crm_product_pricing_1_delete_dt
, crm_product_1.product_id AS crm_product_1_product_id
, crm_product_1.company_id AS crm_product_1_company_id
, crm_product_1.status_id AS crm_product_1_status_id
, crm_product_1.vendor_id AS crm_product_1_vendor_id
, crm_product_1.name AS crm_product_1_name
, crm_product_1.detail_description AS crm_product_1_detail_description
, crm_product_1.description AS crm_product_1_description
, crm_product_1.create_dt AS crm_product_1_create_dt
, crm_product_1.delete_dt AS crm_product_1_delete_dt
, crm_product_1.mod_dt AS crm_product_1_mod_dt
, crm_product_1.type AS crm_product_1_type
, crm_product_1.manufacturer AS crm_product_1_manufacturer
, crm_product_1.unit_cost AS crm_product_1_unit_cost
, crm_product_1.sku AS crm_product_1_sku
, crm_product_1.third_party_id AS crm_product_1_third_party_id
, crm_product_1.handling_price AS crm_product_1_handling_price
, crm_product_1.weight AS crm_product_1_weight
, crm_product_1.enabled AS crm_product_1_enabled
, crm_product_1.singleton AS crm_product_1_singleton
, crm_product_1.featured AS crm_product_1_featured
, crm_product_1.special AS crm_product_1_special
, crm_product_1.web_visible AS crm_product_1_web_visible
, crm_product_1.inventory_par AS crm_product_1_inventory_par
, crm_product_1.show_negative_inventory AS crm_product_1_show_negative_inventory
, crm_product_1.seo_title AS crm_product_1_seo_title
, crm_product_1.seo_keywords AS crm_product_1_seo_keywords
, crm_product_1.seo_description AS crm_product_1_seo_description
, crm_product_1.subscription AS crm_product_1_subscription
, crm_product_1.inventory AS crm_product_1_inventory
, crm_order_item_1.order_item_id AS crm_order_item_1_order_item_id
, crm_order_item_1.order_id AS crm_order_item_1_order_id
, crm_order_item_1.status_id AS crm_order_item_1_status_id
, crm_order_item_1.user_created AS crm_order_item_1_user_created
, crm_order_item_1.product_id AS crm_order_item_1_product_id
, crm_order_item_1.parent_id AS crm_order_item_1_parent_id
, crm_order_item_1.name AS crm_order_item_1_name
, crm_order_item_1.unit_cost AS crm_order_item_1_unit_cost
, crm_order_item_1.unit_price AS crm_order_item_1_unit_price
, crm_order_item_1.unit_discount_price AS crm_order_item_1_unit_discount_price
, crm_order_item_1.unit_retail_price AS crm_order_item_1_unit_retail_price
, crm_order_item_1.create_dt AS crm_order_item_1_create_dt
, crm_order_item_1.delete_dt AS crm_order_item_1_delete_dt
, crm_order_item_1.quantity AS crm_order_item_1_quantity
, crm_order_item_1.tax AS crm_order_item_1_tax
, crm_journal_1.journal_id AS crm_journal_1_journal_id
, crm_journal_1.customer_id AS crm_journal_1_customer_id
, crm_journal_1.order_id AS crm_journal_1_order_id
, crm_journal_1.user_created AS crm_journal_1_user_created
, crm_journal_1.create_dt AS crm_journal_1_create_dt
, crm_journal_1.delete_dt AS crm_journal_1_delete_dt
, crm_journal_1.type AS crm_journal_1_type
, crm_journal_1.note AS crm_journal_1_note
, crm_journal_1.method AS crm_journal_1_method
, crm_journal_1.amount AS crm_journal_1_amount
, crm_customer_order_1.order_id AS crm_customer_order_1_order_id
, crm_customer_order_1.customer_id AS crm_customer_order_1_customer_id
, crm_customer_order_1.campaign_id AS crm_customer_order_1_campaign_id
, crm_customer_order_1.status_id AS crm_customer_order_1_status_id
, crm_customer_order_1.user_created AS crm_customer_order_1_user_created
, crm_customer_order_1.create_dt AS crm_customer_order_1_create_dt
, crm_customer_order_1.delete_dt AS crm_customer_order_1_delete_dt
, crm_customer_order_1.cancel_dt AS crm_customer_order_1_cancel_dt
, crm_customer_order_1.note AS crm_customer_order_1_note
, crm_customer_order_1.shipping_note AS crm_customer_order_1_shipping_note
, crm_customer_order_1.shipping_total AS crm_customer_order_1_shipping_total
, crm_customer_order_1.handling_note AS crm_customer_order_1_handling_note
, crm_customer_order_1.handling_total AS crm_customer_order_1_handling_total
, crm_customer_order_1.external_cart_id AS crm_customer_order_1_external_cart_id
, crm_enterprise_2.enterprise_id AS crm_enterprise_2_enterprise_id
, crm_enterprise_2.name AS crm_enterprise_2_name
, crm_enterprise_2.crm_style AS crm_enterprise_2_crm_style
, crm_enterprise_2.customer_id AS crm_enterprise_2_customer_id
, crm_enterprise_2.order_item_id AS crm_enterprise_2_order_item_id
, crm_enterprise_2.terms_link AS crm_enterprise_2_terms_link
, crm_enterprise_2.copyright AS crm_enterprise_2_copyright
, crm_enterprise_2.logo_path AS crm_enterprise_2_logo_path
, crm_enterprise_2.logo_path_pdf AS crm_enterprise_2_logo_path_pdf
, crm_enterprise_2.support_email AS crm_enterprise_2_support_email
, crm_enterprise_2.support_phone AS crm_enterprise_2_support_phone
, crm_enterprise_2.create_dt AS crm_enterprise_2_create_dt
, crm_enterprise_2.delete_dt AS crm_enterprise_2_delete_dt
, crm_enterprise_2.billing_method AS crm_enterprise_2_billing_method
, crm_enterprise_2.email AS crm_enterprise_2_email
, crm_enterprise_2.smtp_server AS crm_enterprise_2_smtp_server
, crm_enterprise_2.smtp_username AS crm_enterprise_2_smtp_username
, crm_enterprise_2.smtp_password AS crm_enterprise_2_smtp_password
, crm_enterprise_2.imap_server AS crm_enterprise_2_imap_server
, crm_enterprise_2.imap_username AS crm_enterprise_2_imap_username
, crm_enterprise_2.imap_password AS crm_enterprise_2_imap_password
, crm_company_2.company_id AS crm_company_2_company_id
, crm_company_2.enterprise_id AS crm_company_2_enterprise_id
, crm_company_2.status_id AS crm_company_2_status_id
, crm_company_2.default_campaign_id AS crm_company_2_default_campaign_id
, crm_company_2.name AS crm_company_2_name
, crm_company_2.paypal_id AS crm_company_2_paypal_id
, crm_company_2.create_dt AS crm_company_2_create_dt
, crm_company_2.delete_dt AS crm_company_2_delete_dt
, crm_company_2.anon_customer_email AS crm_company_2_anon_customer_email
, crm_company_2.addr1 AS crm_company_2_addr1
, crm_company_2.addr2 AS crm_company_2_addr2
, crm_company_2.city AS crm_company_2_city
, crm_company_2.state AS crm_company_2_state
, crm_company_2.zip AS crm_company_2_zip
, crm_company_2.country AS crm_company_2_country
, crm_company_2.phone AS crm_company_2_phone
, crm_company_2.alt_phone AS crm_company_2_alt_phone
, crm_company_2.fax AS crm_company_2_fax
, crm_company_2.email AS crm_company_2_email
, crm_company_2.smtp_server AS crm_company_2_smtp_server
, crm_company_2.smtp_username AS crm_company_2_smtp_username
, crm_company_2.smtp_password AS crm_company_2_smtp_password
, crm_company_2.imap_server AS crm_company_2_imap_server
, crm_company_2.imap_username AS crm_company_2_imap_username
, crm_company_2.imap_password AS crm_company_2_imap_password
, crm_campaign_1.campaign_id AS crm_campaign_1_campaign_id
, crm_campaign_1.company_id AS crm_campaign_1_company_id
, crm_campaign_1.comm_post_purchase_id AS crm_campaign_1_comm_post_purchase_id
, crm_campaign_1.comm_post_cancel_id AS crm_campaign_1_comm_post_cancel_id
, crm_campaign_1.comm_packing_slip_id AS crm_campaign_1_comm_packing_slip_id
, crm_campaign_1.comm_forgot_password_id AS crm_campaign_1_comm_forgot_password_id
, crm_campaign_1.name AS crm_campaign_1_name
, crm_campaign_1.create_dt AS crm_campaign_1_create_dt
, crm_campaign_1.delete_dt AS crm_campaign_1_delete_dt
, crm_campaign_1.type AS crm_campaign_1_type
, crm_campaign_1.default_url AS crm_campaign_1_default_url
, crm_campaign_1.tax_rate AS crm_campaign_1_tax_rate
, crm_campaign_1.email AS crm_campaign_1_email
, crm_campaign_1.smtp_server AS crm_campaign_1_smtp_server
, crm_campaign_1.smtp_username AS crm_campaign_1_smtp_username
, crm_campaign_1.smtp_password AS crm_campaign_1_smtp_password
, crm_campaign_1.imap_server AS crm_campaign_1_imap_server
, crm_campaign_1.imap_username AS crm_campaign_1_imap_username
, crm_campaign_1.imap_password AS crm_campaign_1_imap_password
, crm_billing_1.billing_id AS crm_billing_1_billing_id
, crm_billing_1.status_id AS crm_billing_1_status_id
, crm_billing_1.user_created AS crm_billing_1_user_created
, crm_billing_1.note AS crm_billing_1_note
, crm_billing_1.type AS crm_billing_1_type
, crm_billing_1.account_holder AS crm_billing_1_account_holder
, crm_billing_1.account_addr AS crm_billing_1_account_addr
, crm_billing_1.account_city AS crm_billing_1_account_city
, crm_billing_1.account_state AS crm_billing_1_account_state
, crm_billing_1.account_country AS crm_billing_1_account_country
, crm_billing_1.account_zip AS crm_billing_1_account_zip
, crm_billing_1.third_party_id AS crm_billing_1_third_party_id
, crm_billing_1.cc_token AS crm_billing_1_cc_token
, crm_billing_1.cc_last_4 AS crm_billing_1_cc_last_4
, crm_billing_1.cc_exp AS crm_billing_1_cc_exp
, crm_billing_1.is_primary AS crm_billing_1_is_primary
, crm_billing_1.create_dt AS crm_billing_1_create_dt
, crm_billing_1.delete_dt AS crm_billing_1_delete_dt
FROM (SELECT crm_customer.customer_id AS crm_customer_customer_id
, crm_customer.campaign_id AS crm_customer_campaign_id
, crm_customer.billing_id AS crm_customer_billing_id
, crm_customer.status_id AS crm_customer_status_id
, crm_customer.user_created AS crm_customer_user_created
, crm_customer.user_assigned AS crm_customer_user_assigned
, crm_customer.fname AS crm_customer_fname
, crm_customer.lname AS crm_customer_lname
, crm_customer.title AS crm_customer_title
, crm_customer.company_name AS crm_customer_company_name
, crm_customer.password AS crm_customer_password
, crm_customer.orig_campaign_id AS crm_customer_orig_campaign_id
, crm_customer.email AS crm_customer_email
, crm_customer.delete_dt AS crm_customer_delete_dt
, crm_customer.email_optout_dt AS crm_customer_email_optout_dt
, crm_customer.create_dt AS crm_customer_create_dt
, crm_customer.mod_dt AS crm_customer_mod_dt
, crm_customer.addr1 AS crm_customer_addr1
, crm_customer.addr2 AS crm_customer_addr2
, crm_customer.city AS crm_customer_city
, crm_customer.state AS crm_customer_state
, crm_customer.zip AS crm_customer_zip
, crm_customer.country AS crm_customer_country
, crm_customer.phone AS crm_customer_phone
, crm_customer.alt_phone AS crm_customer_alt_phone
, crm_customer.fax AS crm_customer_fax
, crm_customer.notes AS crm_customer_notes
, crm_customer.third_party_agent AS crm_customer_third_party_agent
, crm_customer.third_party_id AS crm_customer_third_party_id
, crm_customer.default_latitude AS crm_customer_default_latitude
, crm_customer.default_longitude AS crm_customer_default_longitude
, crm_customer.cid_0 AS crm_customer_cid_0
, crm_customer.cid_1 AS crm_customer_cid_1
, crm_customer.cid_2 AS crm_customer_cid_2
, crm_customer.cid_3 AS crm_customer_cid_3
, crm_customer.cid_4 AS crm_customer_cid_4
, crm_customer.cid_5 AS crm_customer_cid_5
, crm_customer.cid_6 AS crm_customer_cid_6
, crm_customer.cid_7 AS crm_customer_cid_7
, crm_customer.cid_8 AS crm_customer_cid_8
, crm_customer.cid_9 AS crm_customer_cid_9
, crm_customer.ref_0 AS crm_customer_ref_0
, crm_customer.ref_1 AS crm_customer_ref_1
, crm_customer.ref_2 AS crm_customer_ref_2
FROM crm_customer JOIN crm_campaign ON crm_campaign.campaign_id = crm_customer.campaign_id
WHERE crm_customer.delete_dt IS NULL AND crm_campaign.company_id = '42d5ce7b-f5be-43fe-80b9-56a013b9314a' AND crm_customer.email ILIKE 'kenneth.bedwell@gmail.com' AND crm_customer.password = 'pass2'
 LIMIT 1 AS anon_1 LEFT OUTER JOIN crm_customer_order AS crm_customer_order_1 ON anon_1.crm_customer_customer_id = crm_customer_order_1.customer_id LEFT OUTER JOIN core_status AS core_status_1 ON core_status_1.status_id = crm_customer_order_1.status_id LEFT OUTER JOIN core_status_event AS core_status_event_1 ON core_status_event_1.event_id = core_status_1.event_id LEFT OUTER JOIN crm_order_item AS crm_order_item_1 ON crm_customer_order_1.order_id = crm_order_item_1.order_id LEFT OUTER JOIN crm_product AS crm_product_1 ON crm_product_1.product_id = crm_order_item_1.product_id LEFT OUTER JOIN crm_company AS crm_company_1 ON crm_company_1.company_id = crm_product_1.company_id LEFT OUTER JOIN crm_enterprise AS crm_enterprise_1 ON crm_enterprise_1.enterprise_id = crm_company_1.enterprise_id LEFT OUTER JOIN crm_product_pricing AS crm_product_pricing_1 ON crm_product_1.product_id = crm_product_pricing_1.product_id LEFT OUTER JOIN crm_journal AS crm_journal_1 ON crm_customer_order_1.order_id = crm_journal_1.order_id LEFT OUTER JOIN crm_campaign AS crm_campaign_1 ON crm_campaign_1.campaign_id = anon_1.crm_customer_campaign_id LEFT OUTER JOIN crm_company AS crm_company_2 ON crm_company_2.company_id = crm_campaign_1.company_id LEFT OUTER JOIN crm_enterprise AS crm_enterprise_2 ON crm_enterprise_2.enterprise_id = crm_company_2.enterprise_id LEFT OUTER JOIN crm_billing AS crm_billing_1 ON crm_billing_1.billing_id = anon_1.crm_customer_billing_id ORDER BY crm_customer_order_1.create_dt DESC
, crm_order_item_1.create_dt ASC
, crm_journal_1.journal_id ASC;


2012-11-25 15:35:30,395 INFO  [sqlalchemy.engine.base.Engine][Dummy-4] {'password_1': u'pass2', 'email_1': u'kenneth.bedwell@gmail.com
', 'company_id_1': , 'param_1': 1}




select c.status_id, c.email, c.customer_id, c.user_created
from crm_customer c, crm_campaign cmp, crm_company comp, crm_order_item oi, crm_customer_order co
where c.email = 'kenneth.bedwell@gmail.com'
and c.password = 'pass2'
and c.campaign_id = cmp.campaign_id
and cmp.company_id = comp.company_id
and comp.company_id = '42d5ce7b-f5be-43fe-80b9-56a013b9314a'
and co.customer_id = c.customer_id
and oi.order_id = co.order_id;


select count(0) cnt
                               from crm_customer c, crm_campaign cmp, crm_company comp
                               where c.email = 'kenneth.bedwell@gmail.com'
                               and c.password = 'pass2'
                               and c.campaign_id = cmp.campaign_id
                               and cmp.company_id = comp.company_id
                               and comp.company_id = '42d5ce7b-f5be-43fe-80b9-56a013b9314a';


select count(0) cnt
                               from crm_customer c
                               where c.email = 'kenneth.bedwell@gmail.com'
                               and c.password = 'pass2';


select * from crm_company where company_id = '42d5ce7b-f5be-43fe-80b9-56a013b9314a';





alter table crm_order_item add column third_party_id varchar(100);
alter table crm_customer_order add column third_party_id varchar(100);


select count(0) cnt
                               from crm_customer c, crm_campaign cmp, crm_company comp
                               where c.email = %(email)s
                               and c.password = %(pwd)s
                               and c.campaign_id = cmp.campaign_id
                               and cmp.company_id = comp.company_id
                               and comp.company_id = %(company_id)s
2012-12-03 13:40:47,636 INFO  [sqlalchemy.engine.base.Engine][Dummy-4] {'pwd': u'no1nose', 'email':
 u'kyle.hewlett@raymondjames.com', 'company_id': UUID('acdeb7bf-1256-47cb-a5f8-065455c167d8')}



select ir.create_dt, ir.ireport_id
from wm_ireport ir , wm_ireport_active ira
where ir.create_dt > '2012-12-04'
and ir.ireport_id = ira.ireport_id
and ira.delete_dt is null;


select * from wm_stock_symbol where symbol = 'XRTX';



select prediction_id, symbol_id, create_dt from wm_prediction where symbol_id = 22162 order by create_dt desc;
select ireport_id, create_dt from wm_ireport where symbol_id = 22162;
select * from wm_ireport_prediction_join where ireport_id = 20001;


delete from wm_ireport_prediction_join where prediction_id in (select prediction_id from wm_prediction where create_dt > '2012-12-17');
delete from wm_ireport_prediction_join where ireport_id in (select ireport_id from wm_ireport where create_dt > '2012-12-17');
delete from wm_ireport_active where ireport_id in (select ireport_id from wm_ireport where create_dt > '2012-12-17');
delete from wm_ireport_alignment where ireport_id in (select ireport_id from wm_ireport where create_dt > '2012-12-17');
delete from wm_ireport where create_dt > '2012-12-17';
delete from wm_prediction where create_dt > '2012-12-17';


alter table cms_site add column eyefoundit_analytics_id varchar(50);


--
-- customer phase install.
--
alter table core_user drop column default_timezone;
alter table crm_customer drop column phase_id;
alter table crm_appointment drop column timezone;
drop table crm_customer_phase;

create table crm_customer_phase (
    phase_id uuid primary key,
    enterprise_id uuid,
    short_name varchar(20) not null,
    display_name varchar(20) not null,
    description text,
    sort_order int default 0,
    create_dt timestamp default now(),
    delete_dt timestamp,
    color varchar(20)
);
alter table crm_customer_phase add foreign key (enterprise_id) references crm_enterprise;
alter table crm_customer add column phase_id uuid;
alter table crm_customer add foreign key (phase_id) references crm_customer_phase;
alter table crm_appointment add column timezone varchar(100);
alter table core_user drop column tz_offset;
alter table core_user add column default_timezone varchar(100);

-- insert Suspect
-- insert Prospect
-- insert Lead
-- insert Opportunity
-- insert Customer

-- python setup.py develop   # in pvscore




select e.* from
wm_earnings_date e, wm_stock_symbol ss
where e.symbol_id = ss.symbol_id
and ss.symbol = 'WWWW'
;




select ed.earnings_dt, ed.symbol_id
from wm_earnings_date ed, wm_stock_symbol ss
where ed.symbol_id = ss.symbol_id
and ss.symbol = 'WWWW'
and ed.earnings_dt > '2007-01-01'
order by ed.earnings_dt asc;



select ed.earnings_dt, ed.symbol_id
from wm_earnings_performance ed, wm_stock_symbol ss
where ed.symbol_id = ss.symbol_id
and ss.symbol = 'WWWW'
order by ed.earnings_dt asc;




select count(0), ed.symbol_id
from wm_earnings_date ed, wm_stock_symbol ss, wm_earnings_performance ep
where ed.symbol_id = ss.symbol_id
and ss.symbol = 'WWWW'
and ep.symbol_id = ed.symbol_id
and ep.earnings_dt between ed.earnings_dt - interval '3 days' and ed.earnings_dt + interval '3 days'
group by ed.symbol_id;


select count(distinct ed.symbol_id)
from wm_earnings_date ed, wm_stock_symbol ss
where ed.symbol_id = ss.symbol_id;

--
-- wm earnings and events mods
--

drop table wm_earnings_performance;
drop table wm_earnings_date;
drop table wm_economic_event;

create table wm_earnings_performance (
    performance_id uuid primary key,
    symbol_id integer not null,
    exchange_id integer not null,
    earnings_dt date not null,
    actual float,
    expected float,
    previous float,
    create_dt timestamp default now()
);

create table wm_earnings_date (
    earnings_date_id uuid primary key,
    symbol_id integer not null,
    exchange_id integer not null,
    earnings_dt date not null,
    create_dt timestamp default now()
);

create table wm_economic_event (
    economic_event_id uuid primary key,
    name  varchar(100) not null,
    for_period varchar(20),
    actual varchar(20),
    forecast varchar(20),
    consensus varchar(20),
    prior varchar(20),
    revised_from varchar(20),
    event_dt date not null,
    create_dt timestamp default now()
);


--
-- end wm earnings
--

select symbol_id from wm_stock_symbol where symbol in
select * from wm_exchange where symbol in ('NASDAQ', 'NYSE');

explain select avg(volume) from wm_eod_quote where symbol_id = 22139;


explain
select ss.symbol, qt.create_dt, avg(volume)
over (partition by qt.quote_dt)
from
wm_eod_quote qt,
wm_stock_symbol ss,
wm_exchange ex
where ex.symbol in ('NASDAQ', 'NYSE')
and ss.symbol in ('MSFT')
and ex.exchange_id = ss.exchange_id
and qt.symbol_id = ss.symbol_id
and qt.quote_dt between '2012-01-01' and '2012-02-01';


select symbol_id, symbol, name from wm_stock_symbol where symbol = 'WWWW';



select company_id, enterprise_id, name from crm_company;

select name from crm_product where company_id = '7e03f6f2-465d-4eb4-a611-7ff5a5ad19dd';


alter table crm_product add column url varchar(100);

select e.name, c.email
from core_user c, crm_enterprise e
where c.enterprise_id = e.enterprise_id
and c.email = 'mr.smartconsult@gmail.com';

delete from core_user where email = 'charlie@wealthmakers.com';


select site_id, domain, namespace from cms_site;

update cms_site set namespace = 'ecom/whitesquares' where site_id = '539083a5-2172-4e4a-bcaa-51416a2e56cf';
update cms_site set namespace = 'ecom/amy2' where site_id = '539083a5-2172-4e4a-bcaa-51416a2e56cf';


select symbol_id, symbol, name from wm_stock_symbol where symbol_id in (20110,20119,20144,20154,20228,20229,20246,20264,20480);


select count(0) from crm_customer where email like '%test.com';

select campaign_id from crm_customer where customer_id = 'f1b53812-6414-4e62-b668-4a6cafaf8ec8';


-- scrubbing production customers
update crm_customer set email = random()||'@test.com', fname = cast(random() as varchar),
       lname = cast(random() as varchar), addr1 = cast(random() as varchar)
       where lower(lname) != 'bedwell';


alter table crm_customer_order add column shipping_addr1 varchar(50);
alter table crm_customer_order add column shipping_addr2 varchar(50);
alter table crm_customer_order add column shipping_city varchar(50);
alter table crm_customer_order add column shipping_state varchar(50);
alter table crm_customer_order add column shipping_zip varchar(50);
alter table crm_customer_order add column shipping_country varchar(50);
alter table crm_customer_order add column shipping_phone varchar(20);



----- product attributes.
-- psql -U postgres -d retail -c 'create extension "uuid-ossp";'
-- psql -U postgres -d wm -c 'create extension "uuid-ossp";'

alter table crm_product add column typex varchar(20) default 'Parent';
update crm_product set typex = type;
alter table crm_product drop column type;
alter table crm_product rename column typex to type;

alter table crm_product add column short_name varchar(50);
alter table crm_product add column attr_class varchar(50);
alter table crm_product add column render_template varchar(50);
alter table crm_product add column track_inventory boolean default true;
alter table crm_order_item add column note text;

insert into core_status_event
(event_id, event_type, short_name, display_name, claim, finalize, is_system, milestone_complete, note_req, dashboard, reason_req, change_status, touch)
values<
(uuid_generate_v4(), 'Product', 'DELETED', 'Deleted', false, true, true, false, false, false, false, true, false);



/*
drop table if exists crm_product_attribute;
create table crm_product_attribute (
   attr_id uuid not null,
   product_id uuid not null,
   attr_class varchar(50) not null,
   attr_name varchar(50) not null,
   price_modifier varchar(20) not null,
   handling_modifier varchar(20),
   weight_modifier varchar(20),
   create_dt timestamp without time zone not null,
   delete_dt timestamp without time zone,
   CONSTRAINT crm_product_attribute_pkey PRIMARY KEY (attr_id)
);
alter table crm_product_attribute add foreign key (product_id) references crm_product;
*/



select count(0) from data;
select * from thing;

ZACH = 426


select d.key from data d, thing t 
where t.thing_id= 'patient.fname'
and d.thing_id = t.thing_id
and lower(d.val_string) = 'zachary';


select d.key, d.thing_id, d.event_dt, substring(d.val_text from 0 for 30)
from data d where d.key = '426' and d.thing_id = 'encnote.mdm_note';


------ discounts
drop table if exists crm_discount;
create table crm_discount (
    discount_id uuid not null,
    enterprise_id uuid not null,
    vendor_id uuid,
    name varchar(200) not null,
    code varchar(50),
    description text,
    percent_off float,
    amount_off float,
    shipping_percent_off float,
    cart_minimum float,
    which_item varchar(30),
    start_dt date default now(),
    end_dt date,
    web_enabled boolean default true,
    store_enabled boolean default true,
    cart_discount boolean default,
    mod_dt timestamp without time zone default now(),
    create_dt timestamp without time zone default now(),
    delete_dt timestamp without time zone,
    constraint crm_discount_pk primary key (discount_id)
);
alter table crm_discount add foreign key (enterprise_id) references crm_enterprise;
alter table crm_discount add foreign key (vendor_id) references crm_vendor;

drop table if exists crm_discount_product;
create table crm_discount_product (
       discount_product_id uuid not null,
       discount_id uuid not null,
       product_id uuid not null,
       create_dt timestamp without time zone default now(),
       delete_dt timestamp without time zone,
       constraint crm_discount_product_pk primary key (discount_product_id)
);
alter table crm_discount_product add foreign key (discount_id) references crm_discount;
alter table crm_discount_product add foreign key (product_id) references crm_product;


