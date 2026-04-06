Create DATABASE LeadAnalyticsDB;

use LeadAnalyticsDB;

CREATE TABLE Leads (
    LeadID INT PRIMARY KEY,
    Name VARCHAR(100),
    Company VARCHAR(100),
    Email VARCHAR(100),
    Phone VARCHAR(50),
    LeadSource VARCHAR(50),
    ServiceInterested VARCHAR(100),
    FollowUpCount INT,
    DateCreated DATE,
    Status VARCHAR(50)
);

CREATE TABLE Sales (
    SaleID INT PRIMARY KEY,
    LeadID INT,
    DealValue FLOAT,
    ClosingDate DATE,
    SalesPerson VARCHAR(100),
    CampaignType VARCHAR(50)
);

CREATE TABLE MarketingSpend (
    SpendID INT PRIMARY KEY,
    CampaignType VARCHAR(50),
    Month VARCHAR(20),
    SpendAmount FLOAT,
    LeadsGenerated INT
);

select * from Leads;

select * from Sales;

select * from MarketingSpend;

SELECT LeadSource,
COUNT(*) AS TotalLeads,
SUM(CASE WHEN Status='Converted' THEN 1 ELSE 0 END) AS Converted
FROM Leads
GROUP BY LeadSource;

