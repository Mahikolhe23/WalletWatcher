IF NOT EXISTS (SELECT 1 FROM sys.databases WHERE name = 'wallet_watcher')
BEGIN
    CREATE DATABASE wallet_watcher
END
GO

USE wallet_watcher
GO

IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'transactions')
BEGIN
    CREATE TABLE transactions(
        id INT IDENTITY(1,1) ,
        date DATETIME ,
        mode VARCHAR(20) ,
        amount FLOAT ,
        category VARCHAR(30)
    )
END
GO
SELECT * FROM transactions

DROP TABLE transactions
