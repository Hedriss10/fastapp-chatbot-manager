# app/schemas/webhook.py

from typing import Optional

from pydantic import BaseModel


class Key(BaseModel):
    remoteJid: Optional[str]
    fromMe: Optional[bool]
    id: Optional[str]


class DeviceListMetadata(BaseModel):
    senderKeyHash: Optional[str]
    senderTimestamp: Optional[str]
    recipientKeyHash: Optional[str]
    recipientTimestamp: Optional[str]


class MessageContextInfo(BaseModel):
    deviceListMetadata: Optional[DeviceListMetadata]
    deviceListMetadataVersion: Optional[int]
    messageSecret: Optional[str]


class Message(BaseModel):
    conversation: Optional[str]
    messageContextInfo: Optional[MessageContextInfo]


class Data(BaseModel):
    key: Optional[Key]
    pushName: Optional[str]
    status: Optional[str]
    message: Optional[Message]
    messageType: Optional[str]
    messageTimestamp: Optional[int]
    instanceId: Optional[str]
    source: Optional[str]


class WebhookPayload(BaseModel):
    event: Optional[str]
    instance: Optional[str]
    data: Optional[Data]
    destination: Optional[str]
    date_time: Optional[str]
    sender: Optional[str]
    server_url: Optional[str]
    apikey: Optional[str]
