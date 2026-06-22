-- reset.sql 
DROP TABLE IF EXISTS tasks CASCADE; 
DROP TABLE IF EXISTS users CASCADE; 
 
-- CASCADE deletes all table dependencies! 