# app/models/messages.py

from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base


class SummaryMessage(Base):
    __tablename__ = 'summary_message'
    __table_args__ = {'schema': 'campaign'}

    id: Mapped[int] = mapped_column(primary_key=True)
    ticket: Mapped[str] = mapped_column(String(40), nullable=False)
    message: Mapped[str] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_by: Mapped[int] = mapped_column(Integer, nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    deleted_by: Mapped[int] = mapped_column(Integer, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    message_flows: Mapped[list['MessageFlow']] = relationship(
        back_populates='summary',
        foreign_keys='MessageFlow.summary_id',
        cascade='all, delete-orphan',
    )

    next_flows: Mapped[list['MessageFlow']] = relationship(
        back_populates='next_message',
        foreign_keys='MessageFlow.next_message_id',
    )

    def __repr__(self):
        return f'SummaryMessage(id={self.id}, message={self.message})'


class MessageFlow(Base):
    __tablename__ = 'message_flow'
    __table_args__ = {'schema': 'campaign'}

    id: Mapped[int] = mapped_column(primary_key=True)

    summary_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('campaign.summary_message.id', ondelete='CASCADE'),
        nullable=False,
    )

    next_message_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('campaign.summary_message.id'), nullable=False
    )

    option_number: Mapped[int] = mapped_column(Integer, nullable=False)
    option_label: Mapped[str] = mapped_column(String(30), nullable=False)
    action_type: Mapped[str] = mapped_column(String(30), nullable=False)
    action_payload: Mapped[str] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    # Relacionamentos
    summary: Mapped['SummaryMessage'] = relationship(
        back_populates='message_flows', foreign_keys=[summary_id]
    )

    next_message: Mapped['SummaryMessage'] = relationship(
        back_populates='next_flows', foreign_keys=[next_message_id]
    )
