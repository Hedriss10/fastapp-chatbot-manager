# app/models/messages.py
import uuid

from sqlalchemy import (
    JSON,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModels


class SummaryMessage(BaseModels):
    __tablename__ = 'summary_message'
    __table_args__ = {'schema': 'campaign'}

    ticket: Mapped[str] = mapped_column(String(40), nullable=False)
    message: Mapped[str] = mapped_column(JSON, nullable=False)

    message_flows: Mapped[list['MessageFlow']] = relationship(
        back_populates='summary',
        foreign_keys='MessageFlow.summary_id',
        cascade='all, delete-orphan',
    )

    next_flows: Mapped[list['MessageFlow']] = relationship(
        back_populates='next_message',
        foreign_keys='MessageFlow.next_message_id',
    )


class MessageFlow(BaseModels):
    __tablename__ = 'message_flow'
    __table_args__ = {'schema': 'campaign'}

    summary_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('campaign.summary_message.id', ondelete='CASCADE'),
        nullable=False,
    )

    next_message_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('campaign.summary_message.id'), nullable=False
    )

    option_number: Mapped[int] = mapped_column(Integer, nullable=False)
    option_label: Mapped[str] = mapped_column(String(30), nullable=False)
    action_type: Mapped[str] = mapped_column(String(30), nullable=False)
    action_payload: Mapped[str] = mapped_column(JSON, nullable=False)
    # Relacionamentos
    summary: Mapped['SummaryMessage'] = relationship(
        back_populates='message_flows', foreign_keys=[summary_id]
    )
    next_message: Mapped['SummaryMessage'] = relationship(
        back_populates='next_flows', foreign_keys=[next_message_id]
    )
