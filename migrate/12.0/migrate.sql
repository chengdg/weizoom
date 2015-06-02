ALTER TABLE webapp_workspace ADD COLUMN template_name varchar(125) default 'default';
ALTER TABLE webapp_workspace ADD COLUMN backend_template_name varchar(125) default 'default';
ALTER TABLE mall_config ADD COLUMN is_enable_bill tinyint(1) default 0;
ALTER TABLE mall_order_has_product ADD COLUMN product_model_name varchar(256) default 'standard';
ALTER TABLE mall_shopping_cart ADD COLUMN product_model_name varchar(125) default 'standard';
