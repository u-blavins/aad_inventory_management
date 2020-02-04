
ALTER TABLE [itm].[Transaction] ADD  DEFAULT (newid()) FOR [TransactionID]
GO

ALTER TABLE [itm].[Transaction] ADD  DEFAULT ((0)) FOR [IsRefund]
GO

ALTER TABLE [usr].[User] ADD  DEFAULT (newid()) FOR [ID]
GO

ALTER TABLE [itm].[Item]  WITH CHECK ADD FOREIGN KEY([UnitName])
REFERENCES [itm].[Unit] ([UnitName])
GO

ALTER TABLE [itm].[Stock]  WITH CHECK ADD FOREIGN KEY([UnitName])
REFERENCES [itm].[Unit] ([UnitName])
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

ALTER TABLE [usr].[User] WITH CHECK ADD FOREIGN KEY([Privileges])
REFERENCES [usr].[Privilege]([AccessLevel])
GO