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
copy cms_site to '/tmp/cms_site.copy';
copy wm_ireport to '/tmp/wm_ireport.copy';
copy wm_ireport_active to '/tmp/wm_ireport_active.copy';
copy wm_ireport_prediction_join to '/tmp/wm_ireport_prediction_join.copy';

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
copy cms_site from '/tmp/cms_site.copy';
copy wm_ireport from '/tmp/wm_ireport.copy';
copy wm_ireport_active from '/tmp/wm_ireport_active.copy';
copy wm_ireport_prediction_join from '/tmp/wm_ireport_prediction_join.copy';

-- select constraint_name, table_name from information_schema.table_constraints where constraint_name like '%fkey1';
alter table crm_customer drop constraint crm_customer_status_id_fkey1;
alter table crm_journal drop constraint crm_journal_order_id_fkey1;

alter table wm_customer_holding drop column customer_id;
alter table wm_customer_holding add column customer_id uuid;

drop table tmp_keepers;
drop table tmp_status_keepers;

alter table core_status add foreign key (customer_id) references crm_customer;


alter table wm_ireport drop column status_id;
alter table wm_ireport add column status_id uuid;
alter table wm_ireport add foreign key (status_id) references core_status;

alter table wm_ireport drop column user_created;
alter table wm_ireport add column user_created uuid;
alter table wm_ireport add foreign key (user_created) references core_user;

alter table wm_ireport drop column product_id;
alter table wm_ireport add column product_id uuid;
alter table wm_ireport add foreign key (product_id) references crm_product;
