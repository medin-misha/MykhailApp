from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta, datetime, timezone

from core.models import Subscription, UserSubscription, User
from contracts.subscriptions import SubscribeUserCreate, SubscribeUserReturn, SubscribeUserCreateForm
from services import CRUD
from services.user.crud import get_user_by_chat_id

async def subscribe(data: SubscribeUserCreateForm, session: AsyncSession) -> SubscribeUserReturn:
    user: User = await get_user_by_chat_id(chat_id=data.chat_id, session=session)
    subscription: Subscription = await CRUD.get(model=Subscription, id=data.subscription_id, session=session)
    expires_at: datetime = datetime.now(tz=timezone.utc) + timedelta(days=subscription.term_days)
    created_form = SubscribeUserCreate(
        user_id=user.id,
        subscription_id=subscription.id,
        expires_at=expires_at if subscription.term_days > 0 else None,
        source=data.source,
        active=True
    )
    user_subscription = UserSubscription(**created_form.model_dump())
    session.add(user_subscription)
    await session.commit()
    await session.refresh(user_subscription)

    return SubscribeUserReturn.model_validate(user_subscription)

