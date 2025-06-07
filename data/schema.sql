IF NOT EXISTS (SELECT 1 FROM sys.databases WHERE name = 'wallet_watcher')
BEGIN
    CREATE DATABASE wallet_watcher
END
GO

USE wallet_watcher
GO


