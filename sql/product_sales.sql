# 商品销量核对sql
# author 江哲

# 查询销量表中没有但是订单表中有销售的商品信息
SELECT 
    a.product_id, SUM(number)
FROM
    mall_order_has_product AS a
        JOIN
    mall_order AS b ON a.order_id = b.id
WHERE
    b.status <> 1 AND b.status < 7
        AND a.product_id NOT IN (SELECT 
            product_id
        FROM
            mall_product_sales)
GROUP BY a.product_id;

# 查询销量表和订单表数据不一致的数据
SELECT 
    aa.product_id AS '商品id',
    aa.sales AS '销量表中数据',
    c.count AS '订单表中数据'
FROM
    mall_product_sales AS aa
        JOIN
    (SELECT 
        a.product_id, SUM(a.number) AS count
    FROM
        mall_order_has_product AS a
    JOIN mall_order AS b ON a.order_id = b.id
    WHERE
        b.status <> 1 AND b.status < 7
    GROUP BY a.product_id) AS c ON aa.product_id = c.product_id
WHERE
    aa.sales <> c.count;
    
-- # 更新销量不致的数据
-- set sql_safe_updates = 0;
-- update mall_product_sales as aa join 
--     (SELECT 
--         a.product_id, sum(a.number) as count
--     FROM
--         mall_order_has_product AS a
--     JOIN mall_order AS b ON a.order_id = b.id
--     where b.status <> 1 and b.status < 7
--     GROUP BY a.product_id) AS c on aa.product_id = c.product_id
-- set aa.sales = c.count
--     where aa.sales <> c.count;
--  # 更新没有销量的商品 销量为0
-- update mall_product_sales set sales = 0 where sales <> 0 and product_id not in (
-- SELECT 
-- 	a.product_id
-- FROM
-- 	mall_order_has_product AS a
-- 		JOIN
-- 	mall_order AS b ON a.order_id = b.id
-- WHERE
-- 	b.status <> 1 AND b.status < 7 )