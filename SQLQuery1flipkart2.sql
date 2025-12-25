create database flipkart2

use flipkart2
Go

CREATE TABLE Customers (
    CustomerID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100),
    SignupDate DATE,
    TotalOrders INT,
    TotalSpent DECIMAL(10,2)
);
GO


use flipkart2;

CREATE TABLE Orders (
    OrderID INT IDENTITY(1,1) PRIMARY KEY,
    CustomerID INT FOREIGN KEY REFERENCES Customers(CustomerID),
    OrderDate DATE,
    OrderAmount DECIMAL(10,2),
    ItemsCount INT,
    IsReturned BIT
);



INSERT INTO Customers (Name, SignupDate, TotalOrders, TotalSpent)
VALUES
('Ravi Kumar',       '2022-03-15', 25, 28500.50),
('Anjali Sharma',    '2023-01-20', 12, 15800.75),
('Rahul Verma',      '2021-09-10', 35, 42500.00),
('Sneha Reddy',      '2022-11-05', 8, 7400.20),
('Amit Patel',       '2023-07-25', 5, 5250.60),
('Priya Nair',       '2021-04-18', 42, 49800.95),
('Karan Singh',      '2022-08-30', 16, 18750.10),
('Divya Joshi',      '2023-02-14', 9, 9800.75),
('Vikram Das',       '2020-12-22', 50, 51200.00),
('Neha Mehta',       '2023-05-09', 6, 6300.40);
GO


INSERT INTO Orders (CustomerID, OrderDate, OrderAmount, ItemsCount, IsReturned)
VALUES
-- Ravi Kumar (CustomerID = 1)
(1, '2024-01-10', 1250.50, 2, 0),
(1, '2024-05-15', 4800.00, 4, 0),

-- Anjali Sharma (CustomerID = 2)
(2, '2023-03-12', 1500.75, 3, 0),
(2, '2023-09-22', 3200.00, 5, 1),

-- Rahul Verma (CustomerID = 3)
(3, '2022-07-08', 5800.00, 6, 0),
(3, '2023-12-30', 4100.50, 5, 0),

-- Sneha Reddy (CustomerID = 4)
(4, '2023-08-10', 950.00, 1, 0),
(4, '2024-02-05', 3200.75, 3, 1),

-- Amit Patel (CustomerID = 5)
(5, '2023-09-18', 750.25, 1, 0),
(5, '2024-03-11', 2400.50, 2, 0),

-- Priya Nair (CustomerID = 6)
(6, '2022-06-20', 10200.00, 8, 0),
(6, '2023-11-15', 8900.25, 7, 0),

-- Karan Singh (CustomerID = 7)
(7, '2023-04-04', 2800.75, 4, 1),
(7, '2024-01-22', 4300.00, 5, 0),

-- Divya Joshi (CustomerID = 8)
(8, '2023-07-19', 1200.00, 2, 0),
(8, '2024-03-29', 2500.50, 3, 0),

-- Vikram Das (CustomerID = 9)
(9, '2022-11-10', 6000.00, 5, 0),
(9, '2024-01-25', 7200.75, 6, 0),

-- Neha Mehta (CustomerID = 10)
(10, '2023-10-02', 900.50, 1, 0),
(10, '2024-02-16', 1500.00, 2, 0);
GO

select * from Customers;
select * from Orders;