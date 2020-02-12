USE [StoreManagement]
GO

/****** Object:  Table [itm].[Item]    Script Date: 05/02/2020 00:44:17 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [itm].[Item](
	[Code] [varchar](10) NOT NULL,
	[Name] [varchar](25) NULL,
	[Risk] [bit] NULL,
	[Price] [float] NULL,
	[Quantity] [float] NULL,
	[MinThreshold] [float] NULL,
	[AutoPurchaseOrder] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[Code] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [itm].[ItemAssociatedUnitType]    Script Date: 05/02/2020 00:44:17 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [itm].[ItemAssociatedUnitType](
	[ItemCode] [varchar](10) NOT NULL,
	[UnitName] [varchar](50) NOT NULL,
 CONSTRAINT [pk_compositeUnitTypeConstraint] PRIMARY KEY CLUSTERED 
(
	[ItemCode] ASC,
	[UnitName] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [itm].[PurchaseOrder]    Script Date: 05/02/2020 00:44:17 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [itm].[PurchaseOrder](
	[PurchaseOrderID] [uniqueidentifier] NOT NULL,
	[UserID] [uniqueidentifier] NULL,
	[GeneratedDate] [date] NULL,
PRIMARY KEY CLUSTERED 
(
	[PurchaseOrderID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [itm].[PurchaseOrderInfo]    Script Date: 05/02/2020 00:44:17 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [itm].[PurchaseOrderInfo](
	[PurchaseOrderID] [uniqueidentifier] NOT NULL,
	[ItemCode] [varchar](10) NOT NULL,
	[Quantity] [float] NULL,
	[IsComplete] [bit] NULL,
 CONSTRAINT [pk_compositePurchaseInfoConstraint] PRIMARY KEY CLUSTERED 
(
	[PurchaseOrderID] ASC,
	[ItemCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [itm].[Transaction]    Script Date: 05/02/2020 00:44:17 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [itm].[Transaction](
	[TransactionID] [uniqueidentifier] NOT NULL,
	[UserID] [uniqueidentifier] NOT NULL,
	[DepartmentCode] [char](5) NOT NULL,
	[Price] [float] NULL,
	[TransactionDate] [date] NULL,
	[IsRefund] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[TransactionID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [itm].[TransactionInfo]    Script Date: 05/02/2020 00:44:17 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [itm].[TransactionInfo](
	[TransactionID] [uniqueidentifier] NOT NULL,
	[ItemCode] [varchar](10) NOT NULL,
	[Quantity] [float] NULL,
	[UnitName] [varchar](50) NULL,
 CONSTRAINT [pk_compositeOrderConstraint] PRIMARY KEY CLUSTERED 
(
	[TransactionID] ASC,
	[ItemCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [itm].[Unit]    Script Date: 05/02/2020 00:44:17 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [itm].[Unit](
	[UnitName] [varchar](50) NOT NULL,
	[Val] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[UnitName] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [usr].[Department]    Script Date: 05/02/2020 00:44:17 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [usr].[Department](
	[Code] [char](5) NOT NULL,
	[Name] [varchar](25) NULL,
PRIMARY KEY CLUSTERED 
(
	[Code] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [usr].[Privilege]    Script Date: 05/02/2020 00:44:17 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [usr].[Privilege](
	[AccessLevel] [int] NOT NULL,
	[Name] [varchar](25) NULL,
PRIMARY KEY CLUSTERED 
(
	[AccessLevel] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [usr].[User]    Script Date: 05/02/2020 00:44:17 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [usr].[User](
	[ID] [uniqueidentifier] NOT NULL,
	[Email] [varchar](50) NOT NULL,
	[FirstName] [varchar](40) NOT NULL,
	[LastName] [varchar](40) NOT NULL,
	[Pass] [binary](64) NOT NULL,
	[Salt] [uniqueidentifier] NOT NULL,
	[DepartmentCode] [char](5) NOT NULL,
	[Privileges] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[Email] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [itm].[Item] ADD  DEFAULT ((0)) FOR [AutoPurchaseOrder]
GO

ALTER TABLE [itm].[PurchaseOrder] ADD  DEFAULT (newid()) FOR [PurchaseOrderID]
GO

ALTER TABLE [itm].[Transaction] ADD  DEFAULT (newid()) FOR [TransactionID]
GO

ALTER TABLE [itm].[Transaction] ADD  DEFAULT ((0)) FOR [IsRefund]
GO

ALTER TABLE [usr].[User] ADD  DEFAULT (newid()) FOR [ID]
GO

ALTER TABLE [itm].[ItemAssociatedUnitType]  WITH CHECK ADD FOREIGN KEY([ItemCode])
REFERENCES [itm].[Item] ([Code])
GO

ALTER TABLE [itm].[ItemAssociatedUnitType]  WITH CHECK ADD FOREIGN KEY([UnitName])
REFERENCES [itm].[Unit] ([UnitName])
GO

ALTER TABLE [itm].[PurchaseOrder]  WITH CHECK ADD FOREIGN KEY([UserID])
REFERENCES [usr].[User] ([ID])
GO

ALTER TABLE [itm].[PurchaseOrderInfo]  WITH CHECK ADD FOREIGN KEY([ItemCode])
REFERENCES [itm].[Item] ([Code])
GO

ALTER TABLE [itm].[PurchaseOrderInfo]  WITH CHECK ADD FOREIGN KEY([PurchaseOrderID])
REFERENCES [itm].[PurchaseOrder] ([PurchaseOrderID])
GO

ALTER TABLE [itm].[Transaction]  WITH CHECK ADD FOREIGN KEY([DepartmentCode])
REFERENCES [usr].[Department] ([Code])
GO

ALTER TABLE [itm].[Transaction]  WITH CHECK ADD FOREIGN KEY([UserID])
REFERENCES [usr].[User] ([ID])
GO

ALTER TABLE [itm].[TransactionInfo]  WITH CHECK ADD FOREIGN KEY([ItemCode])
REFERENCES [itm].[Item] ([Code])
GO

ALTER TABLE [itm].[TransactionInfo]  WITH CHECK ADD FOREIGN KEY([TransactionID])
REFERENCES [itm].[Transaction] ([TransactionID])
GO

ALTER TABLE [itm].[TransactionInfo]  WITH CHECK ADD FOREIGN KEY([UnitName])
REFERENCES [itm].[Unit] ([UnitName])
GO

ALTER TABLE [usr].[User]  WITH CHECK ADD FOREIGN KEY([DepartmentCode])
REFERENCES [usr].[Department] ([Code])
GO

ALTER TABLE [usr].[User]  WITH CHECK ADD FOREIGN KEY([Privileges])
REFERENCES [usr].[Privilege] ([AccessLevel])
GO


