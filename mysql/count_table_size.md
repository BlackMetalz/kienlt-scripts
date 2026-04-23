### Simple query

- Ref: https://www.percona.com/blog/researching-your-mysql-table-sizes/

```mysql
SELECT 
    table_name AS "Table Name",
    ROUND(((data_length + index_length) / 1024 / 1024 / 1024), 2) AS "Total_Size_GB",
    ROUND((data_length / 1024 / 1024 / 1024), 2) AS "Data_Size_GB",
    ROUND((index_length / 1024 / 1024 / 1024), 2) AS "Index_Size_GB",
    table_rows AS "Total_Rows"
FROM 
    information_schema.tables
WHERE 
    table_schema = DATABASE()
ORDER BY 
    (data_length + index_length) DESC
LIMIT 10;
```